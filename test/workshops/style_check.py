#!/usr/bin/env python3
"""House-style lint for learner-facing text — no cluster, no network.

Errors (exit 1):
  * a complex `terminal:execute` with no collapsed `section:begin` Breakdown after it
    (before the next command or `##` heading) — see the authoring skill's
    content-depth-reference "Every complex command gets a collapsed breakdown"
  * a link to the retired docs.openshift.com (every URL on it 404s)
  * raw `<details>` HTML (Educates' Hugo strips raw HTML; use section:begin)

Warnings (printed, exit 0 unless --strict): the mechanical AI-voice tells from
writing-voice-reference.md — framing phrases, intensifiers, buzzwords, and one-to-three
word paragraphs used as punchlines. A warning is a prompt to re-read the sentence, not
proof: "actually" in "the value actually stored" can be fine. The read-aloud pass in the
review skill finds what a regex cannot.

  ./style_check.py lab-b05-autoscaling
  ./style_check.py --all
  ./style_check.py --all --strict
"""
import argparse
import re
import sys

import deploy_workshop as dw
from link_check import learner_facing_files

RED, YEL, GREEN, DIM, RST = "\033[31m", "\033[33m", "\033[32m", "\033[2m", "\033[0m"

# A command needs a breakdown if it pipes, chains, substitutes, loops, wraps a shell, or
# carries an expression language. Keep in sync with content-depth-reference.md.
COMPLEX = re.compile(r"\||&&|;|\$\(|\b(for|while)\b|\bsh -c\b|\btimeout\b|<<|2>&1|"
                     r"jsonpath=|go-template|custom-columns|--sort-by|\bjq\b|\bawk\b|\bsed\b")
EXEC_FENCE = re.compile(r"^```terminal:execute(-[12])?\s*$")
BOUNDARY = re.compile(r"^(```terminal:execute|## )")

VOICE = [(re.compile(p, re.I), why) for p, why in [
    (r"\b(is|was|that'?s) (the|exactly the) (whole )?point\b|\bthe whole (point|idea|difference|story|trick)\b", "'the point' framing"),
    (r"(^|\. )The (trick|catch|answer|result|twist):", "reveal framing"),
    (r"\bhere'?s the thing\b|\blet'?s dive\b|\bwhich brings us to\b|\bas promised\b", "meta narration"),
    (r"\b(genuinely|actually|simply|really|precisely|effortlessly|for real)\b", "intensifier"),
    (r"\b(seamless(ly)?|robust|powerful|leverag(e|es|ing)|empower\w*|unlock\w*|journey|landscape|"
     r"delve|harness|streamline\w*|elevate|magic(al)?|under the hood|game[- ]changer|"
     r"at its core|in a nutshell|deep dive|first-class)\b", "buzzword"),
]]
FRAGMENT = re.compile(r"^[A-Z*`][^.!?]*[.!]$")


def command_text(lines, i):
    """Command of the fence opening at lines[i] → (text, index of closing fence)."""
    out, j = [], i + 1
    while j < len(lines) and not lines[j].startswith("```"):
        out.append(lines[j])
        j += 1
    body = "\n".join(out)
    m = re.search(r"^command:\s*(?:[|>][-+0-9]*\s*\n)?(.*?)(?=^\w+:|\Z)", body, re.S | re.M)
    return (m.group(1) if m else ""), j


def check_commands(rel, lines):
    errs = []
    for i, ln in enumerate(lines):
        if not EXEC_FENCE.match(ln):
            continue
        cmd, end = command_text(lines, i)
        if not COMPLEX.search(cmd):
            continue
        k, found = end + 1, False
        while k < len(lines) and not BOUNDARY.match(lines[k]):
            if lines[k].strip() == "```section:begin":
                head = "\n".join(lines[k + 1:k + 6])
                if re.search(r"^prefix:\s*Breakdown\s*$", head, re.M):
                    found = True
                    break
            k += 1
        if not found:
            first = cmd.strip().splitlines()[0] if cmd.strip() else ""
            errs.append(f"{rel}:{i + 1}  complex command, no Breakdown section: {first[:90]}")
    return errs


def check_voice(rel, lines, is_md):
    warns, in_fence = [], False
    for i, ln in enumerate(lines):
        if ln.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        text = re.sub(r"`[^`]*`|\]\([^)]*\)|\{\{<[^>]*>\}\}", "", ln)   # code, link targets, shortcodes
        for rx, why in VOICE:
            m = rx.search(text)
            if m:
                warns.append(f"{rel}:{i + 1}  {why}: \"{m.group(0)}\"")
        stripped = ln.strip()
        if (is_md and FRAGMENT.match(stripped) and len(stripped.split()) <= 3
                and (i == 0 or not lines[i - 1].strip())
                and (i + 1 == len(lines) or not lines[i + 1].strip())):
            warns.append(f"{rel}:{i + 1}  punchline fragment paragraph: \"{stripped}\"")
    return warns


def check_lab(subpath):
    root = dw.REPO_ROOT / subpath
    files = learner_facing_files(subpath)
    files += [p for p in (root / "resources").glob("*.yaml") if p not in files]
    errs, warns = [], []
    for f in files:
        rel = f.relative_to(dw.REPO_ROOT)
        text = f.read_text()
        lines = text.splitlines()
        is_md = f.suffix == ".md"
        for i, ln in enumerate(lines):
            if "docs.openshift.com" in ln:
                errs.append(f"{rel}:{i + 1}  docs.openshift.com is retired (404) — use docs.redhat.com")
            if is_md and re.search(r"<details\b", ln, re.I):
                errs.append(f"{rel}:{i + 1}  raw <details> HTML is stripped by Hugo — use section:begin")
        if is_md and "/workshop/content/" in f.as_posix():
            errs += check_commands(rel, lines)
        warns += check_voice(rel, lines, is_md)
    return errs, warns


def main():
    p = argparse.ArgumentParser(description="House-style lint: breakdowns, retired links, AI-voice tells.")
    p.add_argument("name", nargs="?")
    p.add_argument("--all", action="store_true")
    p.add_argument("--strict", action="store_true", help="voice warnings also fail")
    p.add_argument("--quiet", action="store_true", help="errors and per-lab counts only")
    args = p.parse_args()
    labs = dw.all_workshop_paths()
    if args.all:
        names = sorted(labs)
    elif args.name:
        names = [args.name]
    else:
        p.error("a workshop name or --all is required")

    n_err = n_warn = 0
    for nm in names:
        subpath = labs.get(nm) or f"{dw.DEFAULT_BASE}/{nm}"
        errs, warns = check_lab(subpath)
        n_err += len(errs)
        n_warn += len(warns)
        bad = errs or (args.strict and warns)
        tag = f"{RED}FAIL{RST}" if bad else (f"{YEL}WARN{RST}" if warns else f"{GREEN}PASS{RST}")
        print(f"{tag} {nm}: {len(errs)} error(s), {len(warns)} voice warning(s)")
        for e in errs:
            print(f"  {RED}ERR {RST} {e}")
        if not args.quiet:
            for w in warns:
                print(f"  {YEL}warn{RST} {DIM}{w}{RST}")
    print(f"\n{n_err} error(s), {n_warn} voice warning(s) across {len(names)} lab(s)")
    sys.exit(1 if n_err or (args.strict and n_warn) else 0)


if __name__ == "__main__":
    main()
