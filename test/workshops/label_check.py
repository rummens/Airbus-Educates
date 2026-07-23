#!/usr/bin/env python3
"""Verify every workshop declares the DCS lifecycle label correctly — WITHOUT a cluster.

Each Workshop CR must carry `dcs.airbus.com/lifecycle` on metadata.labels, set to `dev`
or `prod`. The rule that makes it meaningful (and self-maintaining — no hardcoded lab
list): a lab must be `prod` exactly when it creates a Route/Ingress, because DCS only
admits external exposure in a PROD-type namespace. Everything else is `dev`.

This catches the two regressions the label is there to prevent: a lab that exposes a Route
but is still marked `dev` (would be rejected on a PROD-enforcing platform), and a lab left
`prod` with nothing to expose (over-privileged intent).

NOTE: this checks the label on the Workshop CR. Propagating it onto the live session
namespace needs a platform mechanism (the portal chart's Kyverno policy is off on
OpenShift) — that runtime step is out of scope here and validated on the platform.

  ./label_check.py lab-a03-expose-app
  ./label_check.py --all
"""
import argparse
import pathlib
import re
import sys

import deploy_workshop as dw          # resolver + REPO_ROOT (same dir)

GREEN, RED, YEL, DIM, RST = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"

LIFECYCLE_RE = re.compile(r'dcs\.airbus\.com/lifecycle:\s*["\']?([A-Za-z0-9_-]+)')
ROUTE_RE = re.compile(r"kind:\s*Route\b|route\.openshift\.io", re.IGNORECASE)
VALID = {"dev", "prod"}


def lab_creates_route(lab_dir):
    """True if the lab provisions a Route/Ingress anywhere (workshop.yaml objects,
    exercise manifests, or content that applies one)."""
    for f in lab_dir.rglob("*"):
        if f.suffix.lower() in {".yaml", ".yml", ".md"} and f.is_file():
            if ROUTE_RE.search(f.read_text(errors="ignore")):
                return True
    return False


def check_lab(name, subpath):
    lab_dir = dw.REPO_ROOT / subpath
    ws = lab_dir / "resources" / "workshop.yaml"
    if not ws.exists():
        return [f"{RED}FAIL{RST} {name}: no resources/workshop.yaml"]
    m = LIFECYCLE_RE.search(ws.read_text())
    label = m.group(1) if m else None
    route = lab_creates_route(lab_dir)
    expected = "prod" if route else "dev"

    errs = []
    if label is None:
        errs.append(f"{RED}FAIL{RST} {name}: missing dcs.airbus.com/lifecycle label "
                    f"(expected '{expected}')")
    elif label not in VALID:
        errs.append(f"{RED}FAIL{RST} {name}: lifecycle '{label}' not in {sorted(VALID)}")
    elif route and label != "prod":
        errs.append(f"{RED}FAIL{RST} {name}: creates a Route but is marked '{label}' — "
                    f"external exposure needs 'prod'")
    elif not route and label == "prod":
        errs.append(f"{YEL}WARN{RST} {name}: marked 'prod' but creates no Route — "
                    f"should this be 'dev'?")
    else:
        print(f"{GREEN}OK{RST}   {name}: lifecycle={label} "
              f"{DIM}(route={'yes' if route else 'no'}){RST}")
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="*", help="workshop dir names (default: --all)")
    ap.add_argument("--all", action="store_true", help="check every workshop in the monorepo")
    args = ap.parse_args()

    paths = dw.all_workshop_paths()
    if args.all or not args.names:
        targets = sorted(paths.items())
    else:
        targets = [(n, paths[n]) for n in args.names if n in paths]
        missing = [n for n in args.names if n not in paths]
        for n in missing:
            print(f"{RED}FAIL{RST} {n}: not found in any track")
        if missing:
            sys.exit(1)

    errors = []
    for name, subpath in targets:
        errors.extend(check_lab(name, pathlib.Path(subpath)))

    fails = [e for e in errors if "FAIL" in e]
    for e in errors:
        print(e)
    if fails:
        print(f"\n{RED}{len(fails)} lifecycle-label problem(s).{RST}")
        sys.exit(1)
    print(f"\n{GREEN}All lifecycle labels correct.{RST}")


if __name__ == "__main__":
    main()
