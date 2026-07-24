"""Serve workshop slide decks outside a session.

A git-sync sidecar keeps a checkout of the workshops monorepo at cfg.SLIDES_ROOT.
Each slides-enabled lab ships workshop/slides/{index.html,slides.md} — the same
self-contained deck the in-session Slides tab uses. This blueprint serves that
directory on the portal host, so a learner can re-read a deck without starting a
container. git-sync re-pulls periodically, so new content appears with no pod
restart.

Login-gated like the rest of the portal (registered after auth.bp, before the
catch-all proxy). SLIDES_ROOT empty (no sidecar, e.g. local dev) → feature off.
"""
import glob
import os
import re

from flask import Blueprint, abort, redirect, send_from_directory, url_for

from . import config as cfg

bp = Blueprint("slides", __name__)
_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")   # lab dir/CR name; blocks path tricks


def slides_dir(name):
    """Absolute path to a lab's workshop/slides directory in the git-sync
    checkout, or None if the lab has no deck. Resolved by glob so it works
    regardless of how deep the lab sits under the tracks tree.

    ponytail: glob on every call. The checkout is small (a few dozen labs) and
    the OS caches the dir tree; add an lru_cache keyed on the git-sync SHA only
    if this ever shows up in a profile."""
    if not cfg.SLIDES_ROOT or not _NAME.match(name or ""):
        return None
    hits = glob.glob(os.path.join(cfg.SLIDES_ROOT, "**", name, "workshop", "slides", "index.html"),
                     recursive=True)
    return os.path.dirname(hits[0]) if hits else None


def has_slides(name):
    return slides_dir(name) is not None


@bp.route("/slides/<name>/")
def deck(name):
    d = slides_dir(name)
    if not d:
        abort(404)
    # index.html fetches 'slides.md' relatively, so the trailing slash matters —
    # Flask redirects /slides/<name> here automatically.
    return send_from_directory(d, "index.html")


@bp.route("/slides/<name>/<path:sub>")
def asset(name, sub):
    d = slides_dir(name)
    if not d:
        abort(404)
    return send_from_directory(d, sub)   # werkzeug safe_join blocks traversal
