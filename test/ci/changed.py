#!/usr/bin/env python3
"""Compute what changed between a base ref and HEAD, so CI only runs the relevant tests.

Emits shell-evalable lines:

    PYTHON=1                       # portal source or python tests changed
    WORKSHOPS="lab-a02-... lab-b04-..."   # workshop dirs that changed (space-separated)

Base ref precedence: $1 arg → $CI_MERGE_REQUEST_DIFF_BASE_SHA → $CI_COMMIT_BEFORE_SHA →
origin/main. If none resolves (e.g. shallow clone), falls back to the working-tree diff
(git status), which is what you want locally.

    eval "$(python3 test/ci/changed.py)"
    python3 test/ci/changed.py origin/main
"""
import os
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True).stdout.strip() or ".")
PYTHON_GLOBS = (re.compile(r"^images/dcs-academy-portal/"),
                re.compile(r"^test/portal/"),
                re.compile(r"^test/workshops/.*\.py$"),
                re.compile(r"^test/ci/"))
WORKSHOP_RE = re.compile(r"^workshops-monorepo/tracks/[^/]+/(lab-[^/]+)/")
# a change to the shared harness or plans affects every workshop's tests
HARNESS_RE = re.compile(r"^test/workshops/(.*\.py|smoke-plans/.*)$")


def _run(*a):
    return subprocess.run(a, capture_output=True, text=True, cwd=str(REPO)).stdout


def base_ref(argv):
    for c in (argv[1] if len(argv) > 1 else None,
              os.environ.get("CI_MERGE_REQUEST_DIFF_BASE_SHA"),
              os.environ.get("CI_COMMIT_BEFORE_SHA"),
              "origin/main"):
        if c and subprocess.run(["git", "rev-parse", "--verify", "--quiet", c],
                                cwd=str(REPO), capture_output=True).returncode == 0:
            return c
    return None


def changed_files(argv):
    ref = base_ref(argv)
    if ref:
        out = _run("git", "diff", "--name-only", f"{ref}...HEAD")
        names = [l for l in out.splitlines() if l.strip()]
        if names:
            return names, ref
    # fallback: uncommitted working-tree changes (local use)
    out = _run("git", "status", "--porcelain")
    return [l[3:] for l in out.splitlines() if l.strip()], "working-tree"


def main():
    files, ref = changed_files(sys.argv)
    python = any(g.search(f) for f in files for g in PYTHON_GLOBS)
    harness = any(HARNESS_RE.search(f) for f in files)

    if harness:
        # shared test code/plans changed → re-test every workshop that has a plan
        plans = (REPO / "test" / "workshops" / "smoke-plans")
        workshops = sorted(p.stem for p in plans.glob("*.json")) if plans.is_dir() else []
    else:
        workshops = sorted({m.group(1) for f in files if (m := WORKSHOP_RE.search(f))})

    sys.stderr.write(f"# base ref: {ref}; {len(files)} files changed\n")
    print(f"PYTHON={1 if python else 0}")
    print(f'WORKSHOPS="{" ".join(workshops)}"')


if __name__ == "__main__":
    main()
