#!/usr/bin/env python3
"""Verify every link in a workshop's description resolves — no cluster needed.

House requirement: all links in the workshop content must respond 200. This checks each
link found in `workshop/content/**.md` (+ the workshop README):

  * external public (https://kubernetes.io/..., docs.openshift.com/...) → HTTP GET, must
    be 2xx after redirects. A dead upstream doc = a learner clicking into a 404.
  * relative (`foo.svg`, `../bar.md`, `#anchor`) → the target file must exist in the repo.
  * internal / air-gapped (`{{< param dcs_docs_base_url >}}/...`, or any link resolving to
    a placeholder `example.*` host) → reported but NOT fetched: the DCS docs are unreachable
    from CI by default. On the real network, pass `--param dcs_docs_base_url=https://real`
    (and --check-internal) to verify them too.

Exit 0 when no reachable link is broken; exit 1 otherwise.

  ./link_check.py lab-a02-kubernetes-essentials
  ./link_check.py --all
  ./link_check.py --all --param dcs_docs_base_url=https://docs.internal.dcs --check-internal
"""
import argparse
import pathlib
import re
import subprocess
import sys

import deploy_workshop as dw

GREEN, RED, YEL, DIM, RST = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
PLACEHOLDER_HOSTS = ("example.dcs", "example.com", ".svc", "localhost", "apps-crc.testing", "127.0.0.1")
LINK_RE = re.compile(r"\]\(\s*<?([^)]+?)>?\s*\)")       # ](url) / ](<url>) / ](url "title")
PARAM_RE = re.compile(r"\{\{<\s*param\s+(\w+)\s*>\}\}")


def clean_target(g):
    """Strip a trailing markdown title and, for non-templated links, anything after the URL.
    A `{{< param X >}}` template legitimately contains spaces, so keep those intact."""
    g = re.sub(r"""\s+["'].*$""", "", g).strip()        # drop ](url "title")
    if "{{<" not in g and " " in g:
        g = g.split()[0]
    return g


def load_params(subpath):
    """workshop/config.yaml params (list of {name,value}) → {name: value}. Tiny parser, no PyYAML."""
    cfg = dw.REPO_ROOT / subpath / "workshop" / "config.yaml"
    out, name = {}, None
    if cfg.exists():
        for ln in cfg.read_text().splitlines():
            m = re.match(r"\s*-\s*name:\s*(.+)", ln)
            if m:
                name = m.group(1).strip().strip("\"'")
                continue
            m = re.match(r"\s*value:\s*(.+)", ln)
            if m and name:
                out[name] = m.group(1).strip().strip("\"'")
                name = None
    return out


def resolve_params(url, params):
    return PARAM_RE.sub(lambda m: params.get(m.group(1), f"__UNRESOLVED_{m.group(1)}__"), url)


# Codes that mean "the URL is valid, the server just refuses an automated request"
# (docs.openshift.com 403s any non-browser client). Reported, not failed.
SOFT_CODES = {"401", "403", "405", "429"}
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def curl_code(url):
    r = subprocess.run(["curl", "-sSL", "-m", "20", "-A", UA,
                        "-H", "Accept: text/html,application/xhtml+xml",
                        "-o", "/dev/null", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    return r.stdout.strip()


def code_verdict(code):
    """'ok' | 'soft' | 'bad'."""
    if code and code[0] in "23":
        return "ok"
    if code in SOFT_CODES:
        return "soft"
    return "bad"


def classify(raw, params):
    """-> (kind, resolved_url) where kind in {external, internal, relative, skip}."""
    had_param = bool(PARAM_RE.search(raw))
    url = resolve_params(raw, params).rstrip(".,;:")
    if url.startswith("#") or url.startswith("mailto:"):
        return "skip", url
    if url.startswith(("http://", "https://")):
        host = url.split("/", 3)[2] if "/" in url[8:] + "/" else url
        if had_param or any(h in url for h in PLACEHOLDER_HOSTS) or "__UNRESOLVED_" in url:
            return "internal", url
        return "external", url
    if "__UNRESOLVED_" in url or had_param:      # param that isn't a full URL → internal doc path
        return "internal", url
    return "relative", url


def check_workshop(name, subpath, params, cache, check_internal):
    cdir = dw.REPO_ROOT / subpath / "workshop" / "content"
    files = []
    if cdir.exists():
        files += sorted(cdir.rglob("*.md"))
    readme = dw.REPO_ROOT / subpath / "README.md"
    if readme.exists():
        files.append(readme)
    if not files:
        return None, [f"{YEL}skip{RST} {name}: no content/README"]

    bad, soft, n_ext, n_int, n_rel = [], [], 0, 0, 0
    lines = []
    for f in files:
        for m in LINK_RE.finditer(f.read_text()):
            raw = clean_target(m.group(1))
            if not raw:
                continue
            kind, url = classify(raw, params)
            if kind == "skip":
                continue
            if kind == "relative":
                n_rel += 1
                target = (f.parent / url.split("#", 1)[0]).resolve()
                if not target.exists():
                    bad.append((f, raw, "relative target missing"))
            elif kind == "internal":
                n_int += 1
                if check_internal and url.startswith(("http://", "https://")) and "__UNRESOLVED_" not in url:
                    v = code_verdict(cache.setdefault(url, curl_code(url)))
                    if v == "bad":
                        bad.append((f, url, f"internal link HTTP {cache[url] or 'ERR'}"))
            else:  # external
                n_ext += 1
                code = cache.setdefault(url, curl_code(url))
                v = code_verdict(code)
                if v == "bad":
                    bad.append((f, url, f"HTTP {code or 'ERR'}"))
                elif v == "soft":
                    soft.append((f, url, code))

    ok = not bad
    head = f"{GREEN if ok else RED}{'PASS' if ok else 'FAIL'}{RST}"
    intnote = f", {n_int} internal {'(checked)' if check_internal else '(air-gapped, not fetched)'}"
    softnote = f", {len(set(u for _, u, _ in soft))} bot-blocked" if soft else ""
    lines.append(f"{head} {name}: {n_ext} external, {n_rel} relative{intnote}{softnote}")
    for f, url, why in bad:
        lines.append(f"     {RED}{why}{RST}  {url}  {DIM}({f.relative_to(dw.REPO_ROOT)}){RST}")
    for f, url, code in soft:
        lines.append(f"     {DIM}{code} (server blocks automated fetch, link assumed valid)  {url}{RST}")
    return ok, lines


def main():
    p = argparse.ArgumentParser(description="Verify workshop content links respond 200.")
    p.add_argument("name", nargs="?")
    p.add_argument("--all", action="store_true")
    p.add_argument("--param", action="append", default=[], metavar="NAME=VALUE",
                   help="override a config param (e.g. dcs_docs_base_url=https://docs.internal)")
    p.add_argument("--check-internal", action="store_true",
                   help="also fetch internal/param links (only works on a network that can reach them)")
    args = p.parse_args()

    overrides = dict(kv.split("=", 1) for kv in args.param)
    if args.all:
        names = sorted(dw.all_workshop_paths())
    elif args.name:
        names = [args.name]
    else:
        p.error("a workshop name or --all is required")

    cache, any_fail = {}, False
    print("=== workshop link check (external links must be 2xx; relative targets must exist) ===")
    for nm in names:
        subpath = dw.find_subpath(nm) or f"{dw.DEFAULT_BASE}/{nm}"
        params = load_params(subpath)
        params.update(overrides)             # --param wins over the workshop's config
        ok, report = check_workshop(nm, subpath, params, cache, args.check_internal)
        for ln in report:
            print(ln)
        if ok is False:
            any_fail = True

    if any_fail:
        print(f"\n{RED}BROKEN LINKS{RST}: a learner following these would hit a 404 / missing image.")
    else:
        print(f"\n{GREEN}all reachable links resolve.{RST}")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
