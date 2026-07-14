#!/usr/bin/env python3
"""Verify a workshop's smoke plan still matches the workshop content — WITHOUT a cluster.

The problem this solves: smoke plans (smoke-plans/<lab>.json) live apart from the
workshop markdown, so a plan can silently rot when a command's examiner check changes.
This script LINKS them: it parses every `examiner:execute-test` block in the workshop
content and checks the plan exercises each one (same test name + args). Change a check's
args in the content and this fails until the plan is updated — you never hand-audit.

It also flags:
  * dead graders  — files in examiner/tests/ no content block references,
  * command debt  — `terminal:execute*` blocks with no examiner check nearby (info only;
                    the house standard is "a check for every command", atomic sequences
                    may share one — see the review skill dimension I).

Exit 0 when every content check is either exercised by a plan step or listed in the plan's
`exclude` (with a reason); exit 1 when any content check is unaccounted for.

  ./coverage_check.py lab-a02-kubernetes-essentials
  ./coverage_check.py --all                       # every workshop with a plan
"""
import argparse
import json
import pathlib
import re
import sys

import deploy_workshop as dw          # resolver + REPO_ROOT (same dir)

HERE = pathlib.Path(__file__).resolve().parent
PLANS = HERE / "smoke-plans"
GREEN, RED, YEL, DIM, RST = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"

FENCE = re.compile(r"^```examiner:execute-test\s*$")
TERMINAL = re.compile(r"^```terminal:(execute|execute-1|execute-2)\b")
TERM_FENCE = re.compile(r"^```terminal:(execute|execute-1|execute-2)\s*$")


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        return s[1:-1]
    return s


def parse_examiner_blocks(md_text):
    """Yield (name, [args]) for each ```examiner:execute-test``` block. Tiny YAML subset
    (name/args only) so no PyYAML dependency."""
    out, lines, i = [], md_text.splitlines(), 0
    while i < len(lines):
        if FENCE.match(lines[i]):
            i += 1
            name, args, in_args = "", [], False
            while i < len(lines) and not lines[i].startswith("```"):
                ln = lines[i]
                if re.match(r"^\s*name:\s*", ln):
                    name = _unquote(ln.split(":", 1)[1])
                    in_args = False
                elif re.match(r"^\s*args:\s*$", ln):
                    in_args = True
                elif in_args and re.match(r"^\s*-\s+", ln):
                    args.append(_unquote(re.sub(r"^\s*-\s+", "", ln)))
                elif in_args and ln.strip() and not ln.startswith(" "):
                    in_args = False
                i += 1
            if name:
                out.append((name, args))
        i += 1
    return out


def parse_doc_order(md_text):
    """Yield ('run', command) and ('check', name, args) in document order — used to
    scaffold a starter plan straight from the workshop content."""
    lines, i = md_text.splitlines(), 0
    while i < len(lines):
        if TERM_FENCE.match(lines[i]):
            i += 1
            cmd = ""
            while i < len(lines) and not lines[i].startswith("```"):
                ln = lines[i]
                if re.match(r"^\s*command:\s*", ln):
                    val = ln.split(":", 1)[1].strip()
                    cmd = "" if val in ("|", "|-", "|+") else val   # block scalar → body follows
                elif cmd == "" and ln.strip() and not re.match(r"^\s*command:", ln):
                    cmd = ln.strip()
                i += 1
            if cmd:
                yield ("run", cmd)
        elif FENCE.match(lines[i]):
            i += 1
            name, args, in_args = "", [], False
            while i < len(lines) and not lines[i].startswith("```"):
                ln = lines[i]
                if re.match(r"^\s*name:\s*", ln):
                    name = _unquote(ln.split(":", 1)[1]); in_args = False
                elif re.match(r"^\s*args:\s*$", ln):
                    in_args = True
                elif in_args and re.match(r"^\s*-\s+", ln):
                    args.append(_unquote(re.sub(r"^\s*-\s+", "", ln)))
                i += 1
            if name:
                yield ("check", name, args)
        i += 1


def scaffold(name, subpath):
    """Print a starter smoke plan derived from the workshop content (doc order). Run
    steps are the terminal commands; check steps are the examiner blocks. Hand-tune the
    run steps for determinism (rollout waits, env) before committing — this is a draft."""
    cdir = content_dir(subpath)
    steps = []
    for md in sorted(cdir.rglob("*.md")):
        for item in parse_doc_order(md.read_text()):
            if item[0] == "run":
                steps.append({"run": item[1]})
            else:
                steps.append({"check": item[1], "args": item[2]})
    plan = {"workshop": name,
            "_note": "SCAFFOLD from content — review run steps (add rollout waits/env) before trusting the smoke run.",
            "steps": steps}
    print(json.dumps(plan, indent=2))


def content_dir(subpath):
    return dw.REPO_ROOT / subpath / "workshop" / "content"


def tests_dir(subpath):
    return dw.REPO_ROOT / subpath / "workshop" / "examiner" / "tests"


def args_match(content_args, plan_args):
    """A content check matches a plan step when the name matches (checked by caller),
    arg counts match, and each content arg either equals the plan arg OR is an env
    placeholder (`$VAR` / `${VAR}` — Educates expands these at runtime, the plan encodes
    the concrete CRC value). So literal args stay coupled; env-substituted ones don't
    trip a false mismatch."""
    if not content_args:
        return True          # a no-arg content ref (e.g. a summary re-check) = "exercised somewhere"
    if len(content_args) != len(plan_args):
        return False
    return all("$" in c or c == p for c, p in zip(content_args, plan_args))


def check_workshop(name, subpath):
    """Return (ok, coverage_pct, report_lines)."""
    cdir, tdir = content_dir(subpath), tests_dir(subpath)
    plan_path = PLANS / f"{name}.json"
    lines = []

    if not cdir.exists():
        return None, 0.0, [f"{YEL}skip{RST} {name}: no content dir ({cdir})"]

    required, block_names, term_count = [], set(), 0
    seen = set()
    for md in sorted(cdir.rglob("*.md")):
        text = md.read_text()
        term_count += len(TERMINAL.findall("\n".join(
            l for l in text.splitlines() if l.startswith("```terminal:"))))
        for nm, args in parse_examiner_blocks(text):
            k = (nm, tuple(args))
            if k not in seen:                    # dedup identical blocks
                seen.add(k)
                required.append((nm, args))
            block_names.add(nm)

    if not plan_path.exists():
        return False, 0.0, [f"{RED}FAIL{RST} {name}: no smoke plan (smoke-plans/{name}.json); "
                            f"content has {len(required)} examiner checks to cover"]

    plan = json.loads(plan_path.read_text())
    plan_checks = [(s["check"], s.get("args", [])) for s in plan.get("steps", []) if "check" in s]
    # `exclude`: content checks a plan can't run on CRC (SCC/Kyverno-dependent, interactive).
    # Listing one — with a reason — keeps coverage honest: the check is consciously accounted
    # for (not silently dropped), and a NEW content check still trips UNTESTED until covered.
    excludes = [(e["check"], e.get("args", []), e.get("reason", "")) for e in plan.get("exclude", [])]

    missing, excluded, matched_plan = [], [], set()
    for nm, args in required:
        hit = next((j for j, (pn, pa) in enumerate(plan_checks)
                    if j not in matched_plan and pn == nm and args_match(args, pa)), None)
        if hit is not None:
            matched_plan.add(hit)
            continue
        ex = next((r for en, ea, r in excludes if en == nm and args_match(args, ea)), None)
        if ex is not None:
            excluded.append((nm, args, ex))
        else:
            missing.append((nm, args))
    extra = [pc for j, pc in enumerate(plan_checks) if j not in matched_plan]

    exercised = len(required) - len(missing) - len(excluded)
    pct = 100.0 if not required else 100.0 * exercised / len(required)
    ok = not missing            # excludes are allowed; only unaccounted checks fail

    head = f"{GREEN if ok else RED}{'PASS' if ok else 'FAIL'}{RST}"
    extra_note = f", {len(excluded)} excluded" if excluded else ""
    lines.append(f"{head} {name}: {exercised}/{len(required)} content checks exercised "
                 f"({pct:.0f}%{extra_note})")
    for nm, args in missing:
        lines.append(f"     {RED}UNTESTED{RST} content check `{nm} {' '.join(args)}` "
                     f"has no matching plan step {DIM}(add a step, or an \"exclude\" entry with a "
                     f"reason, to smoke-plans/{name}.json){RST}")
    for nm, args, reason in excluded:
        lines.append(f"     {YEL}excluded{RST} `{nm} {' '.join(args)}` {DIM}— {reason or 'no reason given'}{RST}")
    for nm, args in extra:
        lines.append(f"     {DIM}extra plan step `{nm} {' '.join(args)}` "
                     f"(setup/precondition, not a content check){RST}")

    # dead graders: shipped test files no content block names
    if tdir.exists():
        shipped = {p.name for p in tdir.iterdir() if p.is_file()}
        dead = sorted(shipped - block_names)
        for d in dead:
            lines.append(f"     {YEL}dead grader{RST} examiner/tests/{d} referenced by no content block")

    if term_count and len(block_names) == 0:
        lines.append(f"     {YEL}note{RST} {term_count} terminal commands, 0 examiner checks "
                     f"(conceptual lab? else violates 'a check for every command')")
    return ok, pct, lines


def main():
    p = argparse.ArgumentParser(description="Verify smoke plans still cover workshop content.")
    p.add_argument("name", nargs="?", help="workshop dir name; omit with --all")
    p.add_argument("--all", action="store_true", help="check every workshop in the monorepo")
    p.add_argument("--scaffold", action="store_true",
                   help="print a starter plan derived from the named workshop's content, then exit")
    p.add_argument("--base", default=dw.DEFAULT_BASE)
    args = p.parse_args()

    if args.scaffold:
        if not args.name:
            p.error("--scaffold needs a workshop name")
        scaffold(args.name, dw.find_subpath(args.name) or f"{args.base}/{args.name}")
        return

    if args.all:
        names = sorted(dw.all_workshop_paths())        # every workshop, so a planless one is flagged
    elif args.name:
        names = [args.name]
    else:
        p.error("a workshop name or --all is required")

    any_fail = False
    print("=== smoke-plan coverage (every content examiner check must be exercised or excluded) ===")
    for nm in names:
        subpath = dw.find_subpath(nm) or f"{args.base}/{nm}"
        ok, pct, report = check_workshop(nm, subpath)
        for ln in report:
            print(ln)
        if ok is False:            # unaccounted content check (not exercised, not excluded)
            any_fail = True

    if any_fail:
        print(f"\n{RED}COVERAGE GAP{RST}: at least one workshop has commands with no smoke test — "
              f"a broken command in that workshop would ship undetected.")
    else:
        print(f"\n{GREEN}all plans cover their workshop content.{RST}")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
