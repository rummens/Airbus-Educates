"""Portal-owned OpenShift OAuth login (replaces the oauth-proxy sidecar).

The portal IS the OAuth client (ServiceAccount-as-OAuthClient). Authorization-code
flow, hand-rolled on `requests` (no extra dep):

  browser → /login → 302 to OpenShift /oauth/authorize
          → /oauth/callback?code=… → POST /oauth/token (client_id + SA-token secret)
          → GET users/~ with the access token → stash {user, token} in the signed
            Flask session cookie.

Downstream, _user()/_token() read that cookie. Because the browser now holds a
real portal session cookie, the Educates session-host oauth_handshake (which the
reverse-proxy forwards on the academy host) is authenticated too — the same cookie
that gated the landing page gates the session paths, no header bridge needed.

CSRF: a random `state` is kept in the session and checked on callback.
"""
import logging
import secrets
import threading
import time
import urllib.parse

import requests
from flask import Blueprint, redirect, request, session, url_for, abort

from . import config as cfg

log = logging.getLogger("portal.auth")
bp = Blueprint("auth", __name__)

_disco_lock = threading.Lock()
_disco = {"authorize": "", "token": "", "exp": 0.0}


def _ca():
    """CA/verify for server-side calls. False on dev (self-signed), else the SA CA."""
    if not cfg.OAUTH_TLS_VERIFY:
        return False
    return cfg.OAUTH_CA_FILE or True


def _client_secret():
    with open(cfg.OAUTH_CLIENT_SECRET_FILE) as f:
        return f.read().strip()


def _endpoints():
    """(authorize_url, token_url). Explicit overrides win; else discover + cache."""
    if cfg.OAUTH_AUTHORIZE_URL and cfg.OAUTH_TOKEN_URL:
        return cfg.OAUTH_AUTHORIZE_URL, cfg.OAUTH_TOKEN_URL
    now = time.time()
    with _disco_lock:
        if _disco["authorize"] and now < _disco["exp"]:
            return _disco["authorize"], _disco["token"]
        r = requests.get(f"{cfg.OAUTH_ISSUER_URL}/.well-known/oauth-authorization-server",
                         verify=_ca(), timeout=10)
        r.raise_for_status()
        d = r.json()
        _disco["authorize"] = cfg.OAUTH_AUTHORIZE_URL or d["authorization_endpoint"]
        _disco["token"] = cfg.OAUTH_TOKEN_URL or d["token_endpoint"]
        _disco["exp"] = now + 3600
        return _disco["authorize"], _disco["token"]


def _whoami(access_token):
    """Resolve the username from the obtained token (OpenShift users/~)."""
    r = requests.get(f"{cfg.OAUTH_API_URL}/apis/user.openshift.io/v1/users/~",
                     headers={"Authorization": f"Bearer {access_token}"},
                     verify=_ca(), timeout=10)
    r.raise_for_status()
    name = (r.json().get("metadata", {}) or {}).get("name", "")
    # This exact string is the session owner the portal hands to Educates on launch and
    # matches against in My Sessions. Log it so an empty/blank My Sessions can be traced
    # to an identity that differs from the owner Educates stored.
    log.info("WHOAMI resolved identity=%r", name)
    return name


def current_user():
    return session.get("user", "") if cfg.OAUTH_ENABLED else ""


def current_token():
    return session.get("token", "") if cfg.OAUTH_ENABLED else ""


@bp.route("/login")
def login():
    if not cfg.OAUTH_ENABLED:
        return redirect(url_for("index"))
    authorize_url, _ = _endpoints()
    state = secrets.token_urlsafe(24)
    session["oauth_state"] = state
    # Where to send the user back to after login (same-origin path only).
    nxt = request.args.get("next", "/")
    session["oauth_next"] = nxt if nxt.startswith("/") else "/"
    q = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": cfg.OAUTH_CLIENT_ID,
        "redirect_uri": cfg.OAUTH_REDIRECT_URL,
        "scope": cfg.OAUTH_SCOPE,
        "state": state,
    })
    return redirect(f"{authorize_url}?{q}")


@bp.route("/oauth/callback")
def callback():
    if not cfg.OAUTH_ENABLED:
        return redirect(url_for("index"))
    if request.args.get("error"):
        abort(401, request.args.get("error_description", request.args["error"]))
    if not request.args.get("state") or request.args.get("state") != session.pop("oauth_state", None):
        abort(400, "oauth state mismatch")
    code = request.args.get("code")
    if not code:
        abort(400, "missing code")
    _, token_url = _endpoints()
    r = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": cfg.OAUTH_REDIRECT_URL,
        "client_id": cfg.OAUTH_CLIENT_ID,
        "client_secret": _client_secret(),
    }, headers={"Accept": "application/json"}, verify=_ca(), timeout=15)
    r.raise_for_status()
    access_token = r.json().get("access_token", "")
    if not access_token:
        abort(401, "no access_token from oauth server")
    session["token"] = access_token
    session["user"] = _whoami(access_token)
    session.permanent = True
    return redirect(session.pop("oauth_next", "/"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
