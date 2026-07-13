"""Feedback storage — absorbed from the standalone feedback-collector.

Same schema and aggregates; storage is now pluggable behind DATABASE_URL:
  * postgres://…  → CloudNativePG (psycopg), the production path (stateless,
    HA-safe — any replica can serve);
  * empty         → SQLite at FEEDBACK_DB, for local/dev iteration only.

Course view exposes ratings only (avg+count, gated by a threshold); comments
are admin-only. Analytics-webhook parsing is carried over verbatim.
"""
import sqlite3
import threading

from . import config as cfg

_IS_PG = cfg.DATABASE_URL.startswith("postgres")
_PH = "%s" if _IS_PG else "?"        # param placeholder differs by driver
_lock = threading.Lock()
_conn = None

# One statement per list entry (psycopg3 execute runs a single statement).
SCHEMA_SQLITE = [
    """CREATE TABLE IF NOT EXISTS feedback (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ts TEXT NOT NULL, workshop TEXT NOT NULL, session TEXT,
      source TEXT NOT NULL, rating INTEGER, clarity INTEGER, comment TEXT)""",
    "CREATE INDEX IF NOT EXISTS idx_feedback_workshop ON feedback(workshop)",
    """CREATE TABLE IF NOT EXISTS progress (
      username TEXT NOT NULL, workshop TEXT NOT NULL, status TEXT NOT NULL,
      ts TEXT NOT NULL, UNIQUE(username, workshop))""",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)",
]
SCHEMA_PG = [
    """CREATE TABLE IF NOT EXISTS feedback (
      id BIGSERIAL PRIMARY KEY,
      ts TIMESTAMPTZ NOT NULL DEFAULT now(), workshop TEXT NOT NULL, session TEXT,
      source TEXT NOT NULL, rating INT, clarity INT, comment TEXT)""",
    "CREATE INDEX IF NOT EXISTS idx_feedback_workshop ON feedback(workshop)",
    """CREATE TABLE IF NOT EXISTS progress (
      username TEXT NOT NULL, workshop TEXT NOT NULL, status TEXT NOT NULL,
      ts TIMESTAMPTZ NOT NULL, UNIQUE(username, workshop))""",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)",
]


def _connect():
    if _IS_PG:
        import psycopg
        return psycopg.connect(cfg.DATABASE_URL, autocommit=True)
    # isolation_level=None → autocommit, so writes are durable immediately
    # (matches the psycopg autocommit path).
    c = sqlite3.connect(cfg.FEEDBACK_DB, check_same_thread=False, isolation_level=None)
    c.row_factory = sqlite3.Row
    return c


def _c():
    """Lazy, lock-guarded connection; reconnect if the link dropped."""
    global _conn
    with _lock:
        if _conn is None:
            _conn = _connect()
        return _conn


def _rows(cur):
    """Normalise rows to dicts across sqlite (Row) and psycopg (tuple)."""
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def init_db():
    with _lock:
        conn = _connect()
        globals()["_conn"] = conn
        for stmt in (SCHEMA_PG if _IS_PG else SCHEMA_SQLITE):
            cur = conn.cursor()
            cur.execute(stmt)


def _clamp(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    return n if 1 <= n <= 5 else None


def _exec(sql, args=()):
    """Run a statement, retrying once on a dropped connection."""
    global _conn
    for attempt in (1, 2):
        try:
            conn = _c()
            with _lock:
                cur = conn.cursor()
                cur.execute(sql, args)
                return cur
        except Exception:            # noqa: BLE001 — reconnect once, then propagate
            if attempt == 2:
                raise
            with _lock:
                _conn = None


def insert(workshop, session, source, rating, clarity, comment):
    workshop = (workshop or "unknown").strip()[:200]
    session = (session or "").strip()[:200] or None
    comment = (comment or "").strip()[:4000] or None
    rating, clarity = _clamp(rating), _clamp(clarity)
    if rating is None and clarity is None and comment is None:
        return False
    if _IS_PG:
        sql = ("INSERT INTO feedback(workshop,session,source,rating,clarity,comment) "
               f"VALUES({_PH},{_PH},{_PH},{_PH},{_PH},{_PH})")
        _exec(sql, (workshop, session, source, rating, clarity, comment))
    else:
        from datetime import datetime, timezone
        sql = ("INSERT INTO feedback(ts,workshop,session,source,rating,clarity,comment) "
               f"VALUES({_PH},{_PH},{_PH},{_PH},{_PH},{_PH},{_PH})")
        _exec(sql, (datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    workshop, session, source, rating, clarity, comment))
    return True


def aggregates():
    """Per-workshop + overall rollups (admin view)."""
    cur = _exec(
        "SELECT workshop, COUNT(*) n, AVG(rating) avg_rating, COUNT(rating) n_rating, "
        "AVG(clarity) avg_clarity, COUNT(clarity) n_clarity, COUNT(comment) n_comment "
        "FROM feedback GROUP BY workshop ORDER BY workshop")
    rows = _rows(cur)
    cur = _exec("SELECT COUNT(*) n, AVG(rating) avg_rating, AVG(clarity) avg_clarity, "
                "COUNT(comment) n_comment FROM feedback")
    overall = _rows(cur)[0]
    return rows, overall


def ratings_by_workshop():
    """{workshop: {'avg': float, 'n': int}} — the ONLY feedback the course view sees."""
    cur = _exec("SELECT workshop, AVG(rating) avg_rating, COUNT(rating) n_rating "
                "FROM feedback GROUP BY workshop")
    out = {}
    for r in _rows(cur):
        if r["n_rating"]:
            out[r["workshop"]] = {"avg": float(r["avg_rating"]), "n": int(r["n_rating"])}
    return out


def comments(limit=200):
    cur = _exec(f"SELECT ts, workshop, rating, clarity, comment FROM feedback "
                f"WHERE comment IS NOT NULL ORDER BY id DESC LIMIT {_PH}", (limit,))
    return _rows(cur)


# --- per-user progress ------------------------------------------------------

def mark_progress(username, workshop, status):
    """Upsert (username, workshop) → status. 'completed' is sticky (a later
    'started' never downgrades it). No-op if user/workshop unknown."""
    username = (username or "").strip()
    workshop = (workshop or "").strip()
    if not username or not workshop or status not in ("started", "completed"):
        return
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sql = (f"INSERT INTO progress(username,workshop,status,ts) "
           f"VALUES({_PH},{_PH},{_PH},{_PH}) "
           f"ON CONFLICT(username,workshop) DO UPDATE SET "
           f"status=CASE WHEN progress.status='completed' THEN 'completed' ELSE excluded.status END, "
           f"ts=excluded.ts")
    _exec(sql, (username, workshop, status, ts))


def clear_progress(username, workshop):
    """Drop a 'started' (in-progress) marker when the user deletes their session, so
    the tile badge + 'Continue where you left off' no longer show it as active.
    'completed' is kept — finishing a lab is permanent and independent of the session."""
    username = (username or "").strip()
    workshop = (workshop or "").strip()
    if not username or not workshop:
        return
    _exec(f"DELETE FROM progress WHERE username={_PH} AND workshop={_PH} AND status='started'",
          (username, workshop))


def user_progress(username):
    """{workshop: status} for a user. Empty if no user (anon/local)."""
    username = (username or "").strip()
    if not username:
        return {}
    cur = _exec(f"SELECT workshop, status FROM progress WHERE username={_PH}", (username,))
    return {r["workshop"]: r["status"] for r in _rows(cur)}


def last_in_progress(username):
    """Most recently started-but-not-completed workshop, or None (for 'Continue')."""
    username = (username or "").strip()
    if not username:
        return None
    cur = _exec(f"SELECT workshop FROM progress WHERE username={_PH} AND status='started' "
                f"ORDER BY ts DESC LIMIT 1", (username,))
    rows = _rows(cur)
    return rows[0]["workshop"] if rows else None


# --- settings (admin-set banner, etc.) --------------------------------------

def get_setting(key, default=""):
    """Single settings value, or default. Best-effort (never raises)."""
    try:
        cur = _exec(f"SELECT value FROM settings WHERE key={_PH}", (key,))
        rows = _rows(cur)
        return rows[0]["value"] if rows and rows[0]["value"] is not None else default
    except Exception:                 # noqa: BLE001
        return default


def set_setting(key, value):
    """Upsert a settings value ('' clears it)."""
    sql = (f"INSERT INTO settings(key,value) VALUES({_PH},{_PH}) "
           f"ON CONFLICT(key) DO UPDATE SET value=excluded.value")
    _exec(sql, (key, value or ""))


# --- analytics webhook parsing (verbatim from feedback-collector) -----------

def parse_analytics(payload):
    ev = payload.get("event") or {}
    name = ev.get("name") if isinstance(ev, dict) else payload.get("event")
    if name not in ("workshop.rating", "workshop.clarity", "workshop.feedback"):
        return None
    data = (ev.get("data") if isinstance(ev, dict) else None) or payload.get("data") or {}
    workshop = ((payload.get("workshop") or {}).get("name") or data.get("workshop") or "unknown")
    session = ((payload.get("session") or {}).get("name") or data.get("session"))
    rating = data.get("score") if name == "workshop.rating" else data.get("rating")
    clarity = data.get("clarity") if name in ("workshop.clarity", "workshop.feedback") else None
    return workshop, session, rating, clarity, data.get("comment")
