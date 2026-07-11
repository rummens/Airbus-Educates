#!/usr/bin/env python3
"""DCS Academy feedback collector.

Tiny stdlib-only HTTP service that collects end-of-workshop feedback (a 1-5
Likert rating, a 1-5 "clarity" rating, and an optional free-text comment) and
stores it in SQLite on a PersistentVolume. It also accepts the Educates
analytics webhook (one-click Likert buttons on the feedback page fire a
`report-analytics-event`, which the TrainingPortal POSTs here).

Endpoints:
  GET  /                     -> health/info (text)
  GET  /healthz              -> "ok"
  GET  /form                 -> HTML feedback form (?workshop=&session=)
  POST /feedback             -> store a form submission (urlencoded)
  POST /analytics            -> Educates analytics webhook sink (JSON)
  GET  /admin                -> HTML report: per-course + aggregate + comments
                                (requires ?token=<ADMIN_TOKEN> or Bearer token)
  GET  /metrics              -> Prometheus metrics (per-workshop avg/count)

Storage seam: SQLite by default (FEEDBACK_DB, default /data/feedback.db). To move
to CloudNativePG later, set DATABASE_URL=postgres://... — a psycopg backend is
stubbed in `_pg` (requires psycopg in the image; not bundled in v1).
# ponytail: SQLite + stdlib http.server is enough for one small form; swap to
# CNPG only if concurrency/HA actually demands it (DATABASE_URL is the seam).
"""
import html
import json
import os
import re
import sqlite3
import sys
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_PATH = os.environ.get("FEEDBACK_DB", "/data/feedback.db")
DATABASE_URL = os.environ.get("DATABASE_URL", "")          # set to postgres://... to swap backends
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
PRODUCT = os.environ.get("PRODUCT_NAME", "DCS Academy")
PORT = int(os.environ.get("PORT", "8080"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ts       TEXT    NOT NULL,
  workshop TEXT    NOT NULL,
  session  TEXT,
  source   TEXT    NOT NULL,            -- 'form' | 'analytics'
  rating   INTEGER,                     -- 1..5 overall
  clarity  INTEGER,                     -- 1..5 instructions clarity
  comment  TEXT
);
CREATE INDEX IF NOT EXISTS idx_feedback_workshop ON feedback(workshop);
"""


# --- storage -----------------------------------------------------------------

def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if DATABASE_URL.startswith("postgres"):
        # ponytail: postgres path deferred — build the image with psycopg and
        # implement _pg when CNPG is actually adopted. SQLite covers v1.
        raise SystemExit("DATABASE_URL set but the postgres backend is not built into this image")
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with _db() as c:
        c.executescript(SCHEMA)


def _clamp_score(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    return n if 1 <= n <= 5 else None


def insert(workshop, session, source, rating, clarity, comment):
    workshop = (workshop or "unknown").strip()[:200]
    session = (session or "").strip()[:200] or None
    comment = (comment or "").strip()[:4000] or None
    rating = _clamp_score(rating)
    clarity = _clamp_score(clarity)
    if rating is None and clarity is None and comment is None:
        return False                                        # nothing worth storing
    with _db() as c:
        c.execute(
            "INSERT INTO feedback(ts,workshop,session,source,rating,clarity,comment) "
            "VALUES(?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"),
             workshop, session, source, rating, clarity, comment),
        )
    return True


def aggregates():
    """Per-workshop and overall rollups."""
    with _db() as c:
        rows = c.execute(
            "SELECT workshop, COUNT(*) n, "
            "AVG(rating) avg_rating, COUNT(rating) n_rating, "
            "AVG(clarity) avg_clarity, COUNT(clarity) n_clarity, "
            "COUNT(comment) n_comment "
            "FROM feedback GROUP BY workshop ORDER BY workshop"
        ).fetchall()
        overall = c.execute(
            "SELECT COUNT(*) n, AVG(rating) avg_rating, AVG(clarity) avg_clarity, "
            "COUNT(comment) n_comment FROM feedback"
        ).fetchone()
    return rows, overall


def comments(limit=200):
    with _db() as c:
        return c.execute(
            "SELECT ts, workshop, rating, clarity, comment FROM feedback "
            "WHERE comment IS NOT NULL ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()


# --- rendering ---------------------------------------------------------------

def _esc(s):
    return html.escape(str(s if s is not None else ""))


def form_page(workshop, session):
    w, s = _esc(workshop), _esc(session)

    def radios(name):
        return "".join(
            f'<label><input type="radio" name="{name}" value="{i}" required>{i}</label>'
            for i in range(1, 6)
        )
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feedback — {_esc(PRODUCT)}</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 1rem;color:#1a2b45}}
 h1{{font-size:1.4rem}} fieldset{{border:1px solid #cbd5e0;border-radius:8px;margin:1rem 0;padding:1rem}}
 legend{{font-weight:600}} label{{margin-right:.9rem}} textarea{{width:100%;min-height:6rem}}
 button{{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:.6rem 1.2rem;font-size:1rem;cursor:pointer}}
 .muted{{color:#5a6b85;font-size:.9rem}}
 @media (prefers-color-scheme:dark){{body{{color:#e8eef7;background:#0f1729}}fieldset{{border-color:#33445c}}.muted{{color:#9fb0c8}}}}
</style></head><body>
<h1>Your feedback</h1>
<p class="muted">Workshop: <strong>{w or "(unspecified)"}</strong>. Takes 15 seconds — thank you.</p>
<form method="POST" action="/feedback">
 <input type="hidden" name="workshop" value="{w}">
 <input type="hidden" name="session" value="{s}">
 <fieldset><legend>How would you rate this workshop?</legend>{radios("rating")}</fieldset>
 <fieldset><legend>How clear were the instructions?</legend>{radios("clarity")}</fieldset>
 <fieldset><legend>Comments (optional)</legend>
  <textarea name="comment" placeholder="What worked well? What was confusing?"></textarea></fieldset>
 <button type="submit">Submit feedback</button>
</form></body></html>"""


def thanks_page():
    return ("<!doctype html><meta charset='utf-8'><title>Thanks</title>"
            "<body style='font-family:system-ui,sans-serif;max-width:640px;margin:3rem auto;text-align:center'>"
            "<h1>Thank you!</h1><p>Your feedback was recorded.</p></body>")


def admin_page():
    rows, overall = aggregates()

    def fmt(v):
        return f"{v:.2f}" if v is not None else "—"
    trs = "".join(
        f"<tr><td>{_esc(r['workshop'])}</td><td>{r['n']}</td>"
        f"<td>{fmt(r['avg_rating'])} ({r['n_rating']})</td>"
        f"<td>{fmt(r['avg_clarity'])} ({r['n_clarity']})</td>"
        f"<td>{r['n_comment']}</td></tr>"
        for r in rows
    ) or "<tr><td colspan=5 class=muted>No feedback yet.</td></tr>"
    crows = "".join(
        f"<tr><td>{_esc(c['ts'])}</td><td>{_esc(c['workshop'])}</td>"
        f"<td>{_esc(c['rating'])}</td><td>{_esc(c['comment'])}</td></tr>"
        for c in comments()
    ) or "<tr><td colspan=4 class=muted>No comments yet.</td></tr>"
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feedback — admin</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#1a2b45}}
 table{{border-collapse:collapse;width:100%;margin:1rem 0}} th,td{{border:1px solid #cbd5e0;padding:.4rem .6rem;text-align:left;vertical-align:top}}
 th{{background:#f0f4fa}} .muted{{color:#5a6b85}} h1{{font-size:1.4rem}}
 @media (prefers-color-scheme:dark){{body{{color:#e8eef7;background:#0f1729}}th,td{{border-color:#33445c}}th{{background:#18233a}}}}
</style></head><body>
<h1>{_esc(PRODUCT)} — feedback</h1>
<p><strong>Overall:</strong> {overall['n']} responses ·
 avg rating {fmt(overall['avg_rating'])} · avg clarity {fmt(overall['avg_clarity'])} ·
 {overall['n_comment']} comments</p>
<h2>By course</h2>
<table><tr><th>Workshop</th><th>Responses</th><th>Avg rating (n)</th><th>Avg clarity (n)</th><th>Comments</th></tr>
{trs}</table>
<h2>Comments</h2>
<table><tr><th>When (UTC)</th><th>Workshop</th><th>Rating</th><th>Comment</th></tr>
{crows}</table>
</body></html>"""


def metrics_text():
    rows, overall = aggregates()
    out = [
        "# HELP feedback_responses_total Feedback responses collected.",
        "# TYPE feedback_responses_total gauge",
        "# HELP feedback_rating_avg Average workshop rating (1-5).",
        "# TYPE feedback_rating_avg gauge",
        "# HELP feedback_clarity_avg Average instruction-clarity rating (1-5).",
        "# TYPE feedback_clarity_avg gauge",
        "# HELP feedback_comments_total Comments collected.",
        "# TYPE feedback_comments_total gauge",
    ]
    for r in rows:
        w = r["workshop"].replace("\\", "\\\\").replace('"', '\\"')
        lbl = f'{{workshop="{w}"}}'
        out.append(f"feedback_responses_total{lbl} {r['n']}")
        if r["avg_rating"] is not None:
            out.append(f"feedback_rating_avg{lbl} {r['avg_rating']:.4f}")
        if r["avg_clarity"] is not None:
            out.append(f"feedback_clarity_avg{lbl} {r['avg_clarity']:.4f}")
        out.append(f"feedback_comments_total{lbl} {r['n_comment']}")
    out.append(f"feedback_responses_total {overall['n']}")
    if overall["avg_rating"] is not None:
        out.append(f"feedback_rating_avg {overall['avg_rating']:.4f}")
    return "\n".join(out) + "\n"


# --- analytics webhook parsing ----------------------------------------------

def parse_analytics(payload):
    """Extract (workshop, session, rating, clarity, comment) from an Educates
    analytics event. Only our custom rating events carry a score; everything
    else (session started/finished, page nav) is ignored (returns None)."""
    ev = payload.get("event") or {}
    name = ev.get("name") if isinstance(ev, dict) else payload.get("event")
    if name not in ("workshop.rating", "workshop.clarity", "workshop.feedback"):
        return None
    data = (ev.get("data") if isinstance(ev, dict) else None) or payload.get("data") or {}
    workshop = ((payload.get("workshop") or {}).get("name")
                or data.get("workshop") or "unknown")
    session = ((payload.get("session") or {}).get("name") or data.get("session"))
    rating = data.get("score") if name == "workshop.rating" else data.get("rating")
    clarity = data.get("clarity") if name in ("workshop.clarity", "workshop.feedback") else None
    comment = data.get("comment")
    return workshop, session, rating, clarity, comment


# --- HTTP --------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "feedback-collector/1"

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _authed(self, q):
        if not ADMIN_TOKEN:
            return False                                    # locked unless a token is configured
        tok = (q.get("token", [""])[0]
               or self.headers.get("Authorization", "").removeprefix("Bearer ").strip())
        return tok == ADMIN_TOKEN

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path in ("/healthz", "/livez", "/readyz"):
            return self._send(200, "ok", "text/plain")
        if u.path == "/metrics":
            return self._send(200, metrics_text(), "text/plain; version=0.0.4")
        if u.path in ("/form", "/feedback"):
            return self._send(200, form_page(q.get("workshop", [""])[0], q.get("session", [""])[0]))
        if u.path == "/admin":
            if not self._authed(q):
                return self._send(401, "unauthorized — append ?token=<ADMIN_TOKEN>", "text/plain")
            return self._send(200, admin_page())
        if u.path == "/":
            return self._send(200, f"{PRODUCT} feedback collector. POST /feedback or /analytics.",
                              "text/plain")
        return self._send(404, "not found", "text/plain")

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        if u.path == "/feedback":
            f = urllib.parse.parse_qs(raw.decode("utf-8", "replace"))
            insert(f.get("workshop", [""])[0], f.get("session", [""])[0], "form",
                   f.get("rating", [None])[0], f.get("clarity", [None])[0],
                   f.get("comment", [None])[0])
            return self._send(200, thanks_page())
        if u.path == "/analytics":
            try:
                payload = json.loads(raw or b"{}")
            except json.JSONDecodeError:
                return self._send(400, "bad json", "text/plain")
            parsed = parse_analytics(payload if isinstance(payload, dict) else {})
            if parsed:
                insert(*(list(parsed[:2]) + ["analytics"] + list(parsed[2:])))
            return self._send(204, b"")                     # ack every event; store only ratings
        return self._send(404, "not found", "text/plain")

    def log_message(self, fmt, *args):                      # concise stdout logging
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))


def selftest():
    """Runnable check: exercises insert/aggregate/metrics/analytics in-memory."""
    global DB_PATH
    DB_PATH = ":memory:"
    # sqlite :memory: is per-connection, so pin one connection for the test
    global _db
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _db = lambda: conn  # noqa: E731
    assert insert("lab-a01", "s1", "form", 5, 4, "great") is True
    assert insert("lab-a01", "s2", "analytics", 3, None, None) is True
    assert insert("lab-a02", "s3", "form", None, None, None) is False       # nothing to store
    rows, overall = aggregates()
    assert overall["n"] == 2, overall["n"]
    assert abs(overall["avg_rating"] - 4.0) < 1e-6, overall["avg_rating"]
    by = {r["workshop"]: r for r in rows}
    assert by["lab-a01"]["n"] == 2 and by["lab-a01"]["n_comment"] == 1
    m = metrics_text()
    assert 'feedback_rating_avg{workshop="lab-a01"}' in m
    assert parse_analytics({"event": {"name": "workshop.rating", "data": {"score": 5}},
                            "workshop": {"name": "lab-a03"}})[0] == "lab-a03"
    assert parse_analytics({"event": {"name": "session.started"}}) is None
    print("selftest OK")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    init_db()
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"feedback-collector listening on :{PORT} db={DB_PATH}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
