#!/usr/bin/env python3
"""env-guard tests: portal/reap.py + portal/validate.py (pytest, no cluster).

These two modules run unattended as ArgoCD PostSync hooks / a CronJob and they
**delete** WorkshopSession and WorkshopEnvironment CRs, so the interesting cases are the
ones where they must NOT delete: within grace, live env, draining env, unreadable catalog,
missing portal name. The k8s API is monkeypatched — nothing here talks to a cluster.

Covers the decision cores (`classify`, `classify_environments`, `assess`), the small
helpers, and both `main()` entrypoints incl. dry-run, debug, delete failure, warn mode and
the settle-loop timeout.
"""
import os
import tempfile

os.environ["PORTAL_DEMO"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ.setdefault("PORTAL_OAUTH_ENABLED", "false")
os.environ["FEEDBACK_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")

import pytest                                    # noqa: E402
from portal import k8sclient, reap, validate     # noqa: E402
from portal import config as cfg                 # noqa: E402

NOW = 1_000_000.0
PORTAL = "dcst"


# --- builders ---------------------------------------------------------------

def ts(age_s):
    """creationTimestamp `age_s` seconds before NOW, in the RFC3339 form the API returns."""
    from datetime import datetime, timezone
    return datetime.fromtimestamp(NOW - age_s, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sess(name, env, phase="Allocated", age=600, portal=PORTAL):
    md = {"name": name, "creationTimestamp": ts(age)}
    if portal is not None:
        md["labels"] = {reap.PORTAL_LABEL: portal}
    return {"metadata": md, "spec": {"environment": {"name": env}},
            "status": {"educates": {"phase": phase}}}


def env(name, ws, age=5000, phase="Running", portal=PORTAL, terminating=False):
    md = {"name": name, "creationTimestamp": ts(age)}
    if portal is not None:
        md["labels"] = {reap.PORTAL_LABEL: portal}
    if terminating:
        md["deletionTimestamp"] = ts(10)
    return {"metadata": md, "spec": {"workshop": {"name": ws}},
            "status": {"educates": {"phase": phase}}}


@pytest.fixture
def cluster(monkeypatch):
    """Fake cluster state + recorded deletes. Mutate `state` inside a test."""
    state = {"envs": [], "sessions": [], "workshops": [], "portal_phase": "Running",
             "deleted_sessions": [], "deleted_envs": [], "fail_delete": False}
    monkeypatch.setattr(reap.cfg, "PORTAL_NAME", PORTAL)
    monkeypatch.setattr(validate.cfg, "PORTAL_NAME", PORTAL)
    monkeypatch.setattr(k8sclient, "list_environments", lambda: list(state["envs"]))
    monkeypatch.setattr(k8sclient, "list_sessions", lambda: list(state["sessions"]))
    monkeypatch.setattr(k8sclient, "trainingportal_workshops", lambda: list(state["workshops"]))
    monkeypatch.setattr(k8sclient, "portal_status", lambda: {"phase": state["portal_phase"]})

    def _del_sess(name):
        if state["fail_delete"]:
            raise RuntimeError("boom")
        state["deleted_sessions"].append(name)

    def _del_env(name):
        if state["fail_delete"]:
            raise RuntimeError("boom")
        state["deleted_envs"].append(name)

    monkeypatch.setattr(k8sclient, "delete_session", _del_sess)
    monkeypatch.setattr(k8sclient, "delete_environment", _del_env)
    monkeypatch.setattr(reap.time, "time", lambda: NOW)
    return state


# --- helpers ----------------------------------------------------------------

def test_helpers():
    assert reap._portal_of({"metadata": {"labels": {reap.PORTAL_LABEL: "p"}}}) == "p"
    assert reap._portal_of({}) is None                       # unlabelled → not ours
    assert reap._epoch(None) is None
    assert reap._epoch("not-a-timestamp") is None             # unparseable, not a crash
    assert reap._epoch("2020-01-01T00:00:00Z") == pytest.approx(1577836800)
    # phase falls back to status.phase when status.educates is absent
    assert reap._phase({"status": {"phase": "Stopped"}}) == "Stopped"
    assert reap._phase({}) == ""
    assert reap._env_of({}) == "" and reap._ws_of({}) == ""


def test_int_env(monkeypatch):
    monkeypatch.delenv("REAPER_GRACE_SECONDS", raising=False)
    assert reap._int_env("REAPER_GRACE_SECONDS", 300) == 300   # unset → default
    monkeypatch.setenv("REAPER_GRACE_SECONDS", "60")
    assert reap._int_env("REAPER_GRACE_SECONDS", 300) == 60
    monkeypatch.setenv("REAPER_GRACE_SECONDS", "twelve")
    assert reap._int_env("REAPER_GRACE_SECONDS", 300) == 300   # garbage → default, no crash


# --- session classification -------------------------------------------------

def test_classify_sessions_keeps_what_it_must():
    sessions = [
        sess("healthy", "env-live", "Allocated", 600),
        sess("spare", "env-live", "Available", 99999),      # not Allocated → backstop N/A
        sess("rollout-orphan", "env-gone", "Allocated", 600),
        sess("just-born", "env-gone", "Allocated", 10),     # within grace
        sess("restart-orphan", "env-live", "Allocated", 90000),
        {"metadata": {}},                                    # nameless → skipped entirely
        sess("no-timestamp", "env-live", "Allocated", 600),
    ]
    del sessions[-1]["metadata"]["creationTimestamp"]        # unparseable age → treated as 0
    rows = reap.classify(sessions, {"env-live"}, NOW, 24 * 3600, 300)
    by = {r["name"]: r for r in rows}
    assert len(rows) == 6                                    # the nameless one is gone
    assert by["healthy"]["decision"] == "keep"
    assert by["spare"]["decision"] == "keep"
    assert by["just-born"]["decision"] == "keep" and "grace" in by["just-born"]["reason"]
    assert by["no-timestamp"]["decision"] == "keep"          # age 0 → inside grace
    assert by["rollout-orphan"]["decision"] == "reap"
    assert by["restart-orphan"]["decision"] == "reap" and "backstop" in by["restart-orphan"]["reason"]
    assert {n for n, _ in reap.find_orphans(sessions, {"env-live"}, NOW, 24 * 3600, 300)} == \
        {"rollout-orphan", "restart-orphan"}


# --- environment classification --------------------------------------------

def test_classify_environments_is_drain_safe():
    envs = [
        env("wcurrent", "lab-live", 5000),
        env("wold-dupe", "lab-live", 9000),        # superseded by wcurrent
        env("wdropped", "lab-gone", 9000),         # workshop left the catalog
        env("wdraining", "lab-live", 9500),        # superseded but still serving a learner
        env("wfresh", "lab-vanished", 30),         # stale but inside grace (still provisioning)
        env("wterminating", "lab-gone", 9000, terminating=True),   # already going away
        {"metadata": {"creationTimestamp": ts(9000)}, "spec": {}},  # nameless → skipped
    ]
    rows = reap.classify_environments(envs, {"lab-live"},
                                      {"wdraining": 1}, NOW, 300)
    by = {r["name"]: r for r in rows}
    assert "wterminating" not in by and len(rows) == 5
    assert by["wcurrent"]["decision"] == "keep"
    assert by["wold-dupe"]["decision"] == "reap" and "superseded" in by["wold-dupe"]["reason"]
    assert by["wdropped"]["decision"] == "reap" and "dropped" in by["wdropped"]["reason"]
    assert by["wdraining"]["decision"] == "keep" and "draining" in by["wdraining"]["reason"]
    assert by["wfresh"]["decision"] == "keep" and "grace" in by["wfresh"]["reason"]


def test_reap_demo():
    reap.demo()                                   # module self-check must pass


# --- reap.main() ------------------------------------------------------------

def test_reap_main_requires_portal_name(monkeypatch):
    monkeypatch.setattr(reap.cfg, "PORTAL_NAME", "")
    with pytest.raises(SystemExit) as e:
        reap.main()
    assert e.value.code == 2                      # refuses to reap unscoped


def test_reap_main_deletes_orphans_and_stale_envs(cluster, monkeypatch):
    monkeypatch.setenv("REAPER_DEBUG", "true")    # exercise the decision dump too
    monkeypatch.delenv("REAPER_DRY_RUN", raising=False)
    cluster["envs"] = [env("env-live", "lab-live"), env("env-dupe", "lab-live", 9000)]
    cluster["sessions"] = [
        sess("healthy", "env-live"),
        sess("orphan", "env-gone"),
        sess("not-ours", "env-gone", portal="other-portal"),   # different portal → untouched
        sess("unlabelled", "env-gone", portal=None),
    ]
    cluster["workshops"] = ["lab-live"]
    reap.main()
    assert cluster["deleted_sessions"] == ["orphan"]
    assert cluster["deleted_envs"] == ["env-dupe"]


def test_reap_main_dry_run_deletes_nothing(cluster, monkeypatch):
    monkeypatch.setenv("REAPER_DRY_RUN", "true")
    cluster["envs"] = [env("env-live", "lab-live"), env("env-dupe", "lab-live", 9000)]
    cluster["sessions"] = [sess("orphan", "env-gone")]
    cluster["workshops"] = ["lab-live"]
    reap.main()
    assert cluster["deleted_sessions"] == [] and cluster["deleted_envs"] == []


def test_reap_main_survives_delete_failures(cluster, monkeypatch):
    monkeypatch.delenv("REAPER_DRY_RUN", raising=False)
    cluster["fail_delete"] = True
    cluster["envs"] = [env("env-live", "lab-live"), env("env-dupe", "lab-live", 9000)]
    cluster["sessions"] = [sess("orphan", "env-gone")]
    cluster["workshops"] = ["lab-live"]
    reap.main()                                   # a failed delete is logged, never raised
    assert cluster["deleted_sessions"] == [] and cluster["deleted_envs"] == []


def test_reap_main_skips_env_reaping_on_empty_catalog(cluster, monkeypatch):
    """An unreadable/empty TrainingPortal must never be read as 'catalog has no labs'."""
    monkeypatch.delenv("REAPER_DRY_RUN", raising=False)
    cluster["envs"] = [env("env-a", "lab-live"), env("env-b", "lab-gone", 9000)]
    cluster["sessions"] = []
    cluster["workshops"] = []
    reap.main()
    assert cluster["deleted_envs"] == []


def test_reap_main_env_reaping_can_be_switched_off(cluster, monkeypatch):
    monkeypatch.delenv("REAPER_DRY_RUN", raising=False)
    monkeypatch.setenv("REAPER_ENV_ENABLED", "false")
    cluster["envs"] = [env("env-live", "lab-live"), env("env-dupe", "lab-live", 9000)]
    cluster["workshops"] = ["lab-live"]
    reap.main()
    assert cluster["deleted_envs"] == []
    monkeypatch.delenv("REAPER_ENV_ENABLED")


# --- validate.assess --------------------------------------------------------

def test_assess_ready_missing_and_session_fallback():
    envs = [
        env("e-a", "lab-a"),                                  # ready by phase
        env("e-b", "lab-b", phase="Provisioning"),            # not ready by phase…
        env("e-c-old", "lab-c", terminating=True),            # terminating → lab-c has none
        env("e-extra", "lab-not-in-catalog"),
    ]
    sessions = [{"spec": {"environment": {"name": "e-b"}},
                 "status": {"educates": {"phase": "Reserved"}}},
                {"spec": {"environment": {"name": "e-dead"}},
                 "status": {"educates": {"phase": "Stopped"}}}]   # dead → no fallback
    ok, rep = validate.assess({"lab-a", "lab-b", "lab-c"}, envs, sessions, "Running", {"Running"})
    assert not ok
    assert rep["workshops"]["lab-a"]["ready"] is True
    assert rep["workshops"]["lab-b"]["ready"] is True         # …but backed by a live session
    assert rep["workshops"]["lab-c"]["ready"] is False
    assert rep["workshops"]["lab-c"]["reason"] == "no WorkshopEnvironment"
    assert rep["extra_envs"] == ["lab-not-in-catalog"]
    validate._report(rep)                                     # log formatting must not blow up


def test_assess_phase_and_duplicate_reasons():
    ok, rep = validate.assess({"lab-a"}, [env("e-a", "lab-a", phase="Stopped")], [],
                              "Running", {"Running"})
    assert not ok and "none ready" in rep["workshops"]["lab-a"]["reason"]
    # two ready envs: still OK (a start can be served) but the report says so
    ok2, rep2 = validate.assess({"lab-a"}, [env("e-1", "lab-a"), env("e-2", "lab-a")], [],
                                "Running", {"Running"})
    assert ok2 and "2 ready envs" in rep2["workshops"]["lab-a"]["reason"]


def test_assess_needs_a_running_portal():
    ok, rep = validate.assess({"lab-a"}, [env("e-a", "lab-a")], [], "Pending", {"Running"})
    assert not ok and rep["portal_ok"] is False


def test_validate_demo():
    validate.demo()                               # module self-check must pass


# --- validate.main() --------------------------------------------------------

def test_validate_main_requires_portal_name(monkeypatch):
    monkeypatch.setattr(validate.cfg, "PORTAL_NAME", "")
    with pytest.raises(SystemExit) as e:
        validate.main()
    assert e.value.code == 2


def test_validate_main_passes_when_every_workshop_has_an_env(cluster):
    cluster["workshops"] = ["lab-live"]
    cluster["envs"] = [env("env-live", "lab-live")]
    validate.main()                               # returns → hook exits 0 → Argo green


def test_validate_main_fails_on_unreadable_catalog(cluster, monkeypatch):
    cluster["workshops"] = []
    with pytest.raises(SystemExit) as e:
        validate.main()
    assert e.value.code == 2
    monkeypatch.setenv("VALIDATE_MODE", "warn")
    with pytest.raises(SystemExit) as e2:         # warn mode: same finding, but exit 0
        validate.main()
    assert e2.value.code == 0
    monkeypatch.delenv("VALIDATE_MODE")


def test_validate_main_fails_when_an_env_is_missing(cluster, monkeypatch):
    """The gate's whole purpose: a catalog workshop with no env must fail the sync."""
    monkeypatch.setenv("VALIDATE_SETTLE_SECONDS", "0")        # no waiting in tests
    cluster["workshops"] = ["lab-live", "lab-broken"]
    cluster["envs"] = [env("env-live", "lab-live")]
    with pytest.raises(SystemExit):
        validate.main()
    monkeypatch.setenv("VALIDATE_MODE", "warn")
    validate.main()                                           # warn → logs, exits 0
    monkeypatch.delenv("VALIDATE_MODE")
    monkeypatch.delenv("VALIDATE_SETTLE_SECONDS")


def test_validate_main_polls_until_converged(cluster, monkeypatch):
    """Envs appear late (the normal case right after a sync) — the gate must wait, not fail."""
    monkeypatch.setenv("VALIDATE_SETTLE_SECONDS", "60")
    monkeypatch.setenv("VALIDATE_POLL_SECONDS", "0")
    cluster["workshops"] = ["lab-live"]
    calls = {"n": 0}

    def envs_appearing_late():
        calls["n"] += 1
        return [] if calls["n"] < 3 else [env("env-live", "lab-live")]

    monkeypatch.setattr(k8sclient, "list_environments", envs_appearing_late)
    monkeypatch.setattr(validate.time, "sleep", lambda s: None)
    validate.main()
    assert calls["n"] >= 3
    monkeypatch.delenv("VALIDATE_SETTLE_SECONDS")
    monkeypatch.delenv("VALIDATE_POLL_SECONDS")


def test_validate_main_tolerates_unreadable_portal_status(cluster, monkeypatch):
    monkeypatch.setenv("VALIDATE_SETTLE_SECONDS", "0")
    monkeypatch.setenv("VALIDATE_MODE", "warn")
    cluster["workshops"] = ["lab-live"]
    cluster["envs"] = [env("env-live", "lab-live")]
    monkeypatch.setattr(k8sclient, "portal_status", lambda: (_ for _ in ()).throw(RuntimeError("no api")))
    validate.main()                               # phase unknown → not ok, but warn exits 0
    monkeypatch.delenv("VALIDATE_MODE")
    monkeypatch.delenv("VALIDATE_SETTLE_SECONDS")
