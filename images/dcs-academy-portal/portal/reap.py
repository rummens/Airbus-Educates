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


def _ws_of(env):
    return ((env.get("spec", {}) or {}).get("workshop", {}) or {}).get("name", "")


def _epoch(ts):
    """RFC3339 (…Z) → epoch seconds; None if unparseable."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def classify(sessions, live_env_names, now, max_alloc_age_s, grace_s):
    """Judge every session → list of rows {name, phase, env, env_live, age_s, decision,
    reason}. `decision` is "reap" or "keep". This is the single source of truth for both
    the reap list (find_orphans) and the REAPER_DEBUG dump, so what you see logged is
    exactly what drives the delete."""
    rows = []
    for s in sessions:
        md = s.get("metadata", {}) or {}
        name = md.get("name", "")
        if not name:
            continue
        created = _epoch(md.get("creationTimestamp"))
        age = (now - created) if created is not None else 0
        env = _env_of(s)
        env_live = env in live_env_names
        phase = _phase(s)
        row = {"name": name, "phase": phase, "env": env, "env_live": env_live,
               "age_s": int(age)}
        if age < grace_s:
            row["decision"], row["reason"] = "keep", f"within grace ({grace_s}s)"
        elif not env_live:
            row["decision"], row["reason"] = "reap", f"environment {env!r} gone/terminating"
        elif phase == "Allocated" and age > max_alloc_age_s:
            row["decision"], row["reason"] = "reap", (
                f"Allocated {int(age)}s > backstop {max_alloc_age_s}s "
                f"(portal DB likely lost it on a restart)")
        else:
            row["decision"], row["reason"] = "keep", (
                f"live env, phase={phase!r}, age={int(age)}s < backstop {max_alloc_age_s}s")
        rows.append(row)
    return rows


def find_orphans(sessions, live_env_names, now, max_alloc_age_s, grace_s):
    """Return [(name, reason)] for sessions that should be reaped.

    `live_env_names`: names of WorkshopEnvironments that exist and are NOT terminating.
    A session younger than `grace_s` is never reaped (still provisioning)."""
    return [(r["name"], r["reason"])
            for r in classify(sessions, live_env_names, now, max_alloc_age_s, grace_s)
            if r["decision"] == "reap"]


def classify_environments(envs, desired_names, active_by_env, now, grace_s):
    """Judge each WorkshopEnvironment → rows {name, workshop, phase, age_s, active,
    decision, reason}. `decision` is "reap" or "keep" — the single source of truth for
    both the reap list and the debug dump.

    An env is STALE when its workshop was dropped from the catalog, or it's an older
    duplicate for a workshop that already has a newer env (the create/delete-only portal
    leaves these behind on a workshop roll). Reaping is DRAIN-SAFE: a stale env is only
    deleted once it has zero Allocated sessions and is past the provisioning grace; one
    still serving learners is kept (logged as draining) until they finish. Envs already
    terminating are skipped."""
    live = [e for e in envs if not (e.get("metadata", {}) or {}).get("deletionTimestamp")]
    # winner per workshop = newest live env; older envs for the same workshop are dupes.
    newest = {}
    for e in live:
        ws, md = _ws_of(e), (e.get("metadata", {}) or {})
        c = _epoch(md.get("creationTimestamp")) or 0
        if ws and (ws not in newest or c > newest[ws][1]):
            newest[ws] = (md.get("name"), c)
    keep_names = {v[0] for v in newest.values()}

    rows = []
    for e in live:
        md = e.get("metadata", {}) or {}
        name = md.get("name", "")
        if not name:
            continue
        ws = _ws_of(e)
        created = _epoch(md.get("creationTimestamp"))
        age = (now - created) if created is not None else 0
        active = active_by_env.get(name, 0)
        row = {"name": name, "workshop": ws, "phase": _phase(e),
               "age_s": int(age), "active": active}
        current = ws in desired_names and name in keep_names
        if current:
            row["decision"], row["reason"] = "keep", "current env for a live workshop"
        elif age < grace_s:
            row["decision"], row["reason"] = "keep", f"stale but within grace ({grace_s}s)"
        else:
            why = "workshop dropped from catalog" if ws not in desired_names else "superseded by a newer env"
            if active > 0:
                row["decision"], row["reason"] = "keep", f"stale ({why}) but draining — {active} active session(s)"
            else:
                row["decision"], row["reason"] = "reap", f"{why}, 0 active sessions"
        rows.append(row)
    return rows


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
    debug = (os.environ.get("REAPER_DEBUG", "false").lower() in ("1", "true", "yes"))
    if debug:
        log.setLevel(logging.DEBUG)
    grace = _int_env("REAPER_GRACE_SECONDS", 300)
    max_alloc = _int_env("REAPER_MAX_ALLOCATED_SECONDS", 24 * 3600)
    now = time.time()

    envs = k8sclient.list_environments()
    live = {(e.get("metadata", {}) or {}).get("name")
            for e in envs
            if not (e.get("metadata", {}) or {}).get("deletionTimestamp")}
    all_sessions = k8sclient.list_sessions()
    # Only ever consider sessions positively attributed to OUR portal (unlabelled or
    # other-portal sessions are left alone — a wrong label key makes us no-op, not
    # delete the wrong thing).
    ours = [s for s in all_sessions if _portal_of(s) == portal]
    rows = classify(ours, live, now, max_alloc, grace)
    orphans = [(r["name"], r["reason"]) for r in rows if r["decision"] == "reap"]

    log.info("reaper: portal=%s envs=%d live_envs=%d all_sessions=%d our_sessions=%d "
             "orphans=%d dry_run=%s debug=%s",
             portal, len(envs), len(live), len(all_sessions), len(ours),
             len(orphans), dry, debug)

    if debug:
        # Why is a session kept/reaped? Log the decision inputs for every one of OUR
        # sessions, plus the full status.educates block — so "reaper thinks a dead
        # session is live" can be traced to the exact phase / env / age it saw.
        log.info("DEBUG live_env_names=%s", sorted(n for n in live if n))
        # Portal attribution across ALL sessions (spot a wrong/absent portal label).
        seen_portals = sorted({_portal_of(s) for s in all_sessions}, key=lambda x: (x is None, x))
        log.info("DEBUG portal labels seen on sessions: %s (matching %r)", seen_portals, portal)
        by_name = {(s.get("metadata", {}) or {}).get("name"): s for s in ours}
        for r in rows:
            ed = (by_name.get(r["name"], {}).get("status", {}) or {}).get("educates", {}) or {}
            log.info("DEBUG session=%s decision=%s phase=%r env=%r env_live=%s age=%ss :: %s | "
                     "status.educates=%s",
                     r["name"], r["decision"].upper(), r["phase"], r["env"], r["env_live"],
                     r["age_s"], r["reason"], ed)

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
    log.info("session reaper done: %d orphan(s), %d reaped%s",
             len(orphans), reaped, " (dry-run)" if dry else "")

    # --- environments: reap stale/duplicate WorkshopEnvironments (drain-safe) --------
    # The training-portal reconciles envs by create/delete only; a rolled workshop can
    # leave a stale env behind so the current one never appears → 'start' 403s. Deleting
    # the stale env forces the portal's working create path. Scoped to OUR portal + the
    # current catalog; an unreadable catalog means we skip (never nuke on a blip).
    if os.environ.get("REAPER_ENV_ENABLED", "true").lower() in ("1", "true", "yes"):
        desired = k8sclient.trainingportal_workshops()
        if not desired:
            log.warning("env reaper: TrainingPortal %r has no readable spec.workshops — "
                        "skipping env reaping (refuse to reap against an empty catalog).", portal)
        else:
            our_envs = [e for e in envs if _portal_of(e) == portal]
            active_by_env = {}
            for s in ours:
                if _phase(s) == "Allocated":
                    active_by_env[_env_of(s)] = active_by_env.get(_env_of(s), 0) + 1
            erows = classify_environments(our_envs, desired, active_by_env, now, grace)
            estale = [(r["name"], r["reason"]) for r in erows if r["decision"] == "reap"]
            log.info("env reaper: portal=%s our_envs=%d desired_workshops=%d stale=%d",
                     portal, len(our_envs), len(desired), len(estale))
            if debug:
                for r in erows:
                    log.info("DEBUG env=%s workshop=%r decision=%s phase=%r age=%ss active=%d :: %s",
                             r["name"], r["workshop"], r["decision"].upper(), r["phase"],
                             r["age_s"], r["active"], r["reason"])
            ereaped = 0
            for name, reason in estale:
                if dry:
                    log.info("would reap env %s (%s)", name, reason)
                    continue
                try:
                    k8sclient.delete_environment(name)
                    ereaped += 1
                    log.info("reaped env %s (%s)", name, reason)
                except Exception as e:                  # noqa: BLE001
                    log.warning("failed to reap env %s: %s", name, e)
            log.info("env reaper done: %d stale, %d reaped%s",
                     len(estale), ereaped, " (dry-run)" if dry else "")


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

    # env reaping (drain-safe): stale/dupe envs with no active sessions get reaped.
    def env(name, ws, age):
        return {"metadata": {"name": name,
                             "creationTimestamp":
                                 datetime.utcfromtimestamp(now - age).strftime("%Y-%m-%dT%H:%M:%SZ")},
                "spec": {"workshop": {"name": ws}}}
    envs = [
        env("wcurrent", "lab-live", 5000),      # keep: current env for a live workshop
        env("wold-dupe", "lab-live", 9000),     # reap: older dupe (newer wcurrent exists), 0 active
        env("wdropped", "lab-gone", 9000),      # reap: workshop not in catalog, 0 active
        env("wdraining", "lab-old", 9000),      # keep: stale but 1 active session draining
        env("wfresh", "lab-new", 30),           # keep: within grace (still provisioning)
    ]
    # newest per workshop: lab-live -> wcurrent (age 5000 < wold-dupe age 9000, so wcurrent newer)
    desired = {"lab-live", "lab-old", "lab-new"}
    active = {"wdraining": 1}
    erows = classify_environments(envs, desired, active, now, grace_s=300)
    ereap = {r["name"] for r in erows if r["decision"] == "reap"}
    assert ereap == {"wold-dupe", "wdropped"}, ereap
    print("reap.demo OK: sessions=%s envs=%s" % (got, ereap))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
