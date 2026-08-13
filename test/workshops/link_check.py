#!/usr/bin/env python3
"""Verify every link a learner can click resolves — no cluster needed.

House requirement: all links in the workshop must respond 200. Everything a learner
reads is scanned, not just the instructions:

  * `workshop/content/**.md`   — the instructions
  * `workshop/slides/**.md`    — the slide decks
  * `exercises/**.md`          — files the learner opens in the editor
  * `README.md`                — the lab's own readme
  * `resources/consolelab.yaml` — console labs (guided console tours) keep their
    learner-facing text in the CR, so they have no content/ dir at all

Link kinds:

  * external public (https://kubernetes.io/..., docs.openshift.com/...) → HTTP GET, must
    be 2xx after redirects. A dead upstream doc = a learner clicking into a 404.
  * relative (`foo.svg`, `../bar.md`, `#anchor`) → the target file must exist in the repo.
  * internal / air-gapped (`{{< param dcs_docs_base_url >}}/...`, or any link resolving to
    a placeholder `example.*` host) → reported but NOT fetched by default: the DCS docs are
    unreachable from a public runner. Give the real host to check them too — see below.

The base URL for internal docs comes from the shared chart values
(`values.yaml` → `params.dcsDocsBaseUrl`, the same value the
TrainingPortal injects into every session), then each lab's `workshop/config.yaml`
param as a fallback, then `--param` which always wins. Since the committed value is
the placeholder `https://docs.example.dcs`, internal links are only really fetched
when a real host is supplied:

Exit 0 when no reachable link is broken; exit 1 otherwise. Every failure is repeated
in one flat `file:line` list at the end.

  ./link_check.py lab-a02-kubernetes-essentials
  ./link_check.py --all
  ./link_check.py --all --param dcs_docs_base_url=https://docs.internal.dcs --check-internal
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys

import deploy_workshop as dw

GREEN, RED, YEL, DIM, RST = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
PLACEHOLDER_HOSTS = ("example.dcs", "example.com", ".svc", "localhost", "127.0.0.1")
LINK_RE = re.compile(r"\]\(\s*<?([^)]+?)>?\s*\)")       # ](url) / ](<url>) / ](url "title")
PARAM_RE = re.compile(r"\{\{<\s*param\s+(\w+)\s*>\}\}")
# Authoring comments explain the markdown syntax with literal `[text](url)` samples —
# those are documentation, not links. Drop HTML comments before scanning.
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


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


def load_shared_params():
    """values.yaml `params:` → {snake_case_name: value}.

    That block is the single source of truth for the author params (the chart injects
    them as session env on every workshop, each lab's config.yaml param only carries
    the same value as an offline fallback). camelCase there, snake_case in content:
    dcsDocsBaseUrl → dcs_docs_base_url. Tiny parser, no PyYAML — same reason as above.
    """
    vals = dw.REPO_ROOT / "values.yaml"
    out, inside = {}, False
    if not vals.exists():
        return out
    for ln in vals.read_text().splitlines():
        if re.match(r"^params:\s*$", ln):
            inside = True
            continue
        if inside:
            m = re.match(r"^  (\w+):\s*(.+?)\s*$", ln)
            if not m:
                if ln.strip() and not ln.startswith((" ", "\t")):
                    break                       # next top-level key ends the block
                continue
            snake = re.sub(r"(?<!^)(?=[A-Z])", "_", m.group(1)).lower()
            out[snake] = m.group(2).strip().strip("\"'")
    return out


def learner_facing_files(subpath):
    """Every file whose links a learner can click, in reading order."""
    root = dw.REPO_ROOT / subpath
    files = []
    for pattern in ("workshop/content/**/*.md", "workshop/slides/**/*.md", "exercises/**/*.md"):
        files += sorted(root.glob(pattern))
    for extra in ("README.md", "resources/consolelab.yaml"):
        if (root / extra).exists():
            files.append(root / extra)
    return files


def resolve_params(url, params):
    return PARAM_RE.sub(lambda m: params.get(m.group(1), f"__UNRESOLVED_{m.group(1)}__"), url)


# Codes that mean "the URL is valid, the server just refuses an automated request"
# (some sites 403/429 a non-browser client). Reported, not failed.
SOFT_CODES = {"401", "403", "405", "429"}

# Corp egress proxy config, supplied via env (gitlab-ci variables), never hardcoded.
#   HTTPS_PROXY   e.g. http://divproxy01.dsmain.ds.corp:8080
#   PROXY_USER / PROXY_PASSWORD   NTLM creds, masked in CI
#   NO_PROXY      hosts fetched directly (e.g. the internal docs host). Semicolon or
#                 comma separated; curl also still honours its own *_proxy env vars.
# When present the proxy is used with --proxy-ntlm, which is what the corp proxy needs
# (curl's automatic env-proxy only does Basic auth, so it would fail against NTLM).


def proxy_args():
    """curl flags for the corp proxy, or [] when no proxy is configured."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTPSproxy") \
        or os.environ.get("https_proxy")
    if not proxy:
        return []
    args = ["-x", proxy]
    user, pw = os.environ.get("PROXY_USER"), os.environ.get("PROXY_PASSWORD")
    if user:
        args += ["--proxy-ntlm", "--proxy-user", f"{user}:{pw or ''}"]
    # Hosts to fetch directly, bypassing the proxy (internal docs host among them).
    no_proxy = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
    if no_proxy:
        args += ["--noproxy", no_proxy.replace(";", ",")]
    return args


def curl_code(url):
    # Follow redirects (-L) so a 301/302 landing on a 200 stays a pass. Send curl's
    # genuine default user-agent: redhat.com's WAF (now the target of many
    # docs.openshift.com redirects) blocks requests that fake a Chrome UA, but allows
    # plain curl. A browser-like `Accept` header alone is enough elsewhere.
    # -k: the internal docs / proxy hosts use self-signed or internal-CA certs the runner's
    # bundle doesn't trust. Without -k, curl aborts on cert validation -> every internal link
    # reports "000" (no HTTP status ever reached) even though the server is fine.
    # NB: a 000 otherwise means curl never got an HTTP status from the server — the
    # connection/CDN/proxy failed before anyone answered. The reason is intentionally
    # not echoed here (a corp proxy's own error page only adds noise); the CI proxy
    # probe explains the cause in one clear line instead.
    r = subprocess.run(["curl", "-ksSL", "-m", "20",
                        "-H", "Accept: text/html,application/xhtml+xml",
                        *proxy_args(),
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
    # Educates runtime dashboard routes (e.g. /slides/#anchor opens the Slides tab) —
    # served at session runtime, not content files, so don't resolve them on disk.
    if url.startswith("/slides/"):
        return "skip", url
    if url.startswith(("http://", "https://")):
        host = url.split("/", 3)[2] if "/" in url[8:] + "/" else url
        if had_param or any(h in url for h in PLACEHOLDER_HOSTS) or "__UNRESOLVED_" in url:
            return "internal", url
        return "external", url
    if "__UNRESOLVED_" in url or had_param:      # param that isn't a full URL → internal doc path
        return "internal", url
    return "relative", url


def check_workshop(name, subpath, params, cache, check_internal, skip_external=False, debug=False):
    files = learner_facing_files(subpath)
    if not files:
        return None, [f"{YEL}skip{RST} {name}: no content/slides/README"], []

    bad, soft, n_ext, n_int, n_rel = [], [], 0, 0, 0
    lines = []
    for f in files:
        text = f.read_text()
        # Blank out comments in place so match offsets still map to real line numbers.
        text = COMMENT_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
        for m in LINK_RE.finditer(text):
            raw = clean_target(m.group(1))
            if not raw:
                continue
            kind, url = classify(raw, params)
            if kind == "skip":
                if debug:
                    lines.append(f"  SKIP    {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {url}")
                continue
            where = (f, text.count("\n", 0, m.start()) + 1)
            if kind == "relative":
                n_rel += 1
                target = (f.parent / url.split("#", 1)[0]).resolve()
                if not target.exists():
                    bad.append((where, raw, "relative target missing", ""))
                    if debug:
                        lines.append(f"  FAIL    {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {raw}  → missing")
                elif debug:
                    lines.append(f"  OK      {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {raw}  → exists")
            elif kind == "internal":
                n_int += 1
                if check_internal and url.startswith(("http://", "https://")) and "__UNRESOLVED_" not in url:
                    v = code_verdict(cache.setdefault(url, curl_code(url)))
                    if debug:
                        code = cache[url] or "ERR"
                        lines.append(f"  {'OK' if v == 'ok' else 'SOFT' if v == 'soft' else 'FAIL'}  {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {url}  → HTTP {code}")
                    if v == "bad":
                        bad.append((where, url, f"internal link HTTP {cache[url] or 'ERR'}", cache[url] or ""))
                    elif v == "soft" and debug:
                        lines.append(f"        (server blocks automated fetch, link assumed valid)")
                elif debug:
                    lines.append(f"  SKIP    {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {url}  → internal, not fetched (no --check-internal or non-http)")
            else:  # external
                n_ext += 1
                if skip_external:
                    if debug:
                        lines.append(f"  SKIP    {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {url}  → external, not fetched (--skip-external)")
                    continue
                code = cache.setdefault(url, curl_code(url))
                v = code_verdict(code)
                if debug:
                    lines.append(f"  {'OK' if v == 'ok' else 'SOFT' if v == 'soft' else 'FAIL'}  {f.relative_to(dw.REPO_ROOT)}:{text.count(chr(10), 0, m.start()) + 1}  {url}  → HTTP {code or 'ERR'}")
                if v == "bad":
                    bad.append((where, url, f"HTTP {code or 'ERR'}", code))
                elif v == "soft":
                    soft.append((where, url, code))

    ok = not bad
    head = f"{GREEN if ok else RED}{'PASS' if ok else 'FAIL'}{RST}"
    intnote = f", {n_int} internal {'(checked)' if check_internal else '(air-gapped, not fetched)'}"
    softnote = f", {len(set(u for _, u, _ in soft))} bot-blocked" if soft else ""
    extnote = " (offline, not fetched)" if skip_external else ""
    lines.append(f"{head} {name}: {len(files)} files, {n_ext} external{extnote}, "
                 f"{n_rel} relative{intnote}{softnote}")
    for (f, ln), url, why, _code in bad:
        lines.append(f"     {RED}{why}{RST}  {url}  {DIM}({f.relative_to(dw.REPO_ROOT)}:{ln}){RST}")
    for (f, ln), url, code in soft:
        lines.append(f"     {DIM}{code} (server blocks automated fetch, link assumed valid)  {url}{RST}")
    return ok, lines, [(name, f, ln, url, why, code) for (f, ln), url, why, code in bad]


def main():
    p = argparse.ArgumentParser(description="Verify workshop content links respond 200.")
    p.add_argument("name", nargs="?")
    p.add_argument("--all", action="store_true")
    p.add_argument("--param", action="append", default=[], metavar="NAME=VALUE",
                   help="override a config param (e.g. dcs_docs_base_url=https://docs.internal)")
    p.add_argument("--check-internal", action="store_true",
                   help="also fetch internal/param links (only works on a network that can reach them)")
    p.add_argument("--summary-file", metavar="PATH",
                   help="also write the broken-link list to PATH, plain text, one per line "
                        "(lab · file:line · reason · url). Written only when something failed, "
                        "so CI can re-print it as the last thing in the job log.")
    p.add_argument("--summary-csv", metavar="PATH",
                   help="also write the broken links to PATH as CSV with a header "
                        "(lab,file,line,reason,url,http_code) for easy filtering/sorting in a "
                        "spreadsheet. Written only when something failed.")
    p.add_argument("--skip-external", action="store_true",
                   help="don't fetch public links (air-gapped runner has no internet). They are "
                        "still counted and the relative/internal checks still run.")
    p.add_argument("--require-real-docs-url", action="store_true",
                   help="fail if the effective dcs_docs_base_url is still a placeholder host "
                        "(those links ship as 404s; CI uses this so a placeholder can't pass silently)")
    p.add_argument("--debug", action="store_true",
                   help="print every link with its classification (external/internal/"
                        "relative/skip) and whether it was actually fetched + the HTTP code")
    args = p.parse_args()

    overrides = dict(kv.split("=", 1) for kv in args.param)
    if args.all:
        names = sorted(dw.all_workshop_paths())
    elif args.name:
        names = [args.name]
    else:
        p.error("a workshop name or --all is required")

    shared = load_shared_params()
    cache, failures = {}, []
    debug_lines = [] if args.debug else None
    print("=== workshop link check (external links must be 2xx; relative targets must exist) ===")
    docs_base = overrides.get("dcs_docs_base_url", shared.get("dcs_docs_base_url", "(unset)"))
    print(f"    content + slides + exercises + README + consolelab.yaml")
    print(f"    dcs_docs_base_url={docs_base}"
          f"{'  (fetched)' if args.check_internal else '  (not fetched; pass --check-internal)'}")
    if args.debug:
        print(f"\n=== DEBUG: every link found, its classification, and whether it was fetched ===")
    for nm in names:
        subpath = dw.find_subpath(nm) or f"{dw.DEFAULT_BASE}/{nm}"
        params = load_params(subpath)
        params.update(shared)                # shared chart values beat the lab's offline default
        params.update(overrides)             # --param wins over everything
        ok, report, bad = check_workshop(nm, subpath, params, cache, args.check_internal,
                                          args.skip_external, args.debug)
        for ln in report:
            print(ln)
        failures += bad
        if debug_lines is not None:
            debug_lines += report

    # lab · file:line · reason · url — everything needed to open the page and fix it, with
    # no colour codes so it survives being written to a file and pasted elsewhere.
    fix_lines = [f"{nm}  {f.relative_to(dw.REPO_ROOT)}:{ln}  {why}  {url}"
                 for nm, f, ln, url, why, _code in failures]

    if failures:
        # One flat list at the end: the per-lab output above scrolls away in a CI log.
        print(f"\n{RED}BROKEN LINKS ({len(failures)}){RST} — a learner following these hits a 404 / missing image:")
        for nm, f, ln, url, why, _code in failures:
            print(f"  {f.relative_to(dw.REPO_ROOT)}:{ln}  {RED}{why}{RST}  {url}  {DIM}[{nm}]{RST}")
    elif args.skip_external:
        print(f"\n{GREEN}all relative + internal links resolve{RST} "
              f"{YEL}(public links not fetched — offline mode){RST}")
    else:
        print(f"\n{GREEN}all reachable links resolve.{RST}")

    # A placeholder docs host is the one broken-link class this check used to miss: those
    # links are skipped as "internal, not fetched", so the job stayed green while every DCS
    # doc link shipped as a 404 (that is exactly how the A00 environment-guide link reached
    # learners). Fetching them needs a runner that can reach the docs; knowing the value is
    # still a placeholder needs no network at all — so check that unconditionally in CI.
    placeholder_docs = args.require_real_docs_url and (
        docs_base == "(unset)" or any(h in docs_base for h in PLACEHOLDER_HOSTS))
    if placeholder_docs:
        print(f"\n{RED}PLACEHOLDER DOCS URL{RST} — dcs_docs_base_url is {docs_base!r}.")
        print("  Every {{< param dcs_docs_base_url >}} link in the catalog resolves to that host,")
        print("  so they all 404 for learners. Set the real host and re-run:")
        print("    values.yaml → params.dcsDocsBaseUrl (or the per-cluster")
        print("    argocd/envs/*.yaml), and the CI variable DCS_DOCS_BASE_URL for this check.")
        fix_lines.append(f"(all labs)  values.yaml  dcs_docs_base_url is the "
                         f"placeholder {docs_base} — every DCS doc link 404s")

    if args.summary_file and fix_lines:
        pathlib.Path(args.summary_file).write_text("\n".join(fix_lines) + "\n")

    if args.summary_csv and failures:
        import csv
        with open(args.summary_csv, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["lab", "file", "line", "reason", "url", "http_code"])
            for nm, f, ln, url, why, code in failures:
                w.writerow([nm, f.relative_to(dw.REPO_ROOT), ln, why, url, code])

    if args.debug and debug_lines:
        # Aggregate the per-link DEBUG output into counts so the user can see at a glance
        # how many links were actually tested vs skipped.
        from collections import Counter
        tags = Counter(ln.split()[0] for ln in debug_lines if ln.strip() and ln[0] in " OSFK")
        print(f"\n=== DEBUG SUMMARY ===")
        print(f"  OK      = fetched and resolved  ({tags.get('OK', 0)})")
        print(f"  SOFT    = fetched, server blocked automated access (401/403/405/429) ({tags.get('SOFT', 0)})")
        print(f"  FAIL    = fetched and did NOT resolve                       ({tags.get('FAIL', 0)})")
        print(f"  SKIP    = not fetched (classification or flag prevented it) ({tags.get('SKIP', 0)})")

    sys.exit(1 if (failures or placeholder_docs) else 0)


if __name__ == "__main__":
    main()
