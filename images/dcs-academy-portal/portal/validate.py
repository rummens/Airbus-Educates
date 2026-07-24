"""Post-sync validation gate: assert live WorkshopEnvironments match the catalog.

Educates' training-portal reconciles WorkshopEnvironments by create/delete only — never
an in-place update — so a rolled workshop can end up with NO healthy env, and 'start'
403s while Argo still reports the app green (envs are portal-created, invisible to Argo's
health assessment). This runs as an ArgoCD PostSync hook AFTER the env reaper: it polls
until every workshop in TrainingPortal.spec.workshops has exactly one Running,
non-terminating WorkshopEnvironment (and the portal itself is Running). If the deadline
passes with anything missing/broken it exits non-zero → the hook fails → Argo marks the
Application Degraded and retries. VALIDATE_MODE=warn logs the same report but exits 0.

Env vars:
  EDUCATES_PORTAL_NAME       which portal to check (required; scopes every read)
  VALIDATE_MODE              fail (default) | warn
  VALIDATE_SETTLE_SECONDS    max time to wait for envs to converge (default 240)
  VALIDATE_POLL_SECONDS      poll interval (default 10)
  VALIDATE_READY_PHASES      comma list of env phases counted ready (default "Running")
"""
import logging
import os
import time

from . import config as cfg
from . import k8sclient
from .reap import _portal_of, _phase, _ws_of, _env_of

log = logging.getLogger("portal.validate")


def assess(desired_names, envs, sessions, portal_phase, ready_phases):
    """Pure decision core (unit-testable). Returns (ok, report) where report is
    {portal_ok, workshops: {name: {ready, envs, reason}}, extra_envs: [...]}.

    A workshop is OK iff it has >=1 non-terminating env that is either in a ready phase
    OR already backs a live (non-terminating) session — the session fallback avoids a
    false failure when a functioning env reports a phase string this gate doesn't know."""
    live_envs = [e for e in envs if not (e.get("metadata", {}) or {}).get("deletionTimestamp")]
    # env-name -> True if it backs any live session (reserved/allocated/etc.)
    backed = set()
    for s in sessions:
        if _phase(s) not in ("", "Stopped", "Stopping"):
            backed.add(_env_of(s))

    by_ws = {}
    for e in live_envs:
        by_ws.setdefault(_ws_of(e), []).append(e)

    workshops, all_ok = {}, True
    for ws in sorted(desired_names):
        cands = by_ws.get(ws, [])
        ready = [e for e in cands
                 if _phase(e) in ready_phases
                 or (e.get("metadata", {}) or {}).get("name") in backed]
        ok = len(ready) >= 1
        all_ok = all_ok and ok
        if not cands:
            reason = "no WorkshopEnvironment"
        elif not ready:
            reason = "env(s) present but none ready (phases: %s)" % (
                ", ".join(sorted(_phase(e) or "?" for e in cands)))
        elif len(ready) > 1:
            reason = "%d ready envs (reaper should leave one)" % len(ready)
        else:
            reason = "ok"
        workshops[ws] = {"ready": ok, "envs": len(cands), "reason": reason}

    served = set(desired_names)
    extra = sorted({_ws_of(e) for e in live_envs if _ws_of(e) and _ws_of(e) not in served})
    portal_ok = portal_phase == "Running"
    return (all_ok and portal_ok), {"portal_ok": portal_ok, "portal_phase": portal_phase,
                                    "workshops": workshops, "extra_envs": extra}


def _report(rep):
    log.info("portal phase=%r ok=%s", rep["portal_phase"], rep["portal_ok"])
    for ws, r in rep["workshops"].items():
        log.info("  %-40s %s (%d env) %s", ws, "READY" if r["ready"] else "MISSING",
                 r["envs"], "" if r["reason"] == "ok" else "— " + r["reason"])
    if rep["extra_envs"]:
        log.info("  note: envs for non-catalog workshops (reaper will drain): %s", rep["extra_envs"])


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    portal = cfg.PORTAL_NAME
    if not portal:
        log.error("EDUCATES_PORTAL_NAME unset — cannot scope validation.")
        raise SystemExit(2)
    mode = os.environ.get("VALIDATE_MODE", "fail").lower()
    settle = int(os.environ.get("VALIDATE_SETTLE_SECONDS", "240") or 240)
    poll = int(os.environ.get("VALIDATE_POLL_SECONDS", "10") or 10)
    ready_phases = {p.strip() for p in os.environ.get("VALIDATE_READY_PHASES", "Running").split(",") if p.strip()}

    desired = k8sclient.trainingportal_workshops()
    if not desired:
        log.error("TrainingPortal %r has no readable spec.workshops — nothing to validate "
                  "(is the portal synced yet?).", portal)
        raise SystemExit(2 if mode == "fail" else 0)

    deadline = time.time() + settle
    ok, rep = False, {}
    while True:
        envs = [e for e in k8sclient.list_environments() if _portal_of(e) == portal]
        sessions = [s for s in k8sclient.list_sessions() if _portal_of(s) == portal]
        try:
            portal_phase = (k8sclient.portal_status() or {}).get("phase", "")
        except Exception as e:                          # noqa: BLE001
            portal_phase = ""
            log.warning("could not read portal status: %s", e)
        ok, rep = assess(desired, envs, sessions, portal_phase, ready_phases)
        if ok or time.time() >= deadline:
            break
        missing = [w for w, r in rep["workshops"].items() if not r["ready"]]
        log.info("waiting for convergence: %d/%d workshops ready, missing=%s (%.0fs left)",
                 len(desired) - len(missing), len(desired), missing, deadline - time.time())
        time.sleep(poll)

    _report(rep)
    if ok:
        log.info("validation PASS: all %d workshops have a ready environment.", len(desired))
        return
    if mode == "warn":
        log.warning("validation FAILED but VALIDATE_MODE=warn — exiting 0 (Argo stays green).")
        return
    raise SystemExit("validation FAILED: catalog workshops without a ready environment "
                     "(Argo sync will be marked failed and retried).")


def demo():
    # ponytail: one runnable check for the gate's decision core — no cluster.
    def env(name, ws, phase="Running", terminating=False):
        md = {"name": name}
        if terminating:
            md["deletionTimestamp"] = "2020-01-01T00:00:00Z"
        return {"metadata": md, "spec": {"workshop": {"name": ws}},
                "status": {"educates": {"phase": phase}}}
    def sess(env_name, phase="Reserved"):
        return {"spec": {"environment": {"name": env_name}}, "status": {"educates": {"phase": phase}}}
    desired = {"lab-a", "lab-b", "lab-c"}
    envs = [
        env("e-a", "lab-a"),                              # ready via phase
        env("e-b", "lab-b", phase="Provisioning"),       # not ready by phase...
        env("e-c-old", "lab-c", terminating=True),       # ignored (terminating) -> lab-c missing
    ]
    sessions = [sess("e-b", "Reserved")]                 # ...but backed by a live session -> ready
    ok, rep = assess(desired, envs, sessions, "Running", {"Running"})
    assert not ok, rep
    assert rep["workshops"]["lab-a"]["ready"] and rep["workshops"]["lab-b"]["ready"]
    assert not rep["workshops"]["lab-c"]["ready"], rep
    # once lab-c gets a ready env and portal is Running → pass
    envs.append(env("e-c", "lab-c"))
    ok2, _ = assess(desired, envs, sessions, "Running", {"Running"})
    assert ok2
    # portal not Running fails even with all envs ready
    ok3, _ = assess(desired, envs, sessions, "Pending", {"Running"})
    assert not ok3
    print("validate.demo OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
