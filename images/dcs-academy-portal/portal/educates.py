"""Educates portal REST client (backend-for-frontend).

We do NOT reimplement session allocation — Educates owns it. This wraps the
portal REST API with the robot credentials from TrainingPortal.status, so the
robot creds never touch the browser. The only calls we make:

  * token           — OAuth2 password grant (robot user) w/ HTTP-Basic client
  * catalog         — map a Workshop name → its environment name
  * request_session — allocate/return the caller's session, bound to the SSO
                      user (so a returning user resumes their own session)

The returned session `url` is a path under the portal host (academy); the
browser is 302-redirected there and the reverse-proxy (proxy.py) forwards it to
Educates, keeping the oauth_handshake host-consistent.
"""
import logging
import threading
import time

import requests

from . import config as cfg
from . import k8sclient

log = logging.getLogger("portal.educates")

_tok_lock = threading.Lock()
_tok = {"value": "", "exp": 0.0}

_readme_lock = threading.Lock()
_readme_cache = {}                    # url -> (text, exp)


class CapacityError(Exception):
    """Raised when the training portal has no capacity for a new session (HTTP
    503 from /request/). Carries the workshop so the UI can offer to free one."""
    def __init__(self, workshop):
        super().__init__(f"no session capacity for {workshop}")
        self.workshop = workshop


def _verify():
    return cfg.SESSION_TLS_VERIFY


def _creds():
    """(base_url, robot_user, robot_pass, client_id, client_secret) from status."""
    st = k8sclient.portal_status()
    cred = (st.get("credentials", {}) or {}).get("robot", {}) or {}
    clnt = (st.get("clients", {}) or {}).get("robot", {}) or {}
    return (k8sclient.portal_service_base(),
            cred.get("username", ""), cred.get("password", ""),
            clnt.get("id", ""), clnt.get("secret", ""))


def _token(base, ruser, rpass, cid, csec):
    now = time.time()
    with _tok_lock:
        if _tok["value"] and now < _tok["exp"]:
            return _tok["value"]
        r = requests.post(
            f"{base}/oauth2/token/",
            data={"grant_type": "password", "username": ruser, "password": rpass},
            auth=(cid, csec), verify=_verify(), timeout=10)
        r.raise_for_status()
        d = r.json()
        _tok["value"] = d["access_token"]
        # refresh a minute before expiry; default 12h if the portal omits it.
        _tok["exp"] = now + int(d.get("expires_in", 43200)) - 60
        return _tok["value"]


def _session():
    base, ruser, rpass, cid, csec = _creds()
    if not (base and ruser and cid):
        raise RuntimeError("Educates robot credentials not available from TrainingPortal.status")
    s = requests.Session()
    s.verify = _verify()
    s.headers["Authorization"] = f"Bearer {_token(base, ruser, rpass, cid, csec)}"
    return base, s


def catalog():
    """List of environments the portal serves: [{name, workshop, ...}]."""
    base, s = _session()
    r = s.get(f"{base}/workshops/catalog/environments/", timeout=10)
    r.raise_for_status()
    return r.json().get("environments", [])


def _env_for(workshop_name):
    """Resolve the environment name hosting a given Workshop (fallback: name itself)."""
    for env in catalog():
        details = env.get("workshop", {}) or {}
        if details.get("name") == workshop_name or env.get("name") == workshop_name:
            return env.get("name")
    return workshop_name


def request_session(workshop_name, user):
    """Allocate/return the SSO user's session for a workshop.

    Returns {"name", "url", "user", ...}; `url` is a portal-host path to redirect
    the browser to. Bound to `user` so the same person resumes their session.
    """
    base, s = _session()
    env = _env_for(workshop_name)
    params = {"index_url": f"https://{_public_host()}/"}
    if user:
        params["user"] = user
    r = s.get(f"{base}/workshops/environment/{env}/request/", params=params, timeout=30)
    if r.status_code == 503:
        log.info("REQUEST-SESSION workshop=%s env=%s -> 503 (no capacity)", workshop_name, env)
        raise CapacityError(workshop_name)
    r.raise_for_status()
    data = r.json()
    log.info("REQUEST-SESSION workshop=%s env=%s user=%r -> name=%s url=%r",
             workshop_name, env, user, data.get("name"), data.get("url"))
    return data


# NB: no delete_session() here — Educates' delete view is GET + @login_required and
# authorizes only the session OWNER (allocated_session(name, request.user)). A robot
# POST is refused (403). Deletion is driven by the owner's browser straight to the
# proxied /workshops/session/<name>/delete/ (see my_sessions.html / over_limit.html).


def user_sessions(user):
    """The user's currently-active sessions, from the portal's OWN allocation DB
    (authoritative). The WorkshopSession CR only carries the owner while Allocated —
    WAITING/spare sessions have no owner — so the CR is not a reliable source.

    GET /workshops/user/<user>/sessions/ (robot-authed; the robot is in the 'robots'
    group Educates requires). Returns [{name, namespace, workshop, environment,
    started, expires, countdown, ...}] — only non-stopped sessions owned by the user."""
    if not user:
        return []
    base, s = _session()
    r = s.get(f"{base}/workshops/user/{user}/sessions/", timeout=10)
    r.raise_for_status()
    return r.json().get("sessions", []) or []


def terminate_session(name):
    """Hard-delete a session: deletes the WorkshopSession CR + frees the portal DB
    record (Educates schedules `delete_workshop_session`). GET /workshops/session/
    <name>/terminate/ — robot-authed (`@protected_resource`); the robot is in the
    'robots' group so it may terminate ANY allocated session, unlike the owner-only
    /delete/ view (which needs the user's browser cookie and 403s the robot). The
    CALLER must enforce ownership. Educates 400s if the session isn't in use."""
    base, s = _session()
    r = s.get(f"{base}/workshops/session/{name}/terminate/", timeout=15)
    log.info("TERMINATE-SESSION %s -> %s", name, r.status_code)
    r.raise_for_status()
    return True


def fetch_readme(url, ttl=300):
    """Fetch a lab's README markdown (raw git URL), cached. '' on any failure so
    the course view degrades to the CR description."""
    if not url:
        return ""
    now = time.time()
    with _readme_lock:
        hit = _readme_cache.get(url)
        if hit and now < hit[1]:
            return hit[0]
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        text = r.text
    except requests.RequestException as e:
        log.info("README fetch failed %s: %s", url, e)
        text = ""
    with _readme_lock:
        _readme_cache[url] = (text, now + ttl)
    return text


def _public_host():
    """The academy host Educates should send the user back to (from status.url)."""
    st = k8sclient.portal_status()
    url = st.get("url", "")
    return url.split("://", 1)[-1].rstrip("/") if url else ""


def rest_session_status(name):
    """Educates REST view of a session's status (phase). CR is the primary source;
    this is a fallback / cross-check."""
    try:
        base, s = _session()
        r = s.get(f"{base}/workshops/session/{name}/status/", timeout=10)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, RuntimeError):
        return {}
