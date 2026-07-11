#!/usr/bin/env python3
"""Run a workshop's smoke test (setup steps + all examiner checks) in its live session.

Reads a smoke plan (JSON) describing the learner flow as an ordered list of
steps, and executes each inside the running session's workshop container — the
same place the Educates examiner runs tests. Reports pass/fail per step.

Plan format (crc-local-testing/smoke-plans/<workshop>.json):
  {
    "steps": [
      {"run":   "oc apply -f service.yaml"},               # shell cmd in ~/exercises
      {"check": "verify-service", "args": ["hello-dcs"]}   # examiner test + args
    ]
  }

`check` steps run /opt/workshop/examiner/tests/<name> <args...> (exit 0 = pass).
`run` steps set up state (deploy, scale, ...) between checks.

--oc-shim installs a tiny `oc`->`kubectl` wrapper on PATH in the pod, so DCS
workshops (which use `oc`) can be smoke-tested on the stock base-environment
before the custom dcs-workshop-base image (with real `oc`) exists. The shim only
covers subcommands kubectl shares; oc-specific ones (oc project/rsh/status) will
still fail — those need the real base image.

Examples:
  ./smoke_test.py lab-a02-kubernetes-essentials --oc-shim
  ./smoke_test.py lab-a01-what-is-dcs
"""
import argparse, json, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
GREEN, RED, DIM, RST = "\033[32m", "\033[31m", "\033[2m", "\033[0m"


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def find_pod(ctx, ns, prefix):
    r = sh(["oc", "--context", ctx, "-n", ns, "get", "pods", "--no-headers",
            "-o", "custom-columns=N:.metadata.name,P:.status.phase"])
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].startswith(prefix) and "-vc" not in parts[0] and parts[1] == "Running":
            return parts[0]
    return None


def pod_exec(ctx, ns, pod, script, timeout):
    return sh(["oc", "--context", ctx, "-n", ns, "exec", pod, "-c", "workshop", "--",
               "bash", "-lc", script], timeout=timeout)


def main():
    p = argparse.ArgumentParser(description="Run a workshop's examiner smoke test in its live session.")
    p.add_argument("name")
    p.add_argument("--id", default="01")
    p.add_argument("--context", default="crc-admin")
    p.add_argument("--plan", default=None, help="default: smoke-plans/<name>.json")
    p.add_argument("--tests-dir", default="/opt/workshop/examiner/tests")
    p.add_argument("--workdir", default="/home/eduk8s/exercises")
    p.add_argument("--oc-shim", action="store_true", help="alias oc->kubectl on PATH in the pod")
    p.add_argument("--timeout", type=int, default=180, help="per-step timeout (s)")
    args = p.parse_args()

    plan_path = pathlib.Path(args.plan) if args.plan else HERE / "smoke-plans" / f"{args.name}.json"
    if not plan_path.exists():
        sys.exit(f"no smoke plan: {plan_path}")
    steps = json.loads(plan_path.read_text()).get("steps", [])

    ns = args.name                                   # env namespace == workshop name
    pod = find_pod(args.context, ns, f"{args.name}-{args.id}")
    if not pod:
        sys.exit(f"no Running session pod for {args.name}-{args.id} in ns {ns} "
                 f"(deploy first: ./deploy_workshop.py {args.name})")
    print(f"session pod: {ns}/{pod}")

    path_prefix = ""
    if args.oc_shim:
        pod_exec(args.context, ns, pod,
                 'mkdir -p $HOME/bin && printf \'#!/bin/sh\\nexec kubectl "$@"\\n\' '
                 '> $HOME/bin/oc && chmod +x $HOME/bin/oc', args.timeout)
        path_prefix = 'export PATH=$HOME/bin:$PATH; '
        print(f"{DIM}oc->kubectl shim installed{RST}")

    passed = failed = 0
    for i, step in enumerate(steps, 1):
        if "run" in step:
            cmd = f'{path_prefix}cd {args.workdir}; {step["run"]}'
            r = pod_exec(args.context, ns, pod, cmd, args.timeout)
            ok = r.returncode == 0
            label = f"run: {step['run']}"
        else:
            name = step["check"]
            argstr = " ".join(f"'{a}'" for a in step.get("args", []))
            r = pod_exec(args.context, ns, pod, f'{path_prefix}{args.tests_dir}/{name} {argstr}', args.timeout)
            ok = r.returncode == 0
            label = f"check: {name} {' '.join(step.get('args', []))}".rstrip()
        passed, failed = (passed + 1, failed) if ok else (passed, failed + 1)
        tag = f"{GREEN}PASS{RST}" if ok else f"{RED}FAIL{RST}"
        print(f"  [{i:>2}] {tag}  {label}")
        if not ok:
            diag = (r.stderr.strip() or r.stdout.strip()).splitlines()
            if diag:
                print(f"        {DIM}{diag[-1]}{RST}")

    print(f"\n{passed} passed, {failed} failed of {passed + failed}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
