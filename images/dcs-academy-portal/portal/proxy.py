"""Transparent reverse-proxy for the Educates session runtime.

The crux (see HANDOVER-oauth-gating.md): Educates issues session URLs, cookies,
and CSP frame-ancestors for PORTAL_HOSTNAME=academy and does a browser-side
oauth_handshake back to that host. Since this app now *is* academy, it must
forward the Educates session/auth paths to the in-cluster training-portal
Service unchanged — otherwise every session breaks. Everything else 404s, so we
own the landing UI without re-exposing the Educates catalog UI.

ALLOWLIST is intentionally minimal. Under-proxy → sessions break; over-proxy →
the Educates UI leaks back. VERIFY the exact set against a live authenticated
session (watch which academy/… paths the session gateway hits) and adjust here.
"""
import logging

import requests
from flask import Blueprint, Response, request, abort

from . import config as cfg
from . import k8sclient

bp = Blueprint("proxy", __name__)
log = logging.getLogger("portal.proxy")

# Path PREFIXES forwarded to Educates. Keep this tight.
ALLOW_PREFIXES = (
    "/oauth2/",
    "/oauth_callback",
    "/workshops/session/",
    "/session/",
    "/workshops/environment/",
    "/workshops/catalog/",
)

# Hop-by-hop headers must not be forwarded (RFC 7230 §6.1).
_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
        "te", "trailers", "transfer-encoding", "upgrade", "content-length", "host"}


def is_proxied(path):
    return any(path == p or path.startswith(p) for p in ALLOW_PREFIXES)


def _academy_host():
    st = k8sclient.portal_status()
    url = st.get("url", "")
    return url.split("://", 1)[-1].rstrip("/") if url else request.host


@bp.route("/<path:_path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
def forward(_path):
    path = request.full_path[:-1] if request.full_path.endswith("?") else request.full_path
    raw_path = "/" + _path
    if not is_proxied(raw_path):
        abort(404)

    base = k8sclient.portal_service_base()
    host = _academy_host()
    # Educates builds its self-URLs/cookies from these; pin them to academy.
    headers = {k: v for k, v in request.headers if k.lower() not in _HOP}
    headers["Host"] = host
    headers["X-Forwarded-Host"] = host
    headers["X-Forwarded-Proto"] = "https"

    log.info("PROXY-> %s %s%s cookies=%s xfwd-user=%r xfwd-token=%s",
             request.method, base, path, sorted(request.cookies.keys()),
             headers.get("X-Forwarded-User", ""),
             bool(headers.get("X-Forwarded-Access-Token")))

    upstream = requests.request(
        method=request.method,
        url=base + path,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=True,
        verify=cfg.SESSION_TLS_VERIFY,
        timeout=60,
    )
    resp_headers = [(k, v) for k, v in upstream.raw.headers.items()
                    if k.lower() not in _HOP]
    log.info("PROXY<- %s %s -> %d loc=%r set-cookie=%d",
             request.method, path, upstream.status_code,
             upstream.headers.get("Location", ""),
             len(upstream.raw.headers.getlist("Set-Cookie")) if hasattr(upstream.raw.headers, "getlist") else 0)
    return Response(upstream.iter_content(chunk_size=8192),
                    status=upstream.status_code, headers=resp_headers)
