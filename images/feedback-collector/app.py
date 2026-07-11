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
import csv
import html
import io
import json
import os
import re
import sqlite3
import sys
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from zoneinfo import ZoneInfo
    BERLIN = ZoneInfo("Europe/Berlin")          # needs tzdata (in the image)
except Exception:                                # pragma: no cover - fallback if tz db missing
    BERLIN = timezone.utc

EXPORT_COLS = ["id", "ts", "workshop", "session", "source", "rating", "clarity", "comment"]

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


# --- export / import (backup) ------------------------------------------------

def export_rows():
    with _db() as c:
        return [dict(r) for r in c.execute(
            "SELECT id,ts,workshop,session,source,rating,clarity,comment "
            "FROM feedback ORDER BY id").fetchall()]


def export_csv():
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=EXPORT_COLS)
    w.writeheader()
    for row in export_rows():
        w.writerow(row)
    return buf.getvalue()


def import_csv(text, replace=False):
    """Restore rows from a CSV produced by export_csv (Excel-compatible).
    Preserves original ts/source; `id` is ignored (auto-assigned). Returns count."""
    rows = list(csv.DictReader(io.StringIO(text)))
    with _db() as c:
        if replace:
            c.execute("DELETE FROM feedback")
        n = 0
        for r in rows:
            ts = (r.get("ts") or datetime.now(timezone.utc).isoformat(timespec="seconds")).strip()
            workshop = (r.get("workshop") or "unknown").strip()[:200]
            session = ((r.get("session") or "").strip() or None)
            source = (r.get("source") or "import").strip()[:20]
            comment = ((r.get("comment") or "").strip() or None)
            rating = _clamp_score(r.get("rating"))
            clarity = _clamp_score(r.get("clarity"))
            c.execute(
                "INSERT INTO feedback(ts,workshop,session,source,rating,clarity,comment) "
                "VALUES(?,?,?,?,?,?,?)",
                (ts, workshop, session, source, rating, clarity, comment))
            n += 1
    return n


# --- rendering ---------------------------------------------------------------

def _esc(s):
    return html.escape(str(s if s is not None else ""))


def fmt_de(ts):
    """UTC ISO timestamp -> German date-time (TT.MM.JJJJ HH:MM, Europe/Berlin)."""
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(BERLIN).strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return _esc(ts)


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


def admin_page(token=""):
    rows, overall = aggregates()
    tq = urllib.parse.quote(token)

    def fmt(v):
        return f"{v:.2f}" if v is not None else "—"

    def cell_comment(text):
        full = text or ""
        short = full if len(full) <= 80 else full[:80].rstrip() + "…"
        # full text lives in data-full; JS opens a modal on click.
        return (f'<td class="cmt" data-full="{_esc(full)}" onclick="showComment(this)" '
                f'title="Click to show full comment">{_esc(short)}</td>')

    trs = "".join(
        f"<tr><td>{_esc(r['workshop'])}</td><td>{r['n']}</td>"
        f"<td>{fmt(r['avg_rating'])} ({r['n_rating']})</td>"
        f"<td>{fmt(r['avg_clarity'])} ({r['n_clarity']})</td>"
        f"<td>{r['n_comment']}</td></tr>"
        for r in rows
    ) or "<tr><td colspan=5 class=muted>No feedback yet.</td></tr>"
    crows = "".join(
        f"<tr><td>{fmt_de(c['ts'])}</td><td>{_esc(c['workshop'])}</td>"
        f"<td>{_esc(c['rating'])}</td>{cell_comment(c['comment'])}</tr>"
        for c in comments()
    ) or "<tr><td colspan=4 class=muted>No comments yet.</td></tr>"
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feedback — admin</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#1a2b45}}
 table{{border-collapse:collapse;width:100%;margin:1rem 0}} th,td{{border:1px solid #cbd5e0;padding:.4rem .6rem;text-align:left;vertical-align:top}}
 th{{background:#f0f4fa}} .muted{{color:#5a6b85}} h1{{font-size:1.4rem}} h2{{font-size:1.1rem;margin-top:1.6rem}}
 td.cmt{{cursor:pointer;max-width:32rem}} td.cmt:hover{{background:#eef4ff}}
 .tools{{margin:1rem 0;padding:.8rem 1rem;border:1px solid #cbd5e0;border-radius:8px;background:#f7fafd}}
 .tools a,.tools button{{margin-right:1rem}}
 button{{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:.4rem .9rem;cursor:pointer}}
 #modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);align-items:center;justify-content:center}}
 #modal.open{{display:flex}} #modalbox{{background:#fff;color:#1a2b45;max-width:640px;max-height:80vh;overflow:auto;padding:1.5rem;border-radius:10px;white-space:pre-wrap}}
 @media (prefers-color-scheme:dark){{body{{color:#e8eef7;background:#0f1729}}th,td{{border-color:#33445c}}th{{background:#18233a}}
  td.cmt:hover{{background:#18233a}}.tools{{background:#14203a;border-color:#33445c}}#modalbox{{background:#18233a;color:#e8eef7}}}}
</style></head><body>
<h1>{_esc(PRODUCT)} — feedback</h1>
<p><strong>Overall:</strong> {overall['n']} responses ·
 avg rating {fmt(overall['avg_rating'])} · avg clarity {fmt(overall['avg_clarity'])} ·
 {overall['n_comment']} comments</p>

<div class="tools">
 <strong>Backup:</strong>
 <a href="/export.csv?token={tq}">Download CSV</a>
 <a href="/export.json?token={tq}">Download JSON</a>
 <form action="/import?token={tq}" method="POST" enctype="multipart/form-data" style="display:inline">
   <input type="file" name="file" accept=".csv,text/csv" required>
   <label><input type="checkbox" name="replace" value="true"> replace all</label>
   <button type="submit">Import CSV</button>
 </form>
</div>

<h2>By course</h2>
<table><tr><th>Workshop</th><th>Responses</th><th>Avg rating (n)</th><th>Avg clarity (n)</th><th>Comments</th></tr>
{trs}</table>
<h2>Comments</h2>
<table><tr><th>When (Europe/Berlin)</th><th>Workshop</th><th>Rating</th><th>Comment</th></tr>
{crows}</table>

<div id="modal" onclick="this.classList.remove('open')"><div id="modalbox"></div></div>
<script>
 function showComment(td){{document.getElementById('modalbox').textContent=td.getAttribute('data-full');
   document.getElementById('modal').classList.add('open');}}
</script>
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

def _multipart_file(raw, ctype):
    """Minimal multipart/form-data parser: return (file_text, replace_bool).
    Enough for one file field ('file') + an optional 'replace' checkbox — avoids
    the stdlib `cgi` module (removed in Python 3.13)."""
    m = re.search(r'boundary=(?:"([^"]+)"|([^;]+))', ctype)
    if not m:
        return "", False
    boundary = ("--" + (m.group(1) or m.group(2)).strip()).encode()
    text, replace = "", False
    for part in raw.split(boundary):
        if b"\r\n\r\n" not in part:
            continue
        head, _, body = part.partition(b"\r\n\r\n")
        body = body.rstrip(b"\r\n")
        disp = head.decode("utf-8", "replace")
        if 'name="file"' in disp:
            text = body.decode("utf-8", "replace")
        elif 'name="replace"' in disp:
            replace = body.decode().strip().lower() in ("true", "on", "1")
    return text, replace


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
        if u.path in ("/admin", "/export.csv", "/export.json"):
            if not ADMIN_TOKEN:
                return self._send(503, "admin/backup disabled: ADMIN_TOKEN is not configured on "
                                  "the collector (set feedback.adminToken or feedback.existingSecret)",
                                  "text/plain")
            if not self._authed(q):
                return self._send(401, "unauthorized — append ?token=<ADMIN_TOKEN>", "text/plain")
            if u.path == "/export.csv":
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", "attachment; filename=feedback-backup.csv")
                body = export_csv().encode()
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                return self.wfile.write(body)
            if u.path == "/export.json":
                return self._send(200, json.dumps(export_rows(), ensure_ascii=False, indent=2),
                                  "application/json; charset=utf-8")
            return self._send(200, admin_page(q.get("token", [""])[0]))
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
        if u.path == "/import":
            if not ADMIN_TOKEN:
                return self._send(503, "import disabled: ADMIN_TOKEN not configured", "text/plain")
            q = urllib.parse.parse_qs(u.query)
            if not self._authed(q):
                return self._send(401, "unauthorized", "text/plain")
            ctype = self.headers.get("Content-Type", "")
            replace = q.get("replace", ["false"])[0].lower() == "true"
            if ctype.startswith("multipart/form-data"):     # admin UI upload
                text, form_replace = _multipart_file(raw, ctype)
                replace = replace or form_replace
            else:                                            # API: raw CSV body
                text = raw.decode("utf-8", "replace")
            if not text:
                return self._send(400, "no CSV data", "text/plain")
            try:
                n = import_csv(text, replace=replace)
            except (csv.Error, ValueError) as e:
                return self._send(400, f"import failed: {e}", "text/plain")
            msg = f"imported {n} rows{' (replaced all)' if replace else ''}"
            # browser form -> redirect back to admin; API -> plain text
            if ctype.startswith("multipart/form-data"):
                self.send_response(303)
                self.send_header("Location", "/admin?token=" + urllib.parse.quote(q.get("token", [""])[0]))
                self.end_headers()
                return
            return self._send(200, msg + "\n", "text/plain")
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
    # german date format
    assert fmt_de("2026-01-15T09:30:00+00:00") == "15.01.2026 10:30", fmt_de("2026-01-15T09:30:00+00:00")
    # export -> import round-trip (replace) preserves rows + timestamps
    csv_text = export_csv()
    assert "workshop" in csv_text.splitlines()[0]
    n = import_csv(csv_text, replace=True)
    assert n == 2, n
    _, overall2 = aggregates()
    assert overall2["n"] == 2, overall2["n"]
    # multipart extraction
    body = (b"--B\r\nContent-Disposition: form-data; name=\"file\"; filename=\"x.csv\"\r\n\r\n"
            b"id,ts,workshop,session,source,rating,clarity,comment\r\n--B\r\n"
            b"Content-Disposition: form-data; name=\"replace\"\r\n\r\ntrue\r\n--B--\r\n")
    text, rep = _multipart_file(body, "multipart/form-data; boundary=B")
    assert rep is True and text.startswith("id,ts,workshop"), (rep, text[:20])
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
