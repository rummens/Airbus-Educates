"""DCS Academy portal — Flask app (UI + BFF + reverse-proxy in one image).

Custom routes own the landing experience; proxy.bp forwards the Educates session
runtime paths. Order matters: custom routes are registered first, the proxy
blueprint last (it only claims allowlisted prefixes, else 404).
"""
import logging
import os
import re
import time

import markdown as md
from flask import (Flask, render_template, request, redirect, abort, jsonify,
                   Response, url_for)
from markupsafe import Markup

from . import config as cfg
from . import k8sclient, educates, feedback, metrics, proxy, auth
from .icons import ICONS, DIFFICULTY_ICON, resolve_icon

STEPS = ["Reserving session", "Starting virtual cluster", "Starting workshop pod",
         "Loading content", "Ready"]


def _steps_for(vcluster):
    """Loading steps for a launch. Non-vcluster labs run in a plain namespace, so
    the second step must say 'namespace', not 'virtual cluster' (task: stay true)."""
    s = list(STEPS)
    s[1] = "Starting virtual cluster" if vcluster else "Setting up namespace"
    return s


def _render_md(text):
    """Render trusted README markdown → safe HTML for the course view. Source is
    our own repo (git), rendered server-side; tables/fenced code enabled."""
    if not text:
        return ""
    return Markup(md.markdown(text, extensions=["fenced_code", "tables", "toc", "sane_lists"]))

# Endpoints reachable WITHOUT a login session. auth.* drive the login; health
# probes are kubelet; /analytics is the Educates webhook (server-to-server, no
# cookie); static assets must load on the login page itself.
_PUBLIC_ENDPOINTS = {"auth.login", "auth.callback", "auth.logout",
                     "healthz", "readyz", "analytics", "static"}


def _user():
    # OAuth identity in prod; a fixed dev identity locally (OAuth off) so per-user
    # progress/trophies bind to someone and persist across sessions.
    return auth.current_user() or cfg.DEV_USER


def _token():
    return auth.current_token()


def create_app():
    app = Flask(__name__)
    # Force INFO logging to stdout (gunicorn captures it). Debug the session-open
    # chain: every request in/out, user identity, proxied upstream status.
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    log = logging.getLogger("portal")

    # Signed session cookie (login identity + token). A stable secret from a Secret
    # keeps sessions valid across restarts/replicas; fall back to ephemeral for dev.
    app.secret_key = cfg.SESSION_SECRET or os.urandom(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                      SESSION_COOKIE_SECURE=True)
    app.register_blueprint(auth.bp)

    @app.before_request
    def _require_login():
        if not cfg.OAUTH_ENABLED or auth.current_user():
            return None
        if request.endpoint in _PUBLIC_ENDPOINTS:
            return None
        # No session yet → start the OpenShift OAuth dance, returning here after.
        return redirect(url_for("auth.login", next=request.full_path.rstrip("?")))

    @app.before_request
    def _log_req():
        log.info("REQ %s %s user=%r cookies=%s", request.method, request.full_path,
                 _user(), sorted(request.cookies.keys()))

    @app.after_request
    def _log_resp(resp):
        loc = resp.headers.get("Location", "")
        setc = len(resp.headers.getlist("Set-Cookie"))
        log.info("RESP %s %s -> %s loc=%r set-cookie=%d",
                 request.method, request.path, resp.status_code, loc, setc)
        return resp

    try:
        feedback.init_db()
    except Exception as e:            # noqa: BLE001 — DB may be absent in pure-UI local dev
        app.logger.warning("feedback DB init failed (continuing): %s", e)

    # Boot diagnostics: where we will talk to the Educates training-portal REST API.
    # Logs the configured override + the resolved in-cluster Service base (best-effort;
    # the resolve reads TrainingPortal.status, which may not exist yet at boot).
    if not cfg.DEMO:
        log.info("BOOT educates portal=%s cr-namespace=%s service-url=%r",
                 cfg.PORTAL_NAME, cfg.PORTAL_CR_NAMESPACE, cfg.PORTAL_SERVICE_URL or "(derive)")
        try:
            log.info("BOOT educates REST base resolved to %s", k8sclient.portal_service_base())
        except Exception as e:        # noqa: BLE001
            log.info("BOOT educates REST base not resolvable yet: %s", e)

    @app.context_processor
    def _inject():
        return {"theme": cfg.THEME, "icon": _icon, "product": cfg.THEME["product_name"],
                "current_user": _user()}

    @app.template_filter("de")
    def _de(ts):
        """UTC/ISO (or a datetime from psycopg) → German date-time, Europe/Berlin."""
        from datetime import datetime, timezone
        try:
            from zoneinfo import ZoneInfo
            tz = ZoneInfo("Europe/Berlin")
        except Exception:             # noqa: BLE001
            tz = timezone.utc
        if not ts:
            return ""
        dt = ts if isinstance(ts, datetime) else datetime.fromisoformat(str(ts))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(tz).strftime("%d.%m.%Y %H:%M")

    def _icon(name, cls="ic"):
        svg = ICONS.get(name) or ICONS.get(resolve_icon(name, "dot"), ICONS["dot"])
        return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>')

    # --- catalog ------------------------------------------------------------
    @app.route("/")
    def index():
        tracks = k8sclient.list_tracks()
        courses = k8sclient.list_courses()
        ratings = _ratings_safe()
        progress = _progress_safe(_user())
        by_track = {}
        for c in courses:
            by_track.setdefault(c["track"], []).append(c)
        track_names = {t["name"] for t in tracks}
        # Only render courses in a declared track. Uncategorised ones are hidden
        # (kept startable by URL) rather than shown in a ragged "More" section.
        sections = [dict(t, courses=by_track.get(t["name"], [])) for t in tracks]
        hidden = sum(len(v) for k, v in by_track.items() if k not in track_names)
        # "Continue where you left off"
        cont = feedback.last_in_progress(_user()) if not cfg.DEMO else None
        cont_course = next((c for c in courses if c["name"] == cont), None)
        return render_template("index.html", sections=sections, ratings=ratings,
                               min_reviews=cfg.FEEDBACK_MIN_REVIEWS, is_admin=_is_admin(),
                               difficulty_icon=DIFFICULTY_ICON, progress=progress,
                               stats=_catalog_stats(courses, tracks), hidden=hidden,
                               cont=cont_course, banner=_banner(),
                               trophies=_trophies(_user(), courses, tracks))

    @app.route("/trophies")
    def trophies():
        courses = k8sclient.list_courses()
        tracks = k8sclient.list_tracks()
        return render_template("trophies.html", is_admin=_is_admin(),
                               trophies=_trophies(_user(), courses, tracks))

    @app.route("/course/<name>")
    def course(name):
        c = next((x for x in k8sclient.list_courses() if x["name"] == name), None)
        if not c:
            abort(404)
        ratings = _ratings_safe()
        # Rich description = the lab's README.md (markdown), fetched from its git
        # source; falls back to the CR description if unavailable.
        readme = _safe(lambda: educates.fetch_readme(c.get("readme_url", ""))) or ""
        return render_template("course.html", c=c, ratings=ratings,
                               min_reviews=cfg.FEEDBACK_MIN_REVIEWS, is_admin=_is_admin(),
                               difficulty_icon=DIFFICULTY_ICON, readme_html=_render_md(readme),
                               status=_progress_safe(_user()).get(name, ""))

    # --- launch / provisioning ---------------------------------------------
    @app.route("/launch/<name>")
    def launch(name):
        c = next((x for x in k8sclient.list_courses() if x["name"] == name), None)
        if not c:
            abort(404)
        steps = _steps_for(c.get("vcluster"))
        try:
            sess = educates.request_session(name, _user())
            metrics.REQUESTS.labels(name, "ok").inc()
            _safe(lambda: feedback.mark_progress(_user(), name, "started"))
        except educates.CapacityError:
            # Portal is at its session limit → don't dump a raw 503. Show the running
            # sessions and let the user free one (task: clear error + self-service).
            metrics.REQUESTS.labels(name, "error").inc()
            running = _safe(lambda: k8sclient.sessions_for_workshop(name)) or []
            return render_template("over_limit.html", course=c, sessions=running,
                                   is_admin=_is_admin()), 503
        except Exception as e:        # noqa: BLE001
            metrics.REQUESTS.labels(name, "error").inc()
            metrics.ERRORS.labels("session_request").inc()
            return render_template("launch.html", course=c, error=str(e),
                                   session_name="", target="", steps=steps, t0=0), 502
        target = _abs_session_url(sess.get("url", ""))
        return render_template("launch.html", course=c, error="",
                               session_name=sess.get("name", ""), target=target,
                               steps=steps, t0=int(time.time()))

    @app.route("/session/<name>/delete", methods=["POST"])
    def session_delete(name):
        """Free a running session (from the over-capacity page), then retry launch."""
        _safe(lambda: educates.delete_session(name))
        nxt = request.form.get("next", "")
        return redirect(nxt if nxt.startswith("/") else url_for("index"))

    @app.route("/api/session/<name>/status")
    def session_status(name):
        return jsonify(_status_feed(name, request.args.get("t0", type=int)))

    # --- feedback (absorbed) -----------------------------------------------
    @app.route("/form")
    def form():
        return render_template("form.html",
                               workshop=request.args.get("workshop", ""),
                               session=request.args.get("session", ""))

    @app.route("/feedback", methods=["POST"])
    def submit_feedback():
        f = request.form
        feedback.insert(f.get("workshop"), f.get("session"), "form",
                        f.get("rating"), f.get("clarity"), f.get("comment"))
        # Submitting end-of-lab feedback marks the workshop completed for the user.
        _safe(lambda: feedback.mark_progress(_user(), f.get("workshop"), "completed"))
        return render_template("thanks.html")

    @app.route("/analytics", methods=["POST"])
    def analytics():
        payload = request.get_json(silent=True) or {}
        parsed = feedback.parse_analytics(payload if isinstance(payload, dict) else {})
        if parsed:
            feedback.insert(parsed[0], parsed[1], "analytics", parsed[2], parsed[3], parsed[4])
        return ("", 204)

    # --- admin (SSAR-gated) -------------------------------------------------
    @app.route("/admin")
    def admin():
        if not _is_admin():
            abort(403)
        rows, overall = feedback.aggregates()
        return render_template("admin.html", rows=rows, overall=overall,
                               comments=feedback.comments(), sessions=_usage(),
                               banner=_banner(), is_admin=True)

    @app.route("/admin/banner", methods=["POST"])
    def admin_banner():
        """Set/clear the site-wide banner (maintenance / announcement)."""
        if not _is_admin():
            abort(403)
        _safe(lambda: feedback.set_setting("banner", request.form.get("banner", "").strip()[:500]))
        return redirect(url_for("admin"))

    @app.route("/help")
    def help_page():
        return render_template("help.html", is_admin=_is_admin())

    # --- ops ----------------------------------------------------------------
    @app.route("/healthz")
    @app.route("/livez")
    def healthz():
        return ("ok", 200)

    @app.route("/readyz")
    def readyz():
        try:
            k8sclient.ping()
            return ("ok", 200)
        except Exception:             # noqa: BLE001
            return ("not ready", 503)

    @app.route("/metrics")
    def metrics_ep():
        return Response(metrics.render(), mimetype="text/plain; version=0.0.4")

    # proxy LAST — only allowlisted Educates paths, everything else 404.
    app.register_blueprint(proxy.bp)
    return app


# --- helpers ---------------------------------------------------------------

def _safe(fn):
    try:
        return fn()
    except Exception:                 # noqa: BLE001 — progress/feedback are best-effort
        metrics.ERRORS.labels("feedback_db").inc()
        return None


def _banner():
    """Admin-set site banner text ('' = none). Best-effort."""
    return _safe(lambda: feedback.get_setting("banner", "")) or ""


def _pretty_module(mod):
    """'B-Developer' → 'Developer'; leaves a plain value untouched."""
    return mod.split("-", 1)[1] if "-" in mod and len(mod.split("-", 1)[0]) <= 2 else mod


def _trophies(user, courses, tracks=None):
    """Trophies from completed-lab progress. DYNAMIC: the per-module and per-track
    trophies are derived from the live Workshop CRs (module label) and Track CRs, so
    adding a new track/module + its labs grows the trophy set automatically — no code
    change. Each entry carries earned state, the requirement, and progress (done/need)."""
    done = {w for w, s in _progress_safe(user).items() if s == "completed"}
    total = len(courses)
    track_title = {t["name"]: t.get("title", t["name"]) for t in (tracks or [])}

    def group(key):
        g = {}
        for c in courses:
            g.setdefault(c.get(key) or "", []).append(c["name"])
        return {k: v for k, v in g.items() if k}

    def entry(key, title, icon, labs, detail):
        d = sum(1 for l in labs if l in done)
        return {"key": key, "title": title, "icon": icon, "detail": detail,
                "earned": bool(labs) and d == len(labs), "done": d, "need": len(labs)}

    items = [{"key": "first", "title": "First Lab", "icon": "trophy",
              "earned": len(done) >= 1, "detail": "Complete any one lab",
              "done": min(len(done), 1), "need": 1}]
    for mod, labs in sorted(group("module").items()):
        name = _pretty_module(mod)
        items.append(entry(f"module:{mod}", f"{name} Module", "medal", labs,
                           f"Complete all {len(labs)} labs in the {name} module"))
    for tr, labs in sorted(group("track").items()):
        title = track_title.get(tr, tr.title())
        label = title if "track" in title.lower() else f"{title} Track"
        items.append(entry(f"track:{tr}", label, "award", labs,
                           f"Complete all {len(labs)} labs in {title}"))
    if total:
        items.append({"key": "all", "title": "Academy Master", "icon": "star",
                      "earned": len(done) >= total, "detail": "Complete every lab in the academy",
                      "done": len(done), "need": total})
    return {"items": items, "earned": sum(t["earned"] for t in items),
            "done": len(done), "total": total}


def _ratings_safe():
    try:
        return feedback.ratings_by_workshop()
    except Exception:                 # noqa: BLE001
        return {}


def _progress_safe(user):
    # Progress/trophies bind to a user identity, not to cluster mode: with no user
    # there's nothing to read; with one (real OAuth user, or DEV_USER locally) return
    # their persisted progress even in DEMO so trophies work when iterating locally.
    if not user:
        return {}
    return _safe(lambda: feedback.user_progress(user)) or {}


_DUR = re.compile(r"(\d+(?:\.\d+)?)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes)?", re.I)


def _parse_minutes(text):
    """'45 min' → 45, '1 h' → 60, '1.5h' → 90, '90' → 90. 0 if unparseable."""
    if not text:
        return 0
    m = _DUR.search(str(text))
    if not m:
        return 0
    val = float(m.group(1))
    unit = (m.group(2) or "min").lower()
    return int(val * 60) if unit.startswith("h") else int(val)


def _catalog_stats(courses, tracks):
    mins = sum(_parse_minutes(c.get("duration")) for c in courses)
    hours = round(mins / 60) if mins else 0
    return {"workshops": len(courses), "tracks": len(tracks), "hours": hours}


def _is_admin():
    return k8sclient.user_can_admin(_token())


def _abs_session_url(path):
    """Educates returns a portal-host path; the browser hits it on academy (us),
    and the proxy forwards it. Return as-is if already absolute."""
    if not path or path.startswith("http"):
        return path
    return path if path.startswith("/") else "/" + path


def _status_feed(name, t0):
    """Merge WorkshopSession phase + pods → a human step + progress %."""
    st = k8sclient.session_status(name)
    phase = st.get("phase", "Pending")
    pods = k8sclient.session_pods(name)
    vc = [p for p in pods if p["vcluster"]]
    ws = [p for p in pods if not p["vcluster"]]
    vc_ready = bool(vc) and all(p["ready"] == p["total"] and p["total"] for p in vc)
    ws_ready = bool(ws) and all(p["ready"] == p["total"] and p["total"] for p in ws)

    # WorkshopSession.status.educates.phase for a live session is "Allocated"
    # (assigned) — "Running" is never reported here, so we key readiness off the
    # workshop pod being Ready + a session URL, gated to allocated/running phases.
    READY_PHASES = ("Running", "Allocated", "Available")
    url = st.get("url", "")
    # Only call the session truly Ready once its Route is admitted by the router —
    # otherwise the redirect hits the router's "Application is not available" page.
    # session_route_ready → True (admitted), False (not yet), or None (couldn't check,
    # e.g. no Routes RBAC). Fail OPEN on None so a missing check never hangs the launch.
    rr = _safe(lambda: k8sclient.session_route_ready(name, url)) if url else None
    route_ready = (rr is None) or bool(rr)
    step = "Reserving session"
    if phase in READY_PHASES and ws_ready and (vc_ready or not vc) and url and route_ready:
        step = "Ready"
    elif phase in READY_PHASES and ws_ready and (vc_ready or not vc) and url:
        step = "Waiting for route"
    elif ws_ready:
        step = "Loading content"
    elif ws:
        step = "Starting workshop pod"
    elif vc and not vc_ready:
        step = "Starting virtual cluster"
    ready = step == "Ready"
    if ready and t0:
        metrics.PROVISION.observe(max(0, time.time() - t0))
    # "Waiting for route" sits between Loading content and Ready — show it on the
    # last content step so the bar doesn't jump back to the start.
    idx = STEPS.index(step) if step in STEPS else (len(STEPS) - 2 if step == "Waiting for route" else 0)
    return {
        "phase": phase,
        "message": st.get("message", ""),
        "step": step,
        "index": idx,
        "total": len(STEPS),
        "ready": ready,
        "url": _abs_session_url(st.get("url", "")),
        "pods": [{"name": p["name"], "ready": f'{p["ready"]}/{p["total"]}',
                  "phase": p["phase"], "vcluster": p["vcluster"]} for p in pods],
    }


def _usage():
    """Running-session overview for the admin page."""
    out = []
    for s in k8sclient.list_sessions():
        stt = (s.get("status", {}) or {}).get("educates", {}) or {}
        spec = s.get("spec", {})
        out.append({
            "name": s["metadata"]["name"],
            "workshop": (spec.get("environment", {}) or {}).get("name", ""),
            "user": (spec.get("session", {}) or {}).get("username", ""),
            "phase": stt.get("phase", ""),
        })
    return out


app = create_app()
