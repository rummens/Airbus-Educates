#!/usr/bin/env python3
"""Runnable checks for the portal's non-trivial logic (no cluster needed).

    python3 test_portal.py     # asserts; prints "OK"

Covers: feedback sqlite roundtrip + aggregates + ratings threshold source,
analytics-webhook parsing, first-sentence summary fallback, and the demo
catalog / UI render path.
"""
import os
import tempfile

os.environ["PORTAL_DEMO"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ["FEEDBACK_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")

from portal import feedback, k8sclient       # noqa: E402


def test_feedback():
    feedback.init_db()
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


def test_progress():
    feedback.init_db()
    feedback.mark_progress("alice", "lab-a01", "started")
    feedback.mark_progress("alice", "lab-a02", "started")
    feedback.mark_progress("alice", "lab-a02", "completed")
    feedback.mark_progress("alice", "lab-a02", "started")   # must NOT downgrade
    p = feedback.user_progress("alice")
    assert p == {"lab-a01": "started", "lab-a02": "completed"}, p
    assert feedback.last_in_progress("alice") == "lab-a01"   # only non-completed
    assert feedback.user_progress("") == {}                  # anon → empty


def test_parse_minutes():
    from portal.app import _parse_minutes, _catalog_stats
    assert _parse_minutes("45 min") == 45
    assert _parse_minutes("1 h") == 60
    assert _parse_minutes("1.5h") == 90
    assert _parse_minutes("") == 0
    s = _catalog_stats([{"duration": "30 min"}, {"duration": "1 h"}], [{}, {}])
    assert s == {"workshops": 2, "tracks": 2, "hours": 2}, s


def test_icon_resolve():
    from portal.icons import resolve_icon
    assert resolve_icon("fa-cube") == "box"
    assert resolve_icon("network-wired") == "network"
    assert resolve_icon("box") == "box"
    assert resolve_icon("nonsense", default="book") == "book"


def test_analytics_parse():
    p = feedback.parse_analytics(
        {"event": {"name": "workshop.rating", "data": {"score": 5}}, "workshop": {"name": "lab-a03"}})
    assert p == ("lab-a03", None, 5, None, None), p
    assert feedback.parse_analytics({"event": {"name": "session.started"}}) is None


def test_summary_fallback():
    assert k8sclient._first_sentence("First. Second.") == "First."
    assert k8sclient._first_sentence("No punctuation here") == "No punctuation here"
    assert k8sclient._first_sentence("") == ""


def test_prettify_title():
    assert k8sclient._prettify("lab-a02-kubernetes-essentials") == "Kubernetes Essentials"
    assert k8sclient._prettify("lab-3-storage") == "Storage"
    assert k8sclient._prettify("harbor-registry") == "Harbor Registry"


def test_demo_and_render():
    assert len(k8sclient.list_courses()) == 3
    assert len(k8sclient.list_tracks()) == 2
    from portal.app import create_app
    app = create_app()
    c = app.test_client()
    assert c.get("/").status_code == 200
    assert b"DCS" in c.get("/").data
    assert c.get("/course/lab-a02-kubernetes-essentials").status_code == 200
    assert c.get("/healthz").status_code == 200
    assert c.get("/metrics").status_code == 200
    assert c.get("/course/nope").status_code == 404
    assert c.get("/admin").status_code == 403           # no token → SSAR denies
    # a random path is neither a UI route nor an allowlisted proxy path → 404
    assert c.get("/totally/unknown").status_code == 404


if __name__ == "__main__":
    test_feedback()
    test_progress()
    test_parse_minutes()
    test_icon_resolve()
    test_analytics_parse()
    test_summary_fallback()
    test_prettify_title()
    test_demo_and_render()
    print("OK")
