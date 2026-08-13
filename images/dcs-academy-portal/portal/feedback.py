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
      source TEXT NOT NULL, rating INTEGER, clarity INTEGER, comment TEXT,
      done INTEGER NOT NULL DEFAULT 0)""",
    "CREATE INDEX IF NOT EXISTS idx_feedback_workshop ON feedback(workshop)",
    """CREATE TABLE IF NOT EXISTS progress (
      username TEXT NOT NULL, workshop TEXT NOT NULL, status TEXT NOT NULL,
      ts TEXT NOT NULL, UNIQUE(username, workshop))""",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)",
    # One row per launch (progress is one row per user+lab, so it can neither
    # accumulate repeat runs nor time them). This is the usage-stats source.
    """CREATE TABLE IF NOT EXISTS runs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL, workshop TEXT NOT NULL, session TEXT,
      started_at TEXT NOT NULL, finished_at TEXT, feedback_at TEXT)""",
    "CREATE INDEX IF NOT EXISTS idx_runs_workshop ON runs(workshop)",
]
SCHEMA_PG = [
    """CREATE TABLE IF NOT EXISTS feedback (
      id BIGSERIAL PRIMARY KEY,
      ts TIMESTAMPTZ NOT NULL DEFAULT now(), workshop TEXT NOT NULL, session TEXT,
      source TEXT NOT NULL, rating INT, clarity INT, comment TEXT,
      done BOOLEAN NOT NULL DEFAULT false)""",
    "CREATE INDEX IF NOT EXISTS idx_feedback_workshop ON feedback(workshop)",
    """CREATE TABLE IF NOT EXISTS progress (
      username TEXT NOT NULL, workshop TEXT NOT NULL, status TEXT NOT NULL,
      ts TIMESTAMPTZ NOT NULL, UNIQUE(username, workshop))""",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)",
    """CREATE TABLE IF NOT EXISTS runs (
      id BIGSERIAL PRIMARY KEY,
      username TEXT NOT NULL, workshop TEXT NOT NULL, session TEXT,
      started_at TIMESTAMPTZ NOT NULL, finished_at TIMESTAMPTZ, feedback_at TIMESTAMPTZ)""",
    "CREATE INDEX IF NOT EXISTS idx_runs_workshop ON runs(workshop)",
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


def _close_locked():
    """Close and forget the pooled connection. Caller already holds _lock.

    Dropping the reference alone leaks the handle (and trips ResourceWarning) — it matters
    on the reconnect path, which runs for the lifetime of the pod."""
    global _conn
    c, _conn = _conn, None
    if c is None:
        return
    try:
        c.close()
    except Exception:            # noqa: BLE001 — an already-dead link needs no closing
        pass


def close():
    """Drop the pooled connection (re-init, reconnect, and test teardown)."""
    with _lock:
        _close_locked()


def _rows(cur):
    """Normalise rows to dicts across sqlite (Row) and psycopg (tuple)."""
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def init_db():
    with _lock:
        _close_locked()          # re-init must not abandon the previous handle
        conn = _connect()
        globals()["_conn"] = conn
        for stmt in (SCHEMA_PG if _IS_PG else SCHEMA_SQLITE):
            cur = conn.cursor()
            cur.execute(stmt)
        # Migration for DBs created before 'done' existed. CREATE TABLE IF NOT
        # EXISTS won't add it; sqlite has no ADD COLUMN IF NOT EXISTS, so the
        # duplicate-column error is the "already migrated" signal.
        try:
            conn.cursor().execute(
                "ALTER TABLE feedback ADD COLUMN IF NOT EXISTS done BOOLEAN NOT NULL DEFAULT false"
                if _IS_PG else
                "ALTER TABLE feedback ADD COLUMN done INTEGER NOT NULL DEFAULT 0")
        except Exception:            # noqa: BLE001 — column already there
            pass


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
                _close_locked()


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


COMMENT_COLS = ["id", "ts", "workshop", "session", "source", "rating", "clarity",
                "comment", "done"]


def comments(limit=200):
    """Newest comments first. limit=None → all of them (CSV export)."""
    sql = (f"SELECT {', '.join(COMMENT_COLS)} FROM feedback "
           f"WHERE comment IS NOT NULL ORDER BY id DESC")
    if limit is None:
        return _rows(_exec(sql))
    return _rows(_exec(f"{sql} LIMIT {_PH}", (limit,)))


def set_done(fid, done):
    """Mark a comment implemented/fixed (or un-mark it)."""
    _exec(f"UPDATE feedback SET done={_PH} WHERE id={_PH}",
          (bool(done) if _IS_PG else int(bool(done)), int(fid)))


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


# --- lab runs (accumulating usage + timing) ---------------------------------

def _now():
    """Now, in whatever the driver wants: datetime for psycopg, ISO text for sqlite."""
    from datetime import datetime, timezone
    n = datetime.now(timezone.utc)
    return n if _IS_PG else n.isoformat(timespec="seconds")


def start_run(username, workshop, session):
    """One row per launch — the accumulating count of lab runs, and the clock start."""
    username = (username or "").strip()
    workshop = (workshop or "").strip()
    if not username or not workshop:
        return
    _exec(f"INSERT INTO runs(username,workshop,session,started_at) "
          f"VALUES({_PH},{_PH},{_PH},{_PH})",
          (username, workshop, (session or "").strip()[:200] or None, _now()))


def finish_run(username, workshop, with_feedback=False):
    """Stamp the user's newest run of this lab as finished (and optionally as
    feedback-given). Targets the newest run rather than the newest *unstamped* one:
    a console lab stamps finished_at at /lab/<n>/complete and then feedback_at from
    the form — both belong on the same row, and picking 'newest unstamped' would
    put the second stamp on an older abandoned run. Both columns are COALESCEd, so
    the first stamp of each wins and re-posting the form changes nothing."""
    username = (username or "").strip()
    workshop = (workshop or "").strip()
    if not username or not workshop:
        return
    now = _now()
    sets, args = f"finished_at=COALESCE(finished_at,{_PH})", [now]
    if with_feedback:
        sets += f", feedback_at=COALESCE(feedback_at,{_PH})"
        args.append(now)
    _exec(f"UPDATE runs SET {sets} WHERE id=(SELECT id FROM runs "
          f"WHERE username={_PH} AND workshop={_PH} ORDER BY id DESC LIMIT 1)",
          (*args, username, workshop))


def runs():
    """All runs, raw. Rollups happen in the caller (app._run_stats) because the
    duration maths differs per dialect and the per-lab view also needs the CRs'
    planned durations.
    ponytail: full scan — fine for thousands of runs; push to SQL if it ever isn't."""
    cur = _exec("SELECT username, workshop, session, started_at, finished_at, feedback_at "
                "FROM runs ORDER BY id")
    return _rows(cur)


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
