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
import argparse, json, re, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
GREEN, RED, DIM, RST = "\033[32m", "\033[31m", "\033[2m", "\033[0m"
# hosts to skip in link checking: placeholders, in-cluster/demo hosts, session routes
LINK_SKIP = ("example.dcs", "example.com", "localhost", ".svc", "apps-crc.testing")


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def check_links(content_dir):
    """Extract external http(s) links from workshop markdown and verify each is reachable."""
    urls = set()
    for f in content_dir.rglob("*.md"):
        for m in re.findall(r'https?://[^\s)>\]"\'`]+', f.read_text()):
            u = m.rstrip('.,;:')
            if "{{<" in u or "$" in u:                 # unrendered param / shell var
                continue
            if any(s in u for s in LINK_SKIP):          # placeholder / non-public
                continue
            urls.add(u)
    print(f"\nlink check ({len(urls)} external links):")
    bad = 0
    for u in sorted(urls):
        code = sh(["curl", "-sSL", "-m", "20", "-A", "Mozilla/5.0",
                   "-o", "/dev/null", "-w", "%{http_code}", u]).stdout.strip()
        ok = bool(code) and code[0] in "23"             # 2xx/3xx = reachable
        bad += 0 if ok else 1
        tag = f"{GREEN}{code or 'ERR'}{RST}" if ok else f"{RED}{code or 'ERR'}{RST}"
        print(f"  {tag}  {u}")
    return bad


def restart_session(ctx, name, sid):
    """Delete + recreate the WorkshopSession so the next user starts clean."""
    sn = f"{name}-w{sid}"
    sh(["oc", "--context", ctx, "delete", "workshopsession", sn, "--ignore-not-found", "--wait=true"])
    sh(["oc", "--context", ctx, "apply", "-f", "-"], input=json.dumps({
        "apiVersion": "training.educates.dev/v1beta1", "kind": "WorkshopSession",
        "metadata": {"name": sn},
        "spec": {"environment": {"name": name},
                 "session": {"id": sid, "username": "educates", "password": "educates"}}}))


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
    p.add_argument("--content-base", default=str(HERE.parent / "dcs-academy" / "workshops"),
                   help="repo path holding <workshop>/workshop/content for link checking")
    p.add_argument("--no-links", action="store_true", help="skip external link checking")
    p.add_argument("--no-restart", action="store_true", help="don't restart the session at the end")
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

    link_bad = 0
    if not args.no_links:
        cdir = pathlib.Path(args.content_base) / args.name / "workshop" / "content"
        if cdir.exists():
            link_bad = check_links(cdir)
        else:
            print(f"\n(no content dir {cdir}; skipping link check)")

    summary = f"\n{passed} passed, {failed} failed of {passed + failed}"
    if not args.no_links:
        summary += f"; links: {link_bad} unreachable"
    print(summary)

    if not args.no_restart:
        print("\nrestarting session for a clean start...")
        restart_session(args.context, args.name, args.id)
        print(f"session {args.name}-w{args.id} recreated (fresh).")

    sys.exit(1 if (failed or link_bad) else 0)


if __name__ == "__main__":
    main()
