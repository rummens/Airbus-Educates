#!/usr/bin/env python3
"""Portal test suite (pytest, no cluster needed).

    pytest test_portal.py            # or:  python3 test_portal.py

Runs against the DEMO catalog + a throwaway sqlite DB. External dependencies
(Educates REST, the Kubernetes API, git README fetches) are monkeypatched, so the
whole suite is hermetic and fast.

Coverage: feedback/progress storage, settings/banner, trophies (identity +
persistence + isolation), analytics parsing, catalog helpers, README/vcluster/
module/source extraction, markdown render, loading-step labels, capacity handling,
the OAuth login guard, and the HTTP routes (landing, course, launch/over-limit,
session delete, admin banner).
"""
import os
import tempfile

os.environ["PORTAL_DEMO"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ.setdefault("PORTAL_OAUTH_ENABLED", "false")
os.environ["FEEDBACK_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")

import pytest                                    # noqa: E402
from portal import feedback, k8sclient, educates, auth   # noqa: E402
from portal import config as cfg                 # noqa: E402
from portal import app as appmod                 # noqa: E402
from portal.app import create_app                # noqa: E402


# --- fixtures ---------------------------------------------------------------

@pytest.fixture
def db(tmp_path, monkeypatch):
    """Isolated sqlite DB per test (fresh connection + file)."""
    monkeypatch.setattr(cfg, "FEEDBACK_DB", str(tmp_path / "t.db"))
    monkeypatch.setattr(feedback, "_conn", None)
    feedback.init_db()
    yield


@pytest.fixture
def client(db):
    return create_app().test_client()


# --- feedback + progress storage --------------------------------------------

def test_feedback(db):
    assert feedback.insert("lab-a01", "s1", "form", 5, 4, "great") is True
    assert feedback.insert("lab-a01", "s2", "analytics", 3, None, None) is True
    assert feedback.insert("lab-a02", "s3", "form", None, None, None) is False  # nothing to store
    rows, overall = feedback.aggregates()
    assert overall["n"] == 2, overall
    assert abs(overall["avg_rating"] - 4.0) < 1e-6, overall
    by = {r["workshop"]: r for r in rows}
    assert by["lab-a01"]["n"] == 2 and by["lab-a01"]["n_comment"] == 1
    r = feedback.ratings_by_workshop()
    assert r["lab-a01"]["n"] == 2 and abs(r["lab-a01"]["avg"] - 4.0) < 1e-6
    assert feedback.comments()[0]["comment"] == "great"


def test_progress(db):
    feedback.mark_progress("alice", "lab-a01", "started")
    feedback.mark_progress("alice", "lab-a02", "started")
    feedback.mark_progress("alice", "lab-a02", "completed")
    feedback.mark_progress("alice", "lab-a02", "started")   # must NOT downgrade
    assert feedback.user_progress("alice") == {"lab-a01": "started", "lab-a02": "completed"}
    assert feedback.last_in_progress("alice") == "lab-a01"   # only non-completed
    assert feedback.user_progress("") == {}                  # anon → empty


def test_settings_banner(db):
    assert feedback.get_setting("banner", "") == ""          # unset → default
    feedback.set_setting("banner", "Maintenance Sat 20:00")
    assert feedback.get_setting("banner") == "Maintenance Sat 20:00"
    feedback.set_setting("banner", "")                        # clear
    assert feedback.get_setting("banner", "x") == ""          # stored '' wins over default


# --- trophies: identity, persistence, isolation -----------------------------

_TROPHY_COURSES = [
    {"name": "l1", "module": "M1", "track": "T1"},
    {"name": "l2", "module": "M1", "track": "T1"},
    {"name": "l3", "module": "M2", "track": "T2"},
]


def test_trophies_none_when_nothing_done(db):
    t = appmod._trophies("alice", _TROPHY_COURSES)
    assert t["done"] == 0 and t["earned"] == 0 and t["total"] == 3


def test_trophies_partial_and_grouping(db):
    feedback.mark_progress("alice", "l1", "completed")
    feedback.mark_progress("alice", "l2", "completed")       # module M1 + track T1 complete
    t = appmod._trophies("alice", _TROPHY_COURSES)
    earned = {x["title"]: x["earned"] for x in t["items"]}
    assert t["done"] == 2
    assert earned["First Lab"] is True
    assert earned["M1 Module"] is True
    assert earned["M2 Module"] is False
    assert earned["T1 Track"] is True
    assert earned["Academy Master"] is False                 # l3 still open


def test_trophies_all_complete(db):
    for n in ("l1", "l2", "l3"):
        feedback.mark_progress("alice", n, "completed")
    t = appmod._trophies("alice", _TROPHY_COURSES)
    assert t["done"] == 3
    assert all(x["earned"] for x in t["items"])              # every trophy earned


def test_trophies_bound_to_identity(db):
    feedback.mark_progress("alice", "l1", "completed")
    assert appmod._trophies("alice", _TROPHY_COURSES)["done"] == 1
    assert appmod._trophies("bob", _TROPHY_COURSES)["done"] == 0     # isolated per user
    assert appmod._trophies("", _TROPHY_COURSES)["done"] == 0        # anon → nothing


def test_trophies_persist_across_reconnect(db, monkeypatch):
    feedback.mark_progress("alice", "l1", "completed")
    # Simulate a restart / new session: drop the connection, reconnect to the same
    # file. Progress (and therefore trophies) must survive.
    monkeypatch.setattr(feedback, "_conn", None)
    assert feedback.user_progress("alice") == {"l1": "completed"}
    assert appmod._trophies("alice", _TROPHY_COURSES)["done"] == 1


# --- catalog / helper logic -------------------------------------------------

def test_parse_minutes():
    from portal.app import _parse_minutes, _catalog_stats
    assert _parse_minutes("45 min") == 45
    assert _parse_minutes("1 h") == 60
    assert _parse_minutes("1.5h") == 90
    assert _parse_minutes("") == 0
    s = _catalog_stats([{"duration": "30 min"}, {"duration": "1 h"}], [{}, {}])
    assert s == {"workshops": 2, "tracks": 2, "hours": 2}, s


def test_icon_resolve():
    from portal.icons import resolve_icon, ICONS
    assert resolve_icon("fa-cube") == "box"
    assert resolve_icon("network-wired") == "network"
    assert resolve_icon("nonsense", default="book") == "book"
    for name in ("trophy", "medal", "award", "star", "info"):     # trophy/banner icons exist
        assert name in ICONS


def test_analytics_parse():
    p = feedback.parse_analytics(
        {"event": {"name": "workshop.rating", "data": {"score": 5}}, "workshop": {"name": "lab-a03"}})
    assert p == ("lab-a03", None, 5, None, None), p
    assert feedback.parse_analytics({"event": {"name": "session.started"}}) is None


def test_summary_and_prettify():
    assert k8sclient._first_sentence("First. Second.") == "First."
    assert k8sclient._first_sentence("") == ""
    assert k8sclient._prettify("lab-a02-kubernetes-essentials") == "Kubernetes Essentials"
    assert k8sclient._prettify("lab-3-storage") == "Storage"


def test_source_and_readme_url():
    spec = {"workshop": {"files": [{"git": {"url": "https://github.com/o/r.git", "ref": "origin/main"},
                                    "newRootPath": "a/b/lab"}]}}
    assert k8sclient._source_url(spec) == "https://github.com/o/r/tree/main/a/b/lab"
    assert k8sclient._readme_raw_url(spec) == "https://raw.githubusercontent.com/o/r/main/a/b/lab/README.md"
    # non-git (image) source → no links
    img = {"workshop": {"files": [{"image": {"url": "reg/lab-files:v1"}}]}}
    assert k8sclient._source_url(img) == "" and k8sclient._readme_raw_url(img) == ""


def test_vcluster_and_module():
    assert k8sclient._uses_vcluster({"session": {"applications": {"vcluster": {"enabled": True}}}}) is True
    assert k8sclient._uses_vcluster({"session": {"applications": {}}}) is False
    assert k8sclient._module({"labels": [{"name": "module", "value": "A-Foundations"}]}) == "A-Foundations"
    assert k8sclient._module({}) == ""


def test_steps_label_vcluster_vs_namespace():
    assert appmod._steps_for(True)[1] == "Starting virtual cluster"
    assert appmod._steps_for(False)[1] == "Setting up namespace"
    assert len(appmod._steps_for(False)) == len(appmod.STEPS)


def test_render_markdown():
    h = str(appmod._render_md("# Title\n\n- a\n- b\n\n```\noc get pods\n```"))
    assert "<h1" in h and "<li>" in h and "<code" in h
    assert appmod._render_md("") == ""


# --- identity / auth --------------------------------------------------------

def test_user_dev_fallback(monkeypatch):
    monkeypatch.setattr(cfg, "DEV_USER", "devguy")
    app = create_app()
    with app.test_request_context("/"):
        assert appmod._user() == "devguy"           # OAuth off → dev identity


def test_auth_disabled_no_identity():
    app = create_app()
    with app.test_request_context("/"):
        assert auth.current_user() == "" and auth.current_token() == ""


def test_login_guard_redirects_when_oauth_on(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    c = create_app().test_client()
    r = c.get("/", follow_redirects=False)
    assert r.status_code == 302 and "/login" in r.headers["Location"]
    assert c.get("/healthz").status_code == 200      # public endpoints stay open
    assert c.post("/analytics", json={}).status_code == 204   # webhook stays open (no cookie)


# --- Educates REST edge cases -----------------------------------------------

def test_request_session_raises_capacity(monkeypatch):
    class _Resp:
        status_code = 503
    class _Sess:
        def get(self, *a, **k):
            return _Resp()
    monkeypatch.setattr(educates, "_session", lambda: ("http://portal", _Sess()))
    monkeypatch.setattr(educates, "_env_for", lambda w: "env-x")
    monkeypatch.setattr(educates, "_public_host", lambda: "academy")
    with pytest.raises(educates.CapacityError):
        educates.request_session("lab-a01-what-is-dcs", "alice")


def test_fetch_readme_cached(monkeypatch):
    calls = {"n": 0}
    class _R:
        text = "# hi"
        def raise_for_status(self): pass
    def fake_get(url, timeout=0):
        calls["n"] += 1
        return _R()
    monkeypatch.setattr(educates.requests, "get", fake_get)
    monkeypatch.setattr(educates, "_readme_cache", {})
    assert educates.fetch_readme("https://x/readme") == "# hi"
    assert educates.fetch_readme("https://x/readme") == "# hi"   # second hit = cache
    assert calls["n"] == 1
    assert educates.fetch_readme("") == ""                       # no url → no fetch


# --- HTTP routes ------------------------------------------------------------

def test_landing_and_course(client):
    r = client.get("/")
    assert r.status_code == 200 and b"DCS" in r.data
    assert client.get("/course/lab-a02-kubernetes-essentials").status_code == 200
    assert client.get("/course/nope").status_code == 404
    assert client.get("/healthz").status_code == 200
    assert client.get("/metrics").status_code == 200
    assert client.get("/totally/unknown").status_code == 404     # not a route nor proxied


def test_banner_renders_on_landing(client):
    feedback.set_setting("banner", "Scheduled maintenance tonight")
    assert b"Scheduled maintenance tonight" in client.get("/").data
    feedback.set_setting("banner", "")
    assert b"Scheduled maintenance tonight" not in client.get("/").data


def test_trophies_render_for_dev_user(client, monkeypatch):
    monkeypatch.setattr(cfg, "DEV_USER", "alice")
    # complete one demo lab, expect the trophy strip to reflect it
    feedback.mark_progress("alice", "lab-a01-what-is-dcs", "completed")
    body = client.get("/").data
    assert b"Your trophies" in body
    assert b"labs done" in body


def test_launch_over_limit_page(client, monkeypatch):
    monkeypatch.setattr(educates, "request_session",
                        lambda name, user: (_ for _ in ()).throw(educates.CapacityError(name)))
    monkeypatch.setattr(k8sclient, "sessions_for_workshop",
                        lambda name: [{"name": "lab-a01-what-is-dcs-w01", "url": "https://s", "status": "Running"}])
    r = client.get("/launch/lab-a01-what-is-dcs")
    assert r.status_code == 503
    assert b"Session limit reached" in r.data and b"Remove" in r.data
    assert b"lab-a01-what-is-dcs-w01" in r.data


def test_session_delete_route(client, monkeypatch):
    seen = {}
    monkeypatch.setattr(educates, "delete_session", lambda n: seen.setdefault("name", n))
    r = client.post("/session/lab-x-w01/delete", data={"next": "/"}, follow_redirects=False)
    assert r.status_code == 302 and seen["name"] == "lab-x-w01"


def test_admin_gated(client, monkeypatch):
    monkeypatch.setattr(k8sclient, "user_can_admin", lambda tok: False)
    assert client.get("/admin").status_code == 403
    assert client.post("/admin/banner", data={"banner": "x"}).status_code == 403


def test_admin_can_set_banner(client, monkeypatch):
    monkeypatch.setattr(k8sclient, "user_can_admin", lambda tok: True)
    monkeypatch.setattr(k8sclient, "list_sessions", lambda: [])   # no cluster in tests
    assert client.get("/admin").status_code == 200
    r = client.post("/admin/banner", data={"banner": "Hello from admin"}, follow_redirects=False)
    assert r.status_code == 302
    assert feedback.get_setting("banner") == "Hello from admin"
    assert b"Hello from admin" in client.get("/").data


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
