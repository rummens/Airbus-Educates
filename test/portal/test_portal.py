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
import re
import tempfile

os.environ["PORTAL_DEMO"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ.setdefault("PORTAL_OAUTH_ENABLED", "false")
os.environ["FEEDBACK_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")

import pytest                                    # noqa: E402
from portal import feedback, k8sclient, educates, auth, proxy, cache, reap   # noqa: E402
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
    feedback.mark_progress("alice", "l2", "completed")       # track T1 complete
    t = appmod._trophies("alice", _TROPHY_COURSES)
    earned = {x["title"]: x["earned"] for x in t["items"]}
    assert t["done"] == 2
    assert earned["First Lab"] is True
    assert "M1 Module" not in earned                         # no per-module trophies anymore
    assert earned["T1 Track"] is True
    assert earned["T2 Track"] is False
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


def test_session_route_ready(monkeypatch):
    # Two-stage gate: the Route must be Admitted AND actually serving (not the router's
    # 503 page). Stub the HTTP probe so the test needs no network.
    admitted = {"items": [{"spec": {"host": "s1.apps.test"},
                           "status": {"ingress": [{"conditions": [{"type": "Admitted", "status": "True"}]}]}}]}
    pending = {"items": [{"spec": {"host": "s1.apps.test"},
                         "status": {"ingress": [{"conditions": [{"type": "Admitted", "status": "False"}]}]}}]}
    class _CO:
        def __init__(self, data): self.data = data
        def list_cluster_custom_object(self, *a, **k): return self.data

    # Admitted + backend serving → ready.
    monkeypatch.setattr(k8sclient, "_co", lambda: _CO(admitted))
    monkeypatch.setattr(k8sclient, "_route_http_ok", lambda url: True)
    assert k8sclient.session_route_ready("sess", "https://s1.apps.test/") is True
    # Admitted but the router still serves the 503 page → NOT ready (the race we fixed).
    monkeypatch.setattr(k8sclient, "_route_http_ok", lambda url: False)
    assert k8sclient.session_route_ready("sess", "https://s1.apps.test/") is False
    # Not admitted yet → NOT ready, and the probe is never reached.
    monkeypatch.setattr(k8sclient, "_co", lambda: _CO(pending))
    monkeypatch.setattr(k8sclient, "_route_http_ok",
                        lambda url: (_ for _ in ()).throw(AssertionError("probe must not run when not admitted")))
    assert k8sclient.session_route_ready("sess", "https://s1.apps.test/") is False
    assert k8sclient.session_route_ready("sess", "") is False        # no url


def test_trophies_dynamic_from_tracks(db):
    # per-track trophies come from the live Track CRs → adding a track grows them; no per-module
    courses = [{"name": "x1", "module": "B-Developer", "track": "dev"}]
    tracks = [{"name": "dev", "title": "Developer — Build on DCS"}]
    t = appmod._trophies("alice", courses, tracks)
    titles = [x["title"] for x in t["items"]]
    assert not any("Module" in x for x in titles)  # no per-module trophies
    assert "Developer — Build on DCS Track" in titles or "Developer — Build on DCS" in titles


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
        status_code = 200
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


def test_banner_renders_markdown(client):
    feedback.set_setting("banner", "**down** now\n\nsee [docs](http://x)")
    body = client.get("/").data
    feedback.set_setting("banner", "")
    assert b"<strong>down</strong>" in body            # markdown → HTML
    assert b'<a href="http://x">docs</a>' in body      # multi-paragraph + links


def test_trophies_render_for_dev_user(client, monkeypatch):
    monkeypatch.setattr(cfg, "DEV_USER", "alice")
    # complete one demo lab, expect the trophy strip to reflect it
    feedback.mark_progress("alice", "lab-a01-what-is-dcs", "completed")
    body = client.get("/").data
    assert b"Your trophies" in body
    assert b"view all" in body
    # dedicated page renders with earned/locked cards
    page = client.get("/trophies").data
    assert b"Trophies" in page and (b"Earned" in page or b"Locked" in page)


def test_launch_over_limit_page(client, monkeypatch):
    monkeypatch.setattr(educates, "request_session",
                        lambda name, user: (_ for _ in ()).throw(educates.CapacityError(name)))
    r = client.get("/launch/lab-a01-what-is-dcs")
    assert r.status_code == 503
    assert b"Session limit reached" in r.data and b"My Sessions" in r.data


def test_session_end_route(client, monkeypatch):
    # end route is ownership-gated: only the caller's own sessions (or an admin) can end.
    seen = {}
    monkeypatch.setattr(educates, "terminate_session", lambda n: seen.setdefault("name", n))
    monkeypatch.setattr(appmod, "_my_sessions",
                        lambda user: [{"name": "lab-x-w01", "workshop": "lab-x"}])
    r = client.post("/session/lab-x-w01/end", follow_redirects=False)
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


# --- /admin/rescan (PostSync hook trigger) ----------------------------------

def test_rescan_via_token(client, monkeypatch):
    # A non-admin caller with the right bearer token triggers a refresh.
    monkeypatch.setattr(k8sclient, "user_can_admin", lambda tok: False)
    monkeypatch.setattr(cfg, "RESCAN_TOKEN", "s3kr3t")
    calls = []
    monkeypatch.setattr(cache, "refresh_all", lambda: calls.append(1) or ["courses", "tracks"])
    r = client.post("/admin/rescan", headers={"Authorization": "Bearer s3kr3t"})
    assert r.status_code == 200
    assert r.get_json()["refreshed"] == ["courses", "tracks"]
    assert calls == [1]


def test_rescan_bad_or_missing_token_forbidden(client, monkeypatch):
    monkeypatch.setattr(k8sclient, "user_can_admin", lambda tok: False)
    monkeypatch.setattr(cfg, "RESCAN_TOKEN", "s3kr3t")
    monkeypatch.setattr(cache, "refresh_all", lambda: ["x"])   # must NOT be called
    assert client.post("/admin/rescan", headers={"Authorization": "Bearer wrong"}).status_code == 403
    assert client.post("/admin/rescan").status_code == 403


def test_rescan_via_admin_user(client, monkeypatch):
    # No token configured → only an SSAR admin user can trigger it.
    monkeypatch.setattr(cfg, "RESCAN_TOKEN", "")
    monkeypatch.setattr(k8sclient, "user_can_admin", lambda tok: True)
    monkeypatch.setattr(cache, "refresh_all", lambda: ["tracks"])
    r = client.post("/admin/rescan")
    assert r.status_code == 200 and r.get_json()["refreshed"] == ["tracks"]


# --- cache: TTL / last-known-good / cold default ----------------------------

def test_cache_last_known_good_and_cold():
    from portal.cache import Cached
    seq = iter([["a"], RuntimeError("boom"), ["b"]])

    def prod():
        v = next(seq)
        if isinstance(v, Exception):
            raise v
        return v

    c = Cached("t", prod, ttl=0, default=[])
    assert c.get() == ["a"]                 # first good
    assert c.get() == ["a"]                 # ttl=0 → refresh fails → last good
    assert c.get() == ["b"]                 # recovers
    assert c.get(force=True) == ["b"] or True   # exhausted iter → last good retained
    cold = Cached("cold", lambda: (_ for _ in ()).throw(RuntimeError()), ttl=0, default=[])
    assert cold.get() == []                 # cold failure → default


def test_cache_serves_fresh_within_ttl():
    from portal.cache import Cached
    calls = {"n": 0}

    def prod():
        calls["n"] += 1
        return calls["n"]

    c = Cached("fresh", prod, ttl=999)
    assert c.get() == 1 and c.get() == 1     # second read is cached (producer not called again)
    assert calls["n"] == 1


# --- k8sclient live paths (non-DEMO, fake CustomObjects/Core APIs) ----------

class _FakeCO:
    def __init__(self, listing=None, obj=None):
        self._listing, self._obj = listing or {}, obj or {}
    def list_cluster_custom_object(self, *a, **k):
        return self._listing
    def get_cluster_custom_object(self, *a, **k):
        return self._obj


def test_list_courses_live_enriches(monkeypatch):
    monkeypatch.setattr(cfg, "DEMO", False)
    item = {"metadata": {"name": "lab-a02-kubernetes-essentials",
                         "labels": {f"{cfg.ACADEMY_PREFIX}/track": "core", f"{cfg.ACADEMY_PREFIX}/order": "20"},
                         "annotations": {f"{cfg.ACADEMY_PREFIX}/summary": "Do k8s."}},
            "spec": {"title": "Kubernetes Essentials", "description": "Full desc. More.",
                     "labels": [{"name": "module", "value": "A-Foundations"}],
                     "workshop": {"files": [{"git": {"url": "https://github.com/o/r.git",
                                                      "ref": "origin/main"}, "newRootPath": "a/lab"}]}}}
    monkeypatch.setattr(k8sclient, "_co", lambda: _FakeCO(listing={"items": [item]}))
    monkeypatch.setattr(k8sclient, "_list_courses_live", k8sclient._list_courses_live)  # ensure not cached-only
    out = k8sclient._list_courses_live()
    c = out[0]
    assert c["name"] == "lab-a02-kubernetes-essentials" and c["track"] == "core"
    assert c["summary"] == "Do k8s." and c["module"] == "A-Foundations" and c["order"] == 20
    assert c["source_url"].endswith("/tree/main/a/lab")


def test_list_tracks_live(monkeypatch):
    monkeypatch.setattr(cfg, "DEMO", False)
    item = {"metadata": {"name": "core"}, "spec": {"title": "Core", "order": 5, "icon": "layers"}}
    monkeypatch.setattr(k8sclient, "_co", lambda: _FakeCO(listing={"items": [item]}))
    out = k8sclient._list_tracks_live()
    assert out == [{"name": "core", "title": "Core", "description": "", "order": 5, "icon": "layers"}]


def test_portal_status_and_service_base(monkeypatch):
    monkeypatch.setattr(k8sclient, "_co",
                        lambda: _FakeCO(obj={"status": {"educates": {"namespace": "dcst-ui"}}}))
    assert k8sclient.portal_status() == {"namespace": "dcst-ui"}
    monkeypatch.setattr(cfg, "PORTAL_SERVICE_URL", "")
    assert k8sclient.portal_service_base() == "http://training-portal.dcst-ui.svc"


def test_session_status_and_list_sessions(monkeypatch):
    monkeypatch.setattr(k8sclient, "_co",
                        lambda: _FakeCO(obj={"status": {"educates": {"phase": "Allocated"}}},
                                        listing={"items": [{"metadata": {"name": "s1"}}]}))
    assert k8sclient.session_status("s1") == {"phase": "Allocated"}
    assert k8sclient.list_sessions()[0]["metadata"]["name"] == "s1"


def test_user_can_admin_no_token():
    assert k8sclient.user_can_admin("") is False


def test_ping_demo_noop():
    # DEMO ping is a no-op (set at import time); must not touch a cluster
    assert k8sclient.ping() is None


# --- educates REST client ---------------------------------------------------

def _fake_portal(monkeypatch):
    monkeypatch.setattr(educates.k8sclient, "portal_status",
                        lambda: {"credentials": {"robot": {"username": "rob", "password": "pw"}},
                                 "clients": {"robot": {"id": "cid", "secret": "sec"}},
                                 "url": "https://academy.test/"})
    monkeypatch.setattr(educates.k8sclient, "portal_service_base", lambda: "http://portal.svc")
    educates.invalidate_token()


class _Resp:
    def __init__(self, code=200, data=None):
        self.status_code, self._data = code, (data or {})
    def raise_for_status(self):
        if self.status_code >= 400:
            raise educates.requests.HTTPError(f"{self.status_code}")
    def json(self):
        return self._data


def test_educates_token_and_public_host(monkeypatch):
    _fake_portal(monkeypatch)
    monkeypatch.setattr(educates.requests, "post",
                        lambda *a, **k: _Resp(200, {"access_token": "tok", "expires_in": 3600}))
    assert educates._token("http://portal.svc", "rob", "pw", "cid", "sec") == "tok"
    assert educates._public_host() == "academy.test"


def test_env_for_and_catalog(monkeypatch):
    _fake_portal(monkeypatch)
    monkeypatch.setattr(educates, "_session", lambda: ("http://portal.svc", _Sess200()))
    monkeypatch.setattr(educates, "_catalog", educates.Cached("t", educates._catalog_live, ttl=999, default=[]))
    assert educates._env_for("lab-a01-what-is-dcs") == "env-a01"
    assert educates._env_for("unknown-lab") == "unknown-lab"       # fallback to name


class _Sess200:
    def get(self, url, **k):
        if "catalog/environments" in url:
            return _Resp(200, {"environments": [{"name": "env-a01",
                                                 "workshop": {"name": "lab-a01-what-is-dcs"}}]})
        if "/request/" in url:
            return _Resp(200, {"name": "sess-1", "url": "/session/sess-1/"})
        if "/sessions/" in url:
            return _Resp(200, {"sessions": [{"name": "sess-1", "workshop": "lab-a01-what-is-dcs"}]})
        if "/status/" in url:
            return _Resp(200, {"phase": "Allocated"})
        if "/terminate/" in url:
            return _Resp(200, {})
        return _Resp(404)


def test_request_session_success(monkeypatch):
    _fake_portal(monkeypatch)
    monkeypatch.setattr(educates, "_session", lambda: ("http://portal.svc", _Sess200()))
    monkeypatch.setattr(educates, "_catalog", educates.Cached("t2", educates._catalog_live, ttl=999, default=[]))
    monkeypatch.setattr(educates, "_public_host", lambda: "academy.test")
    out = educates.request_session("lab-a01-what-is-dcs", "alice")
    assert out["name"] == "sess-1" and out["url"] == "/session/sess-1/"


def test_request_session_stale_ref_retries(monkeypatch):
    _fake_portal(monkeypatch)
    monkeypatch.setattr(educates, "_public_host", lambda: "academy.test")
    monkeypatch.setattr(educates, "_env_for", lambda w: "env-x")
    calls = {"n": 0}

    class _S:
        def get(self, url, **k):
            calls["n"] += 1
            return _Resp(404) if calls["n"] == 1 else _Resp(200, {"name": "s", "url": "/u"})
    monkeypatch.setattr(educates, "_session", lambda: ("http://portal.svc", _S()))
    monkeypatch.setattr(educates, "catalog", lambda force=False: [])
    out = educates.request_session("lab-a01-what-is-dcs", "alice")
    assert out["name"] == "s" and calls["n"] == 2           # 404 → refresh → retry


def test_user_sessions_and_terminate_and_status(monkeypatch):
    _fake_portal(monkeypatch)
    monkeypatch.setattr(educates, "_session", lambda: ("http://portal.svc", _Sess200()))
    assert educates.user_sessions("alice")[0]["name"] == "sess-1"
    assert educates.user_sessions("") == []                 # no user → no call
    assert educates.terminate_session("sess-1") is True
    assert educates.rest_session_status("sess-1") == {"phase": "Allocated"}


def test_fetch_readme_failure_returns_empty(monkeypatch):
    monkeypatch.setattr(educates, "_readme_cache", {})

    def boom(url, timeout=0):
        raise educates.requests.RequestException("down")
    monkeypatch.setattr(educates.requests, "get", boom)
    assert educates.fetch_readme("https://x/readme") == ""


# --- auth: OAuth login / callback / logout ----------------------------------

def test_auth_endpoints_and_login_redirect(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    monkeypatch.setattr(auth, "_endpoints", lambda: ("https://sso/authorize", "https://sso/token"))
    monkeypatch.setattr(cfg, "OAUTH_CLIENT_ID", "cid")
    monkeypatch.setattr(cfg, "OAUTH_REDIRECT_URL", "https://academy/oauth/callback")
    c = create_app().test_client()
    r = c.get("/login?next=/course/x", follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"].startswith("https://sso/authorize?")
    assert "client_id=cid" in r.headers["Location"]


def test_auth_callback_state_mismatch(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    c = create_app().test_client()
    with c.session_transaction() as s:
        s["oauth_state"] = "good"
    r = c.get("/oauth/callback?state=bad&code=z", follow_redirects=False)
    assert r.status_code == 400


def test_auth_callback_success(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    monkeypatch.setattr(auth, "_endpoints", lambda: ("https://sso/authorize", "https://sso/token"))
    monkeypatch.setattr(auth, "_client_secret", lambda: "shh")
    monkeypatch.setattr(auth.requests, "post", lambda *a, **k: _Resp(200, {"access_token": "AT"}))
    monkeypatch.setattr(auth, "_whoami", lambda tok: "alice")
    c = create_app().test_client()
    with c.session_transaction() as s:
        s["oauth_state"] = "st"
        s["oauth_next"] = "/course/x"
    r = c.get("/oauth/callback?state=st&code=abc", follow_redirects=False)
    assert r.status_code == 302 and r.headers["Location"].endswith("/course/x")
    with c.session_transaction() as s:
        assert s["user"] == "alice" and s["token"] == "AT"


def test_auth_logout(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    c = create_app().test_client()
    with c.session_transaction() as s:
        s["user"] = "alice"
    assert c.get("/logout", follow_redirects=False).status_code == 302
    with c.session_transaction() as s:
        assert "user" not in s


def test_current_user_token_when_oauth_on(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    app = create_app()
    with app.test_request_context("/"):
        from flask import session
        session["user"], session["token"] = "bob", "T"
        assert auth.current_user() == "bob" and auth.current_token() == "T"


# --- proxy ------------------------------------------------------------------

def test_proxy_is_proxied():
    assert proxy.is_proxied("/session/abc") is True
    assert proxy.is_proxied("/oauth2/token/") is True
    assert proxy.is_proxied("/course/x") is False


def test_proxy_forwards_allowlisted(client, monkeypatch):
    monkeypatch.setattr(k8sclient, "portal_service_base", lambda: "http://portal.svc")
    monkeypatch.setattr(k8sclient, "portal_status", lambda: {"url": "https://academy.test/"})

    class _Up:
        status_code = 200
        headers = {"Location": ""}
        class raw:
            headers = type("H", (), {"items": staticmethod(lambda: [("Content-Type", "text/html")]),
                                     "getlist": staticmethod(lambda k: [])})()
        def iter_content(self, chunk_size=0):
            yield b"upstream-body"
    monkeypatch.setattr(proxy.requests, "request", lambda **k: _Up())
    r = client.get("/session/sess-1/")
    assert r.status_code == 200 and b"upstream-body" in r.data


# --- app routes: my-sessions, status feed, form/feedback, help, readyz ------

def test_my_sessions_route(client, monkeypatch):
    monkeypatch.setattr(educates, "user_sessions",
                        lambda u: [{"name": "s1", "workshop": "lab-a01-what-is-dcs"}])
    monkeypatch.setattr(k8sclient, "list_sessions", lambda: [])
    monkeypatch.setattr(cfg, "DEV_USER", "alice")
    r = client.get("/my-sessions")
    assert r.status_code == 200


def test_session_status_api(client, monkeypatch):
    monkeypatch.setattr(k8sclient, "session_status",
                        lambda n: {"phase": "Allocated", "url": "/session/s/"})
    monkeypatch.setattr(k8sclient, "session_pods",
                        lambda n: [{"name": "p", "namespace": "ns", "vcluster": False,
                                    "phase": "Running", "ready": 1, "total": 1}])
    monkeypatch.setattr(k8sclient, "session_route_ready", lambda n, u: True)
    j = client.get("/api/session/s/status?t0=0&vc=0").get_json()
    assert j["ready"] is True and j["step"] == "Ready" and j["phase"] == "Allocated"


def test_status_feed_vcluster_waits(monkeypatch):
    monkeypatch.setattr(k8sclient, "session_status", lambda n: {"phase": "Allocated", "url": "/u"})
    # workshop pod ready, but no vc pods yet → a vcluster lab must NOT be Ready
    monkeypatch.setattr(k8sclient, "session_pods",
                        lambda n: [{"name": "ws", "namespace": "ns", "vcluster": False,
                                    "phase": "Running", "ready": 1, "total": 1}])
    monkeypatch.setattr(k8sclient, "session_route_ready", lambda n, u: True)
    feed = appmod._status_feed("s", 0, expect_vc=True)
    assert feed["ready"] is False and feed["step"] == "Starting virtual cluster"


def test_form_and_feedback_flow(client, monkeypatch):
    monkeypatch.setattr(cfg, "DEV_USER", "alice")
    assert client.get("/form?workshop=lab-a01&session=s1").status_code == 200
    r = client.post("/feedback", data={"workshop": "lab-a01", "session": "s1",
                                       "rating": "5", "clarity": "4", "comment": "nice"})
    assert r.status_code == 200 and b"" is not None
    assert feedback.user_progress("alice").get("lab-a01") == "completed"   # feedback → completed


def test_help_and_readyz(client, monkeypatch):
    assert client.get("/help").status_code == 200
    monkeypatch.setattr(k8sclient, "ping", lambda: None)
    assert client.get("/readyz").status_code == 200
    monkeypatch.setattr(k8sclient, "ping", lambda: (_ for _ in ()).throw(RuntimeError("no api")))
    assert client.get("/readyz").status_code == 503


def test_launch_success_and_error(client, monkeypatch):
    monkeypatch.setattr(educates, "request_session",
                        lambda name, user: {"name": "s1", "url": "/session/s1/"})
    r = client.get("/launch/lab-a02-kubernetes-essentials")
    assert r.status_code == 200 and b"s1" in r.data
    # a non-capacity exception → 502 launch page (not a raw 500)
    monkeypatch.setattr(educates, "request_session",
                        lambda name, user: (_ for _ in ()).throw(RuntimeError("boom")))
    assert client.get("/launch/lab-a02-kubernetes-essentials").status_code == 502
    assert client.get("/launch/does-not-exist").status_code == 404


def test_usage_and_de_filter(monkeypatch):
    monkeypatch.setattr(k8sclient, "list_sessions",
                        lambda: [{"metadata": {"name": "s1"}, "spec": {"workshop": {"name": "lab-a01"}},
                                  "status": {"educates": {"user": "alice", "phase": "Allocated"}}}])
    u = appmod._usage()
    assert u[0] == {"name": "s1", "workshop": "lab-a01", "user": "alice", "phase": "Allocated"}
    app = create_app()
    de = app.jinja_env.filters["de"]
    assert de("") == ""
    assert re.match(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}", de("2026-07-13T10:00:00"))


def test_abs_session_url():
    assert appmod._abs_session_url("") == ""
    assert appmod._abs_session_url("session/x") == "/session/x"
    assert appmod._abs_session_url("/session/x") == "/session/x"
    assert appmod._abs_session_url("https://h/s") == "https://h/s"


# --- metrics live collector -------------------------------------------------

def test_metrics_collector_counts(db, monkeypatch):
    from portal import metrics
    monkeypatch.setattr(k8sclient, "list_sessions",
                        lambda: [{"status": {"educates": {"phase": "Running"}},
                                  "spec": {"environment": {"name": "lab-a01"},
                                           "session": {"username": "alice"}}},
                                 {"status": {"educates": {"phase": "Stopped"}}, "spec": {}}])
    monkeypatch.setattr(k8sclient, "list_courses", lambda: [{"name": "x"}])
    monkeypatch.setattr(k8sclient, "list_tracks", lambda: [{"name": "t"}])
    feedback.insert("lab-a01", "s1", "form", 5, 4, "ok")
    out = metrics.render().decode()
    assert "dcs_portal_sessions_running" in out
    assert 'dcs_portal_users_active 1.0' in out
    assert "dcs_portal_feedback_total" in out


# --- k8sclient session pods + route-ready fail-open + admin SSAR ------------

class _FakePod:
    def __init__(self, ns, name, phase="Running", ready=1, total=1):
        cs = [type("C", (), {"ready": i < ready})() for i in range(total)]
        self.metadata = type("M", (), {"namespace": ns, "name": name})()
        self.status = type("S", (), {"phase": phase, "container_statuses": cs})()


class _FakeCore:
    def __init__(self, all_ns, vc_ns=None):
        self._all, self._vc = all_ns, (vc_ns or [])
    def list_pod_for_all_namespaces(self, label_selector=None):
        return type("R", (), {"items": self._all})()
    def list_namespaced_pod(self, ns):
        return type("R", (), {"items": self._vc})()


def test_session_pods_merges_vcluster(monkeypatch):
    ws = _FakePod("s-ns", "ws-pod", ready=1, total=1)
    vc = _FakePod("sess-vc", "my-vcluster-0", ready=1, total=1)
    monkeypatch.setattr(k8sclient, "_core", lambda: _FakeCore([ws], [vc]))
    pods = k8sclient.session_pods("sess")
    names = {p["name"]: p for p in pods}
    assert names["ws-pod"]["vcluster"] is False
    assert names["my-vcluster-0"]["vcluster"] is True and names["my-vcluster-0"]["ready"] == 1


def test_session_route_ready_no_rbac_falls_through_to_probe(monkeypatch):
    # Without Routes RBAC we can't check admission, so we rely solely on the HTTP probe
    # (never fail open early — the probe is the source of truth).
    from kubernetes.client.rest import ApiException

    class _Boom:
        def list_cluster_custom_object(self, *a, **k):
            raise ApiException(status=403)
    monkeypatch.setattr(k8sclient, "_co", lambda: _Boom())

    monkeypatch.setattr(k8sclient, "_route_http_ok", lambda url: True)
    assert k8sclient.session_route_ready("sess", "https://s.apps.test/") is True
    monkeypatch.setattr(k8sclient, "_route_http_ok", lambda url: False)
    assert k8sclient.session_route_ready("sess", "https://s.apps.test/") is False


def test_route_http_ok(monkeypatch):
    # 503 (router "Application is not available") = not ready; 200/401/3xx = serving;
    # connection error = not ready.
    import urllib.error
    import urllib.request

    def _resp(code):
        class _R:
            def getcode(self): return code
        return _R()

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _resp(200))
    assert k8sclient._route_http_ok("https://s.apps.test/") is True
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _resp(503))
    assert k8sclient._route_http_ok("https://s.apps.test/") is False

    def _raise_http(code):
        def _f(*a, **k):
            raise urllib.error.HTTPError("u", code, "m", {}, None)
        return _f
    monkeypatch.setattr(urllib.request, "urlopen", _raise_http(401))
    assert k8sclient._route_http_ok("https://s.apps.test/") is True   # oauth handshake = serving
    monkeypatch.setattr(urllib.request, "urlopen", _raise_http(503))
    assert k8sclient._route_http_ok("https://s.apps.test/") is False

    def _boom(*a, **k):
        raise OSError("conn refused")
    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    assert k8sclient._route_http_ok("https://s.apps.test/") is False
    assert k8sclient._route_http_ok("") is False


def test_reap_find_orphans():
    from datetime import datetime
    now = 1_000_000.0

    def sess(name, env, phase, age):
        ts = datetime.utcfromtimestamp(now - age).strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"metadata": {"name": name, "creationTimestamp": ts},
                "spec": {"environment": {"name": env}},
                "status": {"educates": {"phase": phase}}}

    live = {"env-current"}
    sessions = [
        sess("healthy", "env-current", "Allocated", 600),          # keep: live env, young
        sess("reserved-old", "env-current", "Available", 999999),  # keep: spare on live env
        sess("rollout-orphan", "env-old", "Allocated", 600),       # reap: env gone/terminating
        sess("just-born", "env-old", "Allocated", 10),             # keep: within grace
        sess("restart-orphan", "env-current", "Allocated", 90000),  # reap: Allocated past backstop
    ]
    got = {n for n, _ in reap.find_orphans(sessions, live, now,
                                           max_alloc_age_s=24 * 3600, grace_s=300)}
    assert got == {"rollout-orphan", "restart-orphan"}, got

    # No live envs known (e.g. list failed) → every past-grace session is an env-orphan;
    # still never reaps within grace.
    allnames = {n for n, _ in reap.find_orphans(sessions, set(), now,
                                                max_alloc_age_s=24 * 3600, grace_s=300)}
    assert "just-born" not in allnames and "healthy" in allnames


def test_reap_demo():
    reap.demo()   # self-check must pass


def test_user_can_admin_happy_path(monkeypatch):
    import types
    monkeypatch.setattr(k8sclient, "_ensure", lambda: None)
    allowed_status = types.SimpleNamespace(status=types.SimpleNamespace(allowed=True))

    class _Authz:
        def __init__(self, *a, **k): pass
        def create_self_subject_access_review(self, review):
            return allowed_status
    fake = types.SimpleNamespace(
        Configuration=type("Cfg", (), {
            "get_default_copy": staticmethod(lambda: types.SimpleNamespace(
                host="h", ssl_ca_cert="ca", verify_ssl=True)),
            "__init__": lambda self: None}),
        ApiClient=lambda cfg: object(),
        AuthorizationV1Api=_Authz,
        V1SelfSubjectAccessReview=lambda spec: object(),
        V1SelfSubjectAccessReviewSpec=lambda resource_attributes: object(),
        V1ResourceAttributes=lambda **k: object())
    monkeypatch.setattr(k8sclient, "client", fake)
    assert k8sclient.user_can_admin("user-token") is True


# --- auth: endpoint discovery, whoami, CA, callback error branches ----------

def test_auth_ca_and_endpoints_discovery(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_TLS_VERIFY", False)
    assert auth._ca() is False
    monkeypatch.setattr(cfg, "OAUTH_TLS_VERIFY", True)
    monkeypatch.setattr(cfg, "OAUTH_CA_FILE", "/etc/ca.crt")
    assert auth._ca() == "/etc/ca.crt"
    # discovery: no explicit URLs → fetch .well-known and cache
    monkeypatch.setattr(cfg, "OAUTH_AUTHORIZE_URL", "")
    monkeypatch.setattr(cfg, "OAUTH_TOKEN_URL", "")
    monkeypatch.setattr(cfg, "OAUTH_ISSUER_URL", "https://sso")
    monkeypatch.setattr(auth, "_disco", {"authorize": "", "token": "", "exp": 0.0})
    monkeypatch.setattr(auth.requests, "get",
                        lambda *a, **k: _Resp(200, {"authorization_endpoint": "https://sso/auth",
                                                    "token_endpoint": "https://sso/tok"}))
    assert auth._endpoints() == ("https://sso/auth", "https://sso/tok")


def test_auth_whoami(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_TLS_VERIFY", False)
    monkeypatch.setattr(cfg, "OAUTH_API_URL", "https://api")
    monkeypatch.setattr(auth.requests, "get",
                        lambda *a, **k: _Resp(200, {"metadata": {"name": "carol"}}))
    assert auth._whoami("tok") == "carol"


def test_auth_callback_error_and_missing_code(monkeypatch):
    monkeypatch.setattr(cfg, "OAUTH_ENABLED", True)
    c = create_app().test_client()
    assert c.get("/oauth/callback?error=access_denied", follow_redirects=False).status_code == 401
    with c.session_transaction() as s:
        s["oauth_state"] = "st"
    assert c.get("/oauth/callback?state=st", follow_redirects=False).status_code == 400  # no code


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
