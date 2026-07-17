"""Reap orphaned WorkshopSession CRs.

Two events leave sessions whose per-session OAuth2 client is dead, so re-opening the
session host yields django-oauth-toolkit's "invalid_request Invalid client_id":

  * workshop rollout — with `portal.updates.workshop: true` Educates rolls the workshop
    environment; the old WorkshopEnvironment is deleted and its sessions are left behind.
  * training-portal restart — the portal's DB (session records + OAuth2 clients) is
    ephemeral in-pod SQLite, so a restart forgets every session; the CRs + pods linger,
    leaking capacity the (wiped) DB can no longer reap.

This reaper runs as a CronJob and DELETES the orphaned WorkshopSession CRs (the operator
then GCs the session namespace/pods). Deleting the CR works even when the robot-authed
terminate can't, because it needs no DB record.

Detection is deliberately conservative — it never touches a healthy, current session:
  * env-orphan  — the session's WorkshopEnvironment no longer exists / is terminating.
                  Immediate signal for the rollout case (past a short grace).
  * age-backstop — an *Allocated* session older than a hard cap well above any workshop's
                  `expires`. A live session can't outlive `expires`, so beyond the cap it
                  is a leaked orphan (the restart case). Reserved/spare sessions on a live
                  env are exempt so the pool isn't churned.
"""
import logging
import os
import time
from datetime import datetime

from . import config as cfg
from . import k8sclient

log = logging.getLogger("portal.reap")

PORTAL_LABEL = "training.educates.dev/portal.name"


def _portal_of(cr):
    return ((cr.get("metadata", {}) or {}).get("labels", {}) or {}).get(PORTAL_LABEL)


def _phase(s):
    st = s.get("status", {}) or {}
    return (st.get("educates", {}) or {}).get("phase") or st.get("phase") or ""


def _env_of(s):
    return ((s.get("spec", {}) or {}).get("environment", {}) or {}).get("name", "")


def _epoch(ts):
    """RFC3339 (…Z) → epoch seconds; None if unparseable."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def find_orphans(sessions, live_env_names, now, max_alloc_age_s, grace_s):
    """Return [(name, reason)] for sessions that should be reaped.

    `live_env_names`: names of WorkshopEnvironments that exist and are NOT terminating.
    A session younger than `grace_s` is never reaped (still provisioning)."""
    out = []
    for s in sessions:
        name = (s.get("metadata", {}) or {}).get("name", "")
        if not name:
            continue
        created = _epoch((s.get("metadata", {}) or {}).get("creationTimestamp"))
        age = (now - created) if created is not None else 0
        if age < grace_s:
            continue                                   # too new to judge
        env = _env_of(s)
        if env not in live_env_names:
            out.append((name, f"environment {env!r} gone/terminating"))
        elif _phase(s) == "Allocated" and age > max_alloc_age_s:
            out.append((name, f"Allocated for {int(age)}s > backstop {max_alloc_age_s}s "
                              f"(portal DB likely lost it on a restart)"))
    return out


def _int_env(key, default):
    try:
        return int(os.environ.get(key, "") or default)
    except ValueError:
        return default


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    portal = cfg.PORTAL_NAME
    if not portal:
        log.error("EDUCATES_PORTAL_NAME unset — refusing to reap (can't scope to our portal).")
        raise SystemExit(2)

    dry = (os.environ.get("REAPER_DRY_RUN", "false").lower() in ("1", "true", "yes"))
    grace = _int_env("REAPER_GRACE_SECONDS", 300)
    max_alloc = _int_env("REAPER_MAX_ALLOCATED_SECONDS", 24 * 3600)
    now = time.time()

    live = {(e.get("metadata", {}) or {}).get("name")
            for e in k8sclient.list_environments()
            if not (e.get("metadata", {}) or {}).get("deletionTimestamp")}
    # Only ever consider sessions positively attributed to OUR portal (unlabelled or
    # other-portal sessions are left alone — a wrong label key makes us no-op, not
    # delete the wrong thing).
    ours = [s for s in k8sclient.list_sessions() if _portal_of(s) == portal]
    orphans = find_orphans(ours, live, now, max_alloc, grace)

    log.info("reaper: portal=%s live_envs=%d our_sessions=%d orphans=%d dry_run=%s",
             portal, len(live), len(ours), len(orphans), dry)
    reaped = 0
    for name, reason in orphans:
        if dry:
            log.info("would reap %s (%s)", name, reason)
            continue
        try:
            k8sclient.delete_session(name)
            reaped += 1
            log.info("reaped %s (%s)", name, reason)
        except Exception as e:                          # noqa: BLE001
            log.warning("failed to reap %s: %s", name, e)
    log.info("reaper done: %d orphan(s), %d reaped%s",
             len(orphans), reaped, " (dry-run)" if dry else "")


def demo():
    # ponytail: one runnable check for the orphan logic — no cluster.
    now = 1_000_000.0
    def sess(name, env, phase, age):
        return {"metadata": {"name": name,
                             "creationTimestamp":
                                 datetime.utcfromtimestamp(now - age).strftime("%Y-%m-%dT%H:%M:%SZ")},
                "spec": {"environment": {"name": env}},
                "status": {"educates": {"phase": phase}}}
    live = {"env-current"}
    sessions = [
        sess("healthy", "env-current", "Allocated", 600),        # keep: live env, young
        sess("reserved-old", "env-current", "Available", 99999), # keep: spare on live env (not Allocated)
        sess("rollout-orphan", "env-old", "Allocated", 600),     # reap: env gone
        sess("just-born", "env-old", "Allocated", 10),           # keep: within grace
        sess("restart-orphan", "env-current", "Allocated", 90000),  # reap: allocated past 24h backstop
    ]
    got = {n for n, _ in find_orphans(sessions, live, now, max_alloc_age_s=24 * 3600, grace_s=300)}
    assert got == {"rollout-orphan", "restart-orphan"}, got
    print("reap.demo OK:", got)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
