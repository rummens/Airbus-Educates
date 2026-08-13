"""DCS Academy portal — Flask app (UI + BFF + reverse-proxy in one image).

Custom routes own the landing experience; proxy.bp forwards the Educates session
runtime paths. Order matters: custom routes are registered first, the proxy
blueprint last (it only claims allowlisted prefixes, else 404).
"""
import csv
import io
import logging
import os
import re
import secrets
import time

import markdown as md
from flask import (Flask, render_template, request, redirect, abort, jsonify,
                   Response, url_for, session, g)
from markupsafe import Markup

from urllib.parse import urljoin, urlsplit

from . import config as cfg
from . import (auth, cache, consolelab, educates, feedback, k8sclient, metrics,
               proxy, slides)
from .icons import ICONS, DIFFICULTY_ICON, resolve_icon

_log = logging.getLogger("portal")

STEPS = ["Reserving session", "Starting virtual cluster", "Starting workshop pod",
         "Loading content", "Ready"]


def _steps_for(vcluster):
    """Loading steps for a launch. Non-vcluster labs run in a plain namespace, so
    the second step must say 'namespace', not 'virtual cluster' (task: stay true)."""
    s = list(STEPS)
    s[1] = "Starting virtual cluster" if vcluster else "Setting up namespace"
    return s


def _render_md(text, breaks=False):
    """Render trusted markdown → safe HTML. Source is our own repo/admins,
    rendered server-side; tables/fenced code enabled. breaks=True adds nl2br so a
    single newline becomes <br> (banner: admins type plain lines, not markdown
    paragraphs) — off for READMEs, whose hard-wrapped prose must NOT break per line."""
    if not text:
        return ""
    exts = ["fenced_code", "tables", "toc", "sane_lists"]
    if breaks:
        exts.append("nl2br")
    return Markup(md.markdown(text, extensions=exts))

# Endpoints reachable WITHOUT a login session. auth.* drive the login; health
# probes are kubelet; /analytics is the Educates webhook (server-to-server, no
# cookie); admin_rescan is the workshops-chart PostSync Job (server-to-server, it
# self-gates on the PORTAL_RESCAN_TOKEN bearer) — without this the login gate 302s
# the Job to the OAuth login page instead of letting its token be checked; static
# assets must load on the login page itself.
_PUBLIC_ENDPOINTS = {"auth.login", "auth.callback", "auth.logout",
                     "healthz", "readyz", "analytics", "admin_rescan", "static"}


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
    # SameSite=None (default) so the cookie rides the cross-origin oauth_handshake
    # from the embedded Console/Editor session subdomains; requires Secure.
    app.config.update(SESSION_COOKIE_HTTPONLY=True,
                      SESSION_COOKIE_SAMESITE=cfg.SESSION_COOKIE_SAMESITE,
                      SESSION_COOKIE_SECURE=True)
    app.register_blueprint(auth.bp)
    app.register_blueprint(slides.bp)

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
                "current_user": _user(), "preview": _preview()}

    @app.template_filter("firstname")
    def _firstname(user):
        """Greet by first name only. Some clusters hand back an email or
        firstName.lastName as the username; 'john.doe@corp.com' → 'John'."""
        if not user:
            return ""
        return (user.split("@", 1)[0].split(".", 1)[0] or user).title()

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

    @app.template_filter("mins")
    def _mins(v):
        """Minutes (float) → '42 min' / '3 h 07 min'. '—' when unknown."""
        if v is None:
            return "—"
        m = int(round(v))
        return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{m} min"

    @app.template_filter("pct")
    def _pct(v):
        return "—" if v is None else f"{v:.0f}%"

    def _icon(name, cls="ic"):
        svg = ICONS.get(name) or ICONS.get(resolve_icon(name, "dot"), ICONS["dot"])
        return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>')

    # --- catalog ------------------------------------------------------------
    # A track can be closed while its labs are still being written: the catalog greys
    # it out and a launch is refused. Anything other than an explicit "available" is
    # closed, so a typo in the CR keeps labs unpublished rather than publishing them.
    TRACK_BADGE = {"coming-soon": "In preparation", "disabled": "Not available yet"}

    def _track_availability(track_id):
        track = next((t for t in k8sclient.list_tracks() if t["name"] == track_id), None)
        return (track or {}).get("availability", "available")

    def _track_open(track_id):
        # Admin preview overrides a closed track so we can review an unpublished
        # track's labs end-to-end before publishing it. Learners are unaffected —
        # the flag only exists in an admin's own signed session cookie.
        return _track_availability(track_id) == "available" or _preview()

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
                               track_badge=TRACK_BADGE,
                               min_reviews=cfg.FEEDBACK_MIN_REVIEWS, is_admin=_is_admin(),
                               difficulty_icon=DIFFICULTY_ICON, progress=progress,
                               stats=_catalog_stats(courses, tracks), hidden=hidden,
                               cont=cont_course, banner=_render_md(_banner(), breaks=True),
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
        log.info("COURSE %s: readme_url=%r vcluster=%s", name, c.get("readme_url"), c.get("vcluster"))
        readme = _safe(lambda: educates.fetch_readme(c.get("readme_url", ""))) or ""
        if not readme:
            # Pinpoint why: dump the CR's actual file sources (git vs image, host, ref).
            log.info("COURSE %s: empty README, CR file sources=%s",
                     name, k8sclient.workshop_file_sources(name))
        # Drop the README's own leading H1 — the view already prints the course title
        # as the page <h1> from the CR, so keeping the README title double-headlines it.
        readme = re.sub(r"^#\s+.*$\n?", "", readme, count=1, flags=re.M)
        availability = _track_availability(c.get("track"))
        return render_template("course.html", c=c, ratings=ratings,
                               track_open=_track_open(c.get("track")),
                               track_badge=TRACK_BADGE.get(availability, ""),
                               min_reviews=cfg.FEEDBACK_MIN_REVIEWS, is_admin=_is_admin(),
                               difficulty_icon=DIFFICULTY_ICON, readme_html=_render_md(readme),
                               # academy.dcs/details is markdown (hence details_md) and was
                               # being printed escaped. A console lab has no README to fetch,
                               # so this annotation IS its prospectus — render it.
                               details_html=_render_md(c.get("details_md", "")),
                               status=_progress_safe(_user()).get(name, ""),
                               has_slides=slides.has_slides(name))

    # --- launch / provisioning ---------------------------------------------
    @app.route("/launch/<name>")
    def launch(name):
        c = next((x for x in k8sclient.list_courses() if x["name"] == name), None)
        if not c:
            abort(404)
        steps = _steps_for(c.get("vcluster"))
        # The button is disabled in the UI, but the URL is guessable — refuse here too,
        # or a closed track is only closed to people who do not type URLs.
        if not _track_open(c.get("track")):
            log.info("LAUNCH %s refused: track %r is %s", name, c.get("track"),
                     _track_availability(c.get("track")))
            return render_template(
                "launch.html", course=c,
                error="This track is not published yet, so its labs cannot be started.",
                session_name="", target="", steps=steps, t0=0), 403
        try:
            sess = educates.request_session(name, _user())
            metrics.REQUESTS.labels(name, "ok").inc()
            _safe(lambda: feedback.mark_progress(_user(), name, "started"))
        except educates.CapacityError:
            # Educates returns the same 503 whether the CALLER is at their per-user cap
            # or the whole portal is full. Those need different advice, so look at the
            # caller's own sessions: none of their own → the academy is full and sending
            # them to an empty My Sessions is just confusing.
            mine = _my_sessions(_user())
            log.info("LAUNCH %s refused: no capacity (user %r holds %d session(s))",
                     name, _user(), len(mine))
            metrics.REQUESTS.labels(name, "error").inc()
            return render_template("over_limit.html", course=c, is_admin=_is_admin(),
                                   mine=mine), 503
        except Exception as e:        # noqa: BLE001
            metrics.REQUESTS.labels(name, "error").inc()
            metrics.ERRORS.labels("session_request").inc()
            return render_template("launch.html", course=c, error=str(e),
                                   session_name="", target="", steps=steps, t0=0), 502
        session_name = sess.get("name", "")
        _safe(lambda: feedback.start_run(_user(), name, session_name))
        target = _abs_session_url(sess.get("url", ""))
        if consolelab.is_console_lab(c):
            # The console lab runs in the OpenShift console, not the Educates
            # dashboard. The session (namespace + its pre-deployed objects) is still
            # what we just allocated; we only redirect somewhere else. An empty
            # target here (no ConsoleLab annotation, no console Route) falls back to
            # the dashboard rather than sending the browser to a broken URL.
            console_target = consolelab.launch_url(
                c, k8sclient.session_namespace(session_name), k8sclient.console_base_url(),
                return_url=_return_url(name, session_name))
            if console_target:
                target = console_target
            else:
                log.warning("CONSOLE-LAB %s: no console target, falling back to the dashboard", name)
        return render_template("launch.html", course=c, error="",
                               session_name=session_name, target=target,
                               # Always the Educates activation URL: the browser must
                               # claim the allocation even when it then leaves for the
                               # console, or Educates reclaims the un-accessed session.
                               claim_url=_abs_session_url(sess.get("url", "")),
                               steps=steps, t0=int(time.time()),
                               console_lab=consolelab.is_console_lab(c))

    @app.route("/lab/<name>/complete")
    def lab_complete(name):
        """Where a console lab sends the learner when they press Finish.

        A console lab runs outside the portal, so this is the only moment the portal
        learns it happened: record the completion and free the environment (the lab is
        over — its namespace exists only for that run). Then hand off to the normal
        end-of-lab feedback form.

        GET, because it is reached by a plain browser navigation from the console.
        Terminating is gated on the session being the caller's OWN (same rule as
        /session/<name>/end), so the worst a forged link can do is end a lab session
        the visitor already owns.
        """
        c = next((x for x in k8sclient.list_courses() if x["name"] == name), None)
        if not c:
            abort(404)
        _safe(lambda: feedback.mark_progress(_user(), name, "completed"))
        _safe(lambda: feedback.finish_run(_user(), name))
        session_name = request.args.get("session", "")
        if session_name:
            mine = {s["name"] for s in _my_sessions(_user())}
            if session_name in mine or _is_admin():
                _safe(lambda: educates.terminate_session(session_name))
            else:
                log.warning("LAB-COMPLETE %s: session %r is not %r's — not terminating",
                            name, session_name, _user())
        return render_template("form.html", workshop=name, session=session_name)

    @app.route("/session/<name>/end", methods=["POST"])
    def session_end(name):
        """Hard-delete one of the user's own sessions (deletes the WorkshopSession CR
        + frees the DB) via the robot-authed terminate. The robot can terminate ANY
        session, so gate on ownership here: the name must be one of the caller's own
        sessions (or the caller is an admin)."""
        mine = {s["name"]: s for s in _my_sessions(_user())}
        if name not in mine and not _is_admin():
            abort(403)
        _safe(lambda: educates.terminate_session(name))
        # Deleting the session clears its in-progress marker so the tile/Continue
        # banner reset (a 'completed' lab stays completed — see clear_progress).
        ws = (mine.get(name) or {}).get("workshop", "")
        if ws:
            _safe(lambda: feedback.clear_progress(_user(), ws))
        return redirect(url_for("my_sessions"))

    @app.route("/my-sessions")
    def my_sessions():
        """The signed-in user's active sessions, with a delete/end button each."""
        return render_template("my_sessions.html", sessions=_my_sessions(_user()),
                               is_admin=_is_admin())

    @app.route("/api/session/<name>/status")
    def session_status(name):
        # vc=1 when the launched workshop uses a vcluster (authoritative, from the
        # launch page which read the course flag). Don't infer it from live pods —
        # early in provisioning the -vc pods don't exist yet.
        return jsonify(_status_feed(name, request.args.get("t0", type=int),
                                    request.args.get("vc") == "1",
                                    console_lab=request.args.get("console") == "1",
                                    user=_user()))

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
        # Terminal labs reach the form directly, so this is also where their run
        # gets its finished_at (console labs already have one — COALESCE keeps it).
        _safe(lambda: feedback.finish_run(_user(), f.get("workshop"), with_feedback=True))
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
                               usage=_run_stats(_safe(k8sclient.list_courses) or []),
                               banner=_banner(), is_admin=True)

    @app.route("/admin/feedback.csv")
    def admin_feedback_csv():
        """All comment rows, all columns — for offline triage in a spreadsheet."""
        if not _is_admin():
            abort(403)
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=feedback.COMMENT_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(feedback.comments(limit=None))
        return Response(buf.getvalue(), mimetype="text/csv", headers={
            "Content-Disposition": 'attachment; filename="dcs-academy-feedback.csv"'})

    @app.route("/admin/feedback/<int:fid>/done", methods=["POST"])
    def admin_feedback_done(fid):
        """Toggle the implemented/fixed flag on one comment.

        The admin page is long, so the button posts via fetch and gets 204 — a
        redirect would reload and throw the scroll position away. Plain form
        posts (no JS) still get the redirect."""
        if not _is_admin():
            abort(403)
        feedback.set_done(fid, request.form.get("done") == "1")
        if request.headers.get("X-Requested-With") == "fetch":
            return ("", 204)
        return redirect(url_for("admin") + "#comments")

    @app.route("/admin/banner", methods=["POST"])
    def admin_banner():
        """Set/clear the site-wide banner (maintenance / announcement)."""
        if not _is_admin():
            abort(403)
        _safe(lambda: feedback.set_setting("banner", request.form.get("banner", "").strip()[:2000]))
        return redirect(url_for("admin"))

    @app.route("/admin/preview", methods=["POST"])
    def admin_preview():
        """Toggle admin preview: start labs of tracks that are not published yet.

        Per-admin and per-session (a flag in the signed session cookie, cleared on
        logout), so turning it on never changes what a learner sees. The flag alone
        grants nothing — _preview() re-checks admin rights on every use."""
        if not _is_admin():
            abort(403)
        session["preview"] = not session.get("preview")
        log.info("PREVIEW %s -> %s", _user(), session["preview"])
        nxt = request.form.get("next", "")
        return redirect(nxt if nxt.startswith("/") else url_for("index"))

    @app.route("/admin/rescan", methods=["POST"])
    def admin_rescan():
        """Force an immediate catalog refresh. Called by the workshops chart's
        ArgoCD PostSync hook (in-cluster, hits the Service directly) so a Workshop/
        Track CR change shows up at once instead of after the TTL tick.

        Auth: a bearer token equal to PORTAL_RESCAN_TOKEN, OR an SSAR admin user
        (so it can also be wired to an admin-UI button later). If no token is
        configured, only the admin-user path works (the Job path is disabled)."""
        hdr = request.headers.get("Authorization", "")
        bearer = hdr[7:].strip() if hdr.startswith("Bearer ") else ""
        token_ok = bool(cfg.RESCAN_TOKEN) and secrets.compare_digest(bearer, cfg.RESCAN_TOKEN)
        if not (token_ok or _is_admin()):
            abort(403)
        names = cache.refresh_all()
        return jsonify({"status": "ok", "refreshed": names}), 200

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

    # Background refresh of the catalog + Workshop/Track CRs (keeps the
    # workshop→env map and CR lists warm + last-known-good, so a stale ref never
    # 404/503s a session launch). Skip in DEMO (no cluster/portal to poll).
    if not cfg.DEMO:
        cache.start_refresher(cfg.CATALOG_REFRESH_SECONDS)

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


def _trophies(user, courses, tracks=None):
    """Trophies from completed-lab progress. Two trophies are FIXED (First Lab,
    Academy Master); every other trophy is DYNAMIC — one per live Track CR, so
    adding a track + its labs grows the trophy set automatically, no code change.
    Each entry carries earned state, the requirement, and progress (done/need)."""
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


def _ts(v):
    """Stored timestamp → aware datetime (psycopg hands back datetime, sqlite ISO text)."""
    from datetime import datetime, timezone
    if not v:
        return None
    try:
        dt = v if isinstance(v, datetime) else datetime.fromisoformat(str(v))
    except ValueError:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


# A run open longer than this is a tab left open overnight, not lab time — counted
# as a run, excluded from the duration stats (and reported, so the number is honest).
MAX_RUN_SECONDS = 8 * 3600
RECENT_DAYS = 7


def _run_stats(courses):
    """Accumulating usage rollup from the runs table: funnel (started → finished →
    with feedback), distinct learners, time spent, and per-lab timings — the last
    being the number that should inform each lab's planned duration."""
    from datetime import datetime, timedelta, timezone
    rows = _safe(feedback.runs) or []
    titles = {c["name"]: c.get("title") or c["name"] for c in courses}
    planned = {c["name"]: _parse_minutes(c.get("duration")) for c in courses}
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)

    per_ws, per_user, users, recent = {}, {}, set(), set()
    started = finished = with_fb = outliers = 0
    for r in rows:
        ws = per_ws.setdefault(r["workshop"],
                               {"started": 0, "finished": 0, "fb": 0, "times": []})
        ws["started"] += 1
        started += 1
        users.add(r["username"])
        if r["finished_at"]:
            ws["finished"] += 1
            finished += 1
        if r["feedback_at"]:
            ws["fb"] += 1
            with_fb += 1
        t0, t1 = _ts(r["started_at"]), _ts(r["finished_at"] or r["feedback_at"])
        if t0 and t0 >= cutoff:
            recent.add(r["username"])
        if not (t0 and t1):
            continue                  # still running or abandoned — no duration to count
        secs = (t1 - t0).total_seconds()
        if secs <= 0:
            continue
        if secs > MAX_RUN_SECONDS:
            outliers += 1
            continue
        ws["times"].append(secs)
        per_user[r["username"]] = per_user.get(r["username"], 0) + secs

    labs = []
    for name, d in per_ws.items():
        xs = sorted(d["times"])
        n = len(xs)
        med = (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2) / 60 if n else None
        plan = planned.get(name) or 0
        labs.append({
            "workshop": name, "title": titles.get(name, name),
            "started": d["started"], "finished": d["finished"], "fb": d["fb"],
            "completion": (100.0 * d["finished"] / d["started"]) if d["started"] else None,
            "n": n,
            "median_min": med,
            "avg_min": (sum(xs) / n / 60) if n else None,
            "min_min": (xs[0] / 60) if n else None,
            "max_min": (xs[-1] / 60) if n else None,
            "planned_min": plan or None,
            # Median vs the CR's advertised duration: positive = the lab takes
            # longer than we tell learners it will.
            "delta_min": (med - plan) if (med is not None and plan) else None,
        })
    labs.sort(key=lambda r: (-r["started"], r["title"]))
    total_min = sum(per_user.values()) / 60
    return {
        "started": started, "finished": finished, "with_feedback": with_fb,
        "abandoned": started - finished,
        "users": len(users), "recent_users": len(recent), "recent_days": RECENT_DAYS,
        "runs_per_user": (started / len(users)) if users else None,
        "completion": (100.0 * finished / started) if started else None,
        "feedback_rate": (100.0 * with_fb / finished) if finished else None,
        "total_min": total_min,
        "avg_per_user_min": (total_min / len(per_user)) if per_user else None,
        "avg_per_run_min": (total_min / sum(l["n"] for l in labs)) if total_min else None,
        "timed": sum(l["n"] for l in labs), "outliers": outliers,
        "max_run_hours": MAX_RUN_SECONDS // 3600,
        "labs": labs,
    }


def _catalog_stats(courses, tracks):
    mins = sum(_parse_minutes(c.get("duration")) for c in courses)
    hours = round(mins / 60) if mins else 0
    return {"workshops": len(courses), "tracks": len(tracks), "hours": hours}


def _is_admin():
    return k8sclient.user_can_admin(_token())


def _preview():
    """True when an admin has switched preview on (see /admin/preview).

    Cookie flag first: for everyone else this is a dict lookup, so no extra SSAR
    call per request. The admin check is memoised per request (g) because the
    context processor and the launch route both ask."""
    if not session.get("preview"):
        return False
    if not hasattr(g, "preview_admin"):
        g.preview_admin = _is_admin()
    return g.preview_admin


def _abs_session_url(path):
    """Educates returns a portal-host path; the browser hits it on academy (us),
    and the proxy forwards it. Return as-is if already absolute."""
    if not path or path.startswith("http"):
        return path
    return path if path.startswith("/") else "/" + path


def _portal_base():
    """This portal's PUBLIC origin (scheme + host), no trailing slash.

    Deliberately not `request.url_root`: TLS terminates at the OpenShift route, and the
    app sees a plain-http request with no ProxyFix in front of it, so url_root advertises
    `http://…`. The console plugin honours a returnUrl only when its origin matches the
    configured portal URL exactly, so an http:// value is silently dropped and Finish
    stops returning the learner. The TrainingPortal status carries the real public URL;
    the OAuth redirect URL is the next best known-public value.
    """
    url = (_safe(k8sclient.portal_status) or {}).get("url", "").rstrip("/")
    if url:
        return url
    if cfg.OAUTH_REDIRECT_URL:
        parts = urlsplit(cfg.OAUTH_REDIRECT_URL)
        if parts.scheme and parts.netloc:
            return f"{parts.scheme}://{parts.netloc}"
    # Last resort: the request, forced to https — the portal is only served over TLS.
    return f"https://{request.host}"


def _return_url(course_name, session_name):
    """Absolute URL the console lab sends the learner back to when it completes: the
    completion route, which records progress and frees the session."""
    return urljoin(
        _portal_base() + "/",
        url_for("lab_complete", name=course_name, session=session_name))


def _status_feed(name, t0, expect_vc=False, console_lab=False, user=""):
    """Merge WorkshopSession phase + pods → a human step + progress %.

    expect_vc: this workshop uses a vcluster (from the course flag). When True the
    session is NOT ready until the -vc pods exist AND are ready. The old code
    inferred "needs vcluster" from whether -vc pods were currently present, so in
    the window before they spawn `vc` was empty and the gate `(vc_ready or not vc)`
    waved it straight through → "Waiting for virtual cluster" flashed by."""
    st = k8sclient.session_status(name)
    phase = st.get("phase", "Pending")
    pods = k8sclient.session_pods(name)
    vc = [p for p in pods if p["vcluster"]]
    ws = [p for p in pods if not p["vcluster"]]

    def _grp_ready(g):
        # Gate on the still-live pods; a Succeeded one-shot (e.g. a vcluster init
        # job) reports ready<total forever and must not block readiness.
        live = [p for p in g if p["phase"] != "Succeeded"]
        return bool(live) and all(p["ready"] == p["total"] and p["total"] for p in live)

    vc_ready = _grp_ready(vc)
    # Gate on Educates' own workshop pod, not on everything the lab deployed. A lab may
    # ship a pod that is MEANT to stay broken — "Diagnose a broken pod" hands the learner a
    # pod stuck in CreateContainerConfigError — and Educates labels session objects with
    # the session name, so such a pod lands in this list and pinned the launch at
    # "Starting workshop pod" forever. Fall back to every pod when none is identifiable,
    # so an Educates naming change degrades to the old behaviour rather than reporting
    # Ready while nothing runs.
    ws_ready = _grp_ready([p for p in ws if p.get("workshop")] or ws)
    # A vcluster lab gates on a real vc-ready; a plain-namespace lab ignores vc.
    vc_ok = vc_ready if expect_vc else True

    # WorkshopSession.status.educates.phase for a live session is "Allocated"
    # (assigned) — "Running" is never reported here, so we key readiness off the
    # workshop pod being Ready + a session URL, gated to allocated/running phases.
    READY_PHASES = ("Running", "Allocated", "Available")
    url = st.get("url", "")
    # Only call the session truly Ready once its Route is admitted AND actually serving
    # (not the router's "Application is not available" 503 page) — otherwise the redirect
    # lands there. session_route_ready → True/False. It only raises if the whole check
    # errors unexpectedly; _safe returns None then, and we fail OPEN so a broken check
    # never hangs the launch.
    # A console lab never opens the session dashboard, so whether its Route is
    # already served is irrelevant — probing it only adds latency (and on CRC the
    # session host needs an /etc/hosts entry, which the learner will never have).
    rr = None if console_lab else (_safe(lambda: k8sclient.session_route_ready(name, url)) if url else None)
    route_ready = (rr is None) or bool(rr)
    step = "Reserving session"
    if phase in READY_PHASES and ws_ready and vc_ok and url and route_ready:
        step = "Ready"
    elif phase in READY_PHASES and ws_ready and vc_ok and url:
        step = "Waiting for route"
    elif ws_ready and vc_ok:
        step = "Loading content"
    elif expect_vc and not vc_ready:
        step = "Starting virtual cluster"
    elif ws:
        step = "Starting workshop pod"
    ready = step == "Ready"
    if ready and t0:
        metrics.PROVISION.observe(max(0, time.time() - t0))
    # Grant the learner RBAC on their session namespace before the browser leaves
    # for the console. Idempotent, so re-polling after Ready costs one 409.
    access = None
    if ready and console_lab:
        # A lab can span more than one namespace (the two-project namespace-scope lab
        # gets a secondary session namespace). Bind the learner in each, or the console
        # opens on a project they cannot read.
        nss = _safe(lambda: k8sclient.session_lab_namespaces(name)) or []
        access = bool(nss) and all(
            bool(_safe(lambda ns=ns: k8sclient.ensure_lab_access(ns, user))) for ns in nss)
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
        # None for terminal labs; False means the console lab opens without the
        # learner holding RBAC on its namespace (chart grant missing) — the launch
        # page warns instead of silently handing over an empty-looking console.
        "access": access,
        "url": _abs_session_url(st.get("url", "")),
        "pods": [{"name": p["name"], "namespace": p["namespace"],
                  "ready": f'{p["ready"]}/{p["total"]}',
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
            # spec.session.username is empty; the real identity is status.educates.user
            # and the lab is spec.workshop.name (environment.name is the env, not the lab).
            "workshop": (spec.get("workshop", {}) or {}).get("name", "")
                        or (spec.get("environment", {}) or {}).get("name", ""),
            "user": stt.get("user", ""),
            "phase": stt.get("phase", ""),
        })
    return out


def _my_sessions(user):
    """The user's own active sessions → [{name, title, phase, url}].

    Two sources, unioned so one failing doesn't blank the page:
      * Educates portal DB (educates.user_sessions REST) — authoritative, includes
        WAITING/spare sessions, but depends on the robot being in the 'robots' group;
      * WorkshopSession CRs where status.educates.user == user — an ALLOCATED session
        (the running ones the user cares about here) carries its owner, and we already
        have list RBAC. This is the resilient fallback when the REST call 403s/empties.
    """
    if not user:
        return []
    mine = _safe(lambda: educates.user_sessions(user)) or []
    courses = {c["name"]: c for c in (_safe(k8sclient.list_courses) or [])}
    crs = {c["metadata"]["name"]: c for c in (_safe(k8sclient.list_sessions) or [])}

    rest_ws = {m.get("name", ""): m.get("workshop", "") for m in mine if m.get("name")}
    names = set(rest_ws)
    cr_owned = 0
    cr_owners = set()            # every owner string the live CRs carry (for diagnostics)
    ed_keys = []                 # field names under status.educates (owner may not be 'user')
    for name, cr in crs.items():
        stt = (cr.get("status", {}) or {}).get("educates", {}) or {}
        if stt and not ed_keys:
            ed_keys = sorted(stt.keys())
        owner = stt.get("user")
        if owner:
            cr_owners.add(owner)
        if owner == user:
            names.add(name)
            cr_owned += 1
    _log.info("MY-SESSIONS user=%r rest=%d cr-owned=%d total=%d", user, len(rest_ws), cr_owned, len(names))
    # Diagnostic for a blank My Sessions when sessions clearly exist: an empty result
    # is almost always an identity mismatch — the portal's `user` (an OAuth claim)
    # differs from the owner Educates stored (email vs username, case, domain), so
    # BOTH the REST lookup and the CR owner-match miss. Log both sides + the actual
    # status.educates field names (in case the owner isn't under 'user' on this build).
    if len(names) == 0 and len(crs) > 0:
        _log.warning("MY-SESSIONS EMPTY but %d WorkshopSession CR(s) exist — likely identity "
                     "mismatch. portal user=%r | CR owners=%r | status.educates keys=%r | "
                     "REST names=%r", len(crs), user, sorted(cr_owners), ed_keys, list(rest_ws))

    out = []
    for name in names:
        cr = crs.get(name) or {}
        stt = (cr.get("status", {}) or {}).get("educates", {}) or {}
        wsname = rest_ws.get(name) or (cr.get("spec", {}) or {}).get("workshop", {}).get("name", "")
        out.append({
            "name": name,
            "workshop": wsname,
            "title": (courses.get(wsname) or {}).get("title") or wsname or name,
            "phase": stt.get("phase", "") or "Running",
            "url": _abs_session_url(stt.get("url", "")),
        })
    out.sort(key=lambda x: x["title"])
    return out


app = create_app()
