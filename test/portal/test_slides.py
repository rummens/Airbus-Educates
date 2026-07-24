#!/usr/bin/env python3
"""Slides-serving tests (pytest, no cluster).

Covers portal/slides.py: resolving a lab's workshop/slides dir from the git-sync
checkout, the lab-name guard (blocks path tricks), and the /slides/<lab>/ routes
including traversal safety.
"""
import os
import tempfile

os.environ["PORTAL_DEMO"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ.setdefault("PORTAL_OAUTH_ENABLED", "false")   # routes not login-gated
os.environ["FEEDBACK_DB"] = os.path.join(tempfile.mkdtemp(), "t.db")

import pytest                                    # noqa: E402
from portal import slides                        # noqa: E402
from portal import config as cfg                 # noqa: E402
from portal.app import create_app                # noqa: E402

LAB = "lab-a01-deploy-first-app"


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    """A fake git-sync checkout with one slides-enabled lab nested under tracks/."""
    d = tmp_path / "workshops-monorepo" / "tracks" / "core-track" / LAB / "workshop" / "slides"
    d.mkdir(parents=True)
    (d / "index.html").write_text("<h1>deck</h1>")
    (d / "slides.md").write_text("# hi\n---\n## two")
    monkeypatch.setattr(cfg, "SLIDES_ROOT", str(tmp_path))
    return d


def test_slides_dir_resolves(checkout):
    assert slides.slides_dir(LAB) == str(checkout)
    assert slides.has_slides(LAB) is True


def test_slides_dir_absent(checkout):
    assert slides.slides_dir("lab-does-not-exist") is None
    assert slides.has_slides("lab-does-not-exist") is False


@pytest.mark.parametrize("bad", ["../etc", "a/b", "..", "", "UPPER", "a b"])
def test_slides_dir_rejects_bad_names(checkout, bad):
    assert slides.slides_dir(bad) is None


def test_slides_off_when_root_unset(monkeypatch):
    monkeypatch.setattr(cfg, "SLIDES_ROOT", "")
    assert slides.slides_dir(LAB) is None


def test_routes(checkout):
    c = create_app().test_client()
    # trailing-slash canonical form serves the deck; bare form redirects to it
    assert c.get(f"/slides/{LAB}/").status_code == 200
    assert c.get(f"/slides/{LAB}", follow_redirects=False).status_code in (301, 308)
    assert b"deck" in c.get(f"/slides/{LAB}/").data
    assert c.get(f"/slides/{LAB}/slides.md").status_code == 200
    assert c.get("/slides/lab-nope/").status_code == 404
    # traversal is blocked by werkzeug safe_join
    assert c.get(f"/slides/{LAB}/../../../../etc/passwd").status_code in (400, 404)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
