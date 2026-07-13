#!/usr/bin/env python3
"""User-flow test: spin up a REAL session, prove it works, tear it down.

This is the "does a learner actually get a working environment" test, run end-to-end
against a live cluster. For each variant it:

  1. deploys a workshop session (reuses deploy_workshop.py — the same CR path the portal
     drives; portal-less because the Educates portal SIGILLs on CRC arm64, see README),
  2. waits for the session pod to reach Running,
  3. verifies the session is reachable over HTTP — the dashboard AND the editor answer 200
     (this is the "content loads" step a learner sees in the browser),
  4. runs basic commands in the session terminal and asserts they succeed — identity,
     namespace access, and a write (create + read back a ConfigMap),
  5. tears the session down.

Two variants, matching the two run-locations a workshop can choose (see the house
"vcluster vs namespace" standard):

  * namespace — the session works inside one OpenShift namespace (default lab: a02).
  * vcluster  — the session gets its own virtual cluster (default lab: a03); additionally
                asserts cluster-scoped power the namespace variant must NOT have
                (`oc get nodes`), proving the vcluster is really isolated.

  ./flow_test.py                       # both variants, default labs
  ./flow_test.py --mode namespace
  ./flow_test.py --mode vcluster --workshop lab-a03-namespace-model
  ./flow_test.py --keep                # leave sessions up to inspect

Final setup runs on x86 where the real portal works; there the same session mechanics
front the portal login → catalog → launch flow. On CRC this drives them portal-less.
"""
import argparse
import sys

import deploy_workshop as dw
import smoke_test as st                     # reuse wait_for_pod / pod_exec / sh / run_deploy_tool

GREEN, RED, DIM, BOLD, RST = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"

DEFAULT_LAB = {"namespace": "lab-a02-kubernetes-essentials",
               "vcluster": "lab-a03-namespace-model"}

# (label, script, must_succeed). must_succeed=False → we assert it FAILS (negative check).
BASIC_CMDS = [
    ("identity: oc whoami", "oc whoami", True),
    ("client: oc version", "oc version --client=false -o json >/dev/null 2>&1 || oc version", True),
    ("namespace access: oc get pods", "oc get pods", True),
    ("write: create+read a ConfigMap",
     "oc create configmap flowtest --from-literal=k=v --dry-run=client -o yaml | oc apply -f - "
     "&& oc get configmap flowtest -o jsonpath='{.data.k}' | grep -qx v", True),
]


def http_code(url, ctx=None):
    return st.sh(["curl", "-sk", "-m", "10", "-o", "/dev/null", "-w", "%{http_code}",
                  "-u", "educates:educates", url]).stdout.strip()


def session_url(ctx, session_name):
    r = st.sh(["oc", "--context", ctx, "get", "workshopsession", session_name,
               "-o", "jsonpath={.status.educates.url}"])
    return r.stdout.strip()


def run_variant(mode, workshop, ctx, sid, keep, timeout):
    vcluster = (mode == "vcluster")
    ns = workshop
    session_name = f"{workshop}-w{sid}"
    print(f"\n{BOLD}=== flow: {mode} — {workshop} ==={RST}")

    ok = True
    fails = []

    # 1. deploy
    if not st.run_deploy_tool(workshop, ctx, sid, vcluster):
        return False, [f"deploy failed for {workshop} ({mode})"]

    # 2. session pod Running
    pod = st.wait_for_pod(ctx, ns, f"{workshop}-{sid}", timeout)
    if not pod:
        if not keep:
            st.run_deploy_tool(workshop, ctx, sid, vcluster, delete=True)
        return False, [f"no Running session pod for {session_name}"]
    print(f"  {GREEN}PASS{RST}  session pod Running: {ns}/{pod}")

    # 3. HTTP reachability — dashboard + editor answer (content loads)
    url = session_url(ctx, session_name)
    if not url:
        ok = False; fails.append("session has no status.educates.url")
    else:
        for label, u in [("dashboard", url),
                         ("editor", url.replace("https://", "https://editor-", 1))]:
            code = http_code(u)
            good = code == "200"
            ok &= good
            print(f"  {(GREEN+'PASS' if good else RED+'FAIL')}{RST}  {label} HTTP {code or 'ERR'}  {DIM}{u}{RST}")
            if not good:
                fails.append(f"{label} not reachable (HTTP {code or 'ERR'}) at {u}")

    # 4. basic commands in the terminal
    cmds = list(BASIC_CMDS)
    if vcluster:
        cmds.append(("vcluster is cluster-scoped: oc get nodes", "oc get nodes", True))
    else:
        cmds.append(("namespace is NOT cluster-scoped: oc get nodes denied",
                     "oc get nodes", False))
    for label, script, want_ok in cmds:
        r = st.pod_exec(ctx, ns, pod, script, timeout)
        got_ok = r.returncode == 0
        good = got_ok == want_ok
        ok &= good
        verdict = GREEN + "PASS" if good else RED + "FAIL"
        print(f"  {verdict}{RST}  {label}")
        if not good:
            diag = (r.stderr.strip() or r.stdout.strip()).splitlines()
            fails.append(f"{label}: expected {'success' if want_ok else 'failure'}, "
                         f"got rc={r.returncode}" + (f" — {diag[-1]}" if diag else ""))

    # 5. teardown
    if not keep:
        st.run_deploy_tool(workshop, ctx, sid, vcluster, delete=True)
        print(f"  {DIM}torn down{RST}")
    else:
        print(f"  {DIM}kept running; remove with ./deploy_workshop.py {workshop} "
              f"{'--vcluster ' if vcluster else ''}--delete{RST}")
    return ok, fails


def main():
    p = argparse.ArgumentParser(description="End-to-end user-flow test against a live cluster.")
    p.add_argument("--mode", choices=["namespace", "vcluster", "both"], default="both")
    p.add_argument("--workshop", default=None, help="override the lab for the chosen mode")
    p.add_argument("--id", default="90")            # high id to avoid clashing with manual sessions
    p.add_argument("--context", default="crc-admin")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--keep", action="store_true", help="leave sessions running afterwards")
    args = p.parse_args()

    modes = ["namespace", "vcluster"] if args.mode == "both" else [args.mode]
    results = {}
    for mode in modes:
        workshop = args.workshop or DEFAULT_LAB[mode]
        if not dw.find_subpath(workshop):
            print(f"{RED}unknown workshop {workshop!r}{RST}")
            results[mode] = (False, [f"workshop {workshop} not found in repo"])
            continue
        results[mode] = run_variant(mode, workshop, args.context, args.id, args.keep, args.timeout)

    print(f"\n{BOLD}=== flow summary ==={RST}")
    all_ok = True
    for mode, (ok, fails) in results.items():
        all_ok &= ok
        print(f"  {(GREEN+'PASS' if ok else RED+'FAIL')}{RST}  {mode}")
        for fmsg in fails:
            print(f"        {RED}cost:{RST} {fmsg}")
    if not all_ok:
        print(f"\n{RED}A learner in the failing variant would NOT get a working environment.{RST}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
