#!/usr/bin/env python3
"""End-to-end workshop smoke test: DEPLOY -> run graders -> TEAR DOWN.

Unlike the old script (which assumed a pre-deployed pod and a fixed repo layout),
this owns the whole lifecycle so a single command proves a workshop from scratch:

  1. deploy the workshop to CRC (reuses deploy_workshop.py: git source, portal-less,
     waits for the session to reach Running),
  2. run its smoke plan inside the live session pod — `run` steps set up learner
     state, `check` steps invoke the Educates examiner graders,
  3. optionally link-check the workshop markdown,
  4. tear the workshop down again (unless --keep), so the cluster is left clean.

Nothing is hard-coded to a workshop: the repo path, session namespace, pod name
and content dir are all derived from the workshop name via deploy_workshop's
resolver. Plan lives at smoke-plans/<name>.json:

  { "steps": [ {"run": "oc apply -f service.yaml"},
               {"check": "verify-service", "args": ["hello-dcs"]} ],
    "vcluster": false }

Examples:
  ./smoke_test.py lab-a02-kubernetes-essentials
  ./smoke_test.py lab-a03-namespace-model --keep            # leave it running
  ./smoke_test.py lab-a01-what-is-dcs --no-deploy --no-teardown   # against an existing session
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import time

import deploy_workshop as dw          # reuse resolver + deploy/teardown (same dir)

HERE = pathlib.Path(__file__).resolve().parent
GREEN, RED, DIM, RST = "\033[32m", "\033[31m", "\033[2m", "\033[0m"
LINK_SKIP = ("example.dcs", "example.com", "localhost", ".svc", "apps-crc.testing")


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def run_deploy_tool(name, ctx, sid, vcluster, delete=False):
    """Invoke deploy_workshop.py for the real deploy/teardown (single source of truth)."""
    cmd = [sys.executable, str(HERE / "deploy_workshop.py"), name,
           "--context", ctx, "--id", sid]
    if vcluster:
        cmd.append("--vcluster")
    if delete:
        cmd.append("--delete")
    r = subprocess.run(cmd)
    return r.returncode == 0


def wait_for_pod(ctx, ns, prefix, timeout):
    """Poll for a Running (non-vcluster) session pod; return its name or None."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = sh(["oc", "--context", ctx, "-n", ns, "get", "pods", "--no-headers",
                "-o", "custom-columns=N:.metadata.name,P:.status.phase"])
        for line in r.stdout.splitlines():
            parts = line.split()
            if (len(parts) == 2 and parts[0].startswith(prefix)
                    and "-vc" not in parts[0] and parts[1] == "Running"):
                return parts[0]
        time.sleep(5)
    return None


def pod_exec(ctx, ns, pod, script, timeout):
    return sh(["oc", "--context", ctx, "-n", ns, "exec", pod, "-c", "workshop", "--",
               "bash", "-lc", script], timeout=timeout)


def check_links(content_dir):
    """External http(s) links in the workshop markdown → verify each is reachable."""
    urls = set()
    for f in content_dir.rglob("*.md"):
        for m in re.findall(r'https?://[^\s)>\]"\'`]+', f.read_text()):
            u = m.rstrip('.,;:')
            if "{{<" in u or "$" in u or any(s in u for s in LINK_SKIP):
                continue
            urls.add(u)
    if not urls:
        print("\nlink check: no external links found.")
        return 0
    print(f"\nlink check ({len(urls)} external links):")
    bad = 0
    for u in sorted(urls):
        code = sh(["curl", "-sSL", "-m", "20", "-A", "Mozilla/5.0",
                   "-o", "/dev/null", "-w", "%{http_code}", u]).stdout.strip()
        ok = bool(code) and code[0] in "23"
        bad += 0 if ok else 1
        print(f"  {(GREEN if ok else RED)}{code or 'ERR'}{RST}  {u}")
    return bad


def run_plan(ctx, ns, pod, steps, tests_dir, workdir, oc_shim, timeout):
    """Execute the smoke plan in the pod. Returns (passed, failed)."""
    prefix = ""
    if oc_shim:
        pod_exec(ctx, ns, pod,
                 'mkdir -p $HOME/bin && printf \'#!/bin/sh\\nexec kubectl "$@"\\n\' '
                 '> $HOME/bin/oc && chmod +x $HOME/bin/oc', timeout)
        prefix = 'export PATH=$HOME/bin:$PATH; '
        print(f"{DIM}oc->kubectl shim installed{RST}")

    passed = failed = 0
    for i, step in enumerate(steps, 1):
        if "run" in step:
            r = pod_exec(ctx, ns, pod, f'{prefix}cd {workdir}; {step["run"]}', timeout)
            label = f"run: {step['run']}"
        else:
            argstr = " ".join(f"'{a}'" for a in step.get("args", []))
            r = pod_exec(ctx, ns, pod, f'{prefix}{tests_dir}/{step["check"]} {argstr}', timeout)
            label = f"check: {step['check']} {' '.join(step.get('args', []))}".rstrip()
        ok = r.returncode == 0
        passed, failed = (passed + 1, failed) if ok else (passed, failed + 1)
        print(f"  [{i:>2}] {(GREEN + 'PASS' if ok else RED + 'FAIL')}{RST}  {label}")
        if not ok:
            diag = (r.stderr.strip() or r.stdout.strip()).splitlines()
            if diag:
                print(f"        {DIM}{diag[-1]}{RST}")
    return passed, failed


def main():
    p = argparse.ArgumentParser(description="Deploy a workshop, run its graders, tear it down.")
    p.add_argument("name", help="workshop dir name (e.g. lab-a02-kubernetes-essentials)")
    p.add_argument("--id", default="01")
    p.add_argument("--context", default="crc-admin")
    p.add_argument("--base", default=dw.DEFAULT_BASE, help="repo path prefix of workshops")
    p.add_argument("--plan", default=None, help="default: smoke-plans/<name>.json")
    p.add_argument("--tests-dir", default="/opt/workshop/examiner/tests")
    p.add_argument("--workdir", default="/home/eduk8s/exercises")
    p.add_argument("--oc-shim", action="store_true", help="alias oc->kubectl in the pod")
    p.add_argument("--timeout", type=int, default=180, help="per-step timeout (s)")
    p.add_argument("--deploy-timeout", type=int, default=300, help="wait for session Running (s)")
    p.add_argument("--no-deploy", action="store_true", help="use an already-deployed session")
    p.add_argument("--no-teardown", "--keep", dest="keep", action="store_true",
                   help="leave the workshop running afterwards")
    p.add_argument("--no-links", action="store_true", help="skip external link checking")
    args = p.parse_args()

    # Resolve the workshop's repo subpath (no hard-coded layout).
    targets = dw.resolve_targets(args.name, args.base)
    if not targets:
        sys.exit(f"could not resolve workshop {args.name!r} under {args.base}")
    name, subpath = targets[0]
    ns = name                                    # portal-less deploy: env ns == name
    plan_path = pathlib.Path(args.plan) if args.plan else HERE / "smoke-plans" / f"{name}.json"
    if not plan_path.exists():
        sys.exit(f"no smoke plan: {plan_path}")
    plan = json.loads(plan_path.read_text())
    steps = plan.get("steps", [])
    vcluster = bool(plan.get("vcluster", False))

    # 1. deploy
    if not args.no_deploy:
        print(f"=== deploying {name} (vcluster={vcluster}) ===")
        if not run_deploy_tool(name, args.context, args.id, vcluster):
            sys.exit("deploy failed")

    # 2. find the live session pod
    pod = wait_for_pod(args.context, ns, f"{name}-{args.id}", args.deploy_timeout)
    if not pod:
        if not args.keep:
            run_deploy_tool(name, args.context, args.id, vcluster, delete=True)
        sys.exit(f"no Running session pod for {name}-{args.id} in ns {ns}")
    print(f"session pod: {ns}/{pod}\n")

    # 3. run graders
    passed, failed = run_plan(args.context, ns, pod, steps, args.tests_dir,
                              args.workdir, args.oc_shim, args.timeout)

    # 4. link check
    link_bad = 0
    if not args.no_links:
        cdir = dw.REPO_ROOT / subpath / "workshop" / "content"
        link_bad = check_links(cdir) if cdir.exists() else print(f"\n(no content dir {cdir})") or 0

    print(f"\n{passed} passed, {failed} failed of {passed + failed}"
          + ("" if args.no_links else f"; links: {link_bad} unreachable"))

    # 5. teardown
    if not args.keep:
        print(f"\n=== tearing down {name} ===")
        run_deploy_tool(name, args.context, args.id, vcluster, delete=True)
    else:
        print(f"\n(kept {name} running; remove with ./deploy_workshop.py {name} --delete)")

    sys.exit(1 if (failed or link_bad) else 0)


if __name__ == "__main__":
    main()
