"""Tiny TTL cache with a background refresher that keeps last-known-good.

The catalog / course / track reads all hit an API that can blip (the Educates
REST portal mid-restart, a k8s API hiccup). Serving a *stale-but-good* value
beats serving empty: an empty catalog makes educates._env_for fall back to the
raw workshop name, which the training-portal 404/503s on /request/ — the exact
"workshop CRs stale / references died -> 404" production failure. So on a
refresh error we KEEP the previous value and log; we never overwrite good with
bad. A background thread force-refreshes every `interval` so the value a user
hits is at most `interval` old, and a dead Educates portal is visible in logs
before anyone clicks Start.

ponytail: single gunicorn worker (-w 1) → one process, one cache, one thread.
Scale is by replicas, each with its own warm cache — no shared store needed.
"""
import logging
import threading
import time

log = logging.getLogger("portal.cache")

_registry = []


class Cached:
    """One cached value. get() returns the live value if fresh, else refreshes;
    on producer failure it returns the last good value (or `default` when cold).
    `producer` MUST raise on failure (don't swallow to []) so we can tell a real
    empty result from an error and retain the last good one."""

    def __init__(self, name, producer, ttl, default=None):
        self.name, self.producer, self.ttl, self.default = name, producer, ttl, default
        self._lock = threading.Lock()
        self._val = default
        self._exp = 0.0
        self._have = False
        _registry.append(self)

    def get(self, force=False):
        now = time.time()
        with self._lock:
            if self._have and not force and now < self._exp:
                return self._val
        try:
            val = self.producer()
        except Exception as e:                       # noqa: BLE001 — keep last-known-good
            with self._lock:
                if self._have:
                    log.warning("refresh %s failed, serving cached: %s", self.name, e)
                    return self._val
            log.warning("refresh %s failed (cold, no cached value): %s", self.name, e)
            return self.default
        with self._lock:
            self._val, self._exp, self._have = val, now + self.ttl, True
            return val


def refresh_all():
    """Force-refresh every registered cache NOW and return the names refreshed.

    Used by the /admin/rescan endpoint (ArgoCD PostSync hook) so a catalog change
    is visible immediately instead of after the next TTL tick. Cached.get(force=True)
    keeps last-known-good on producer failure, so this never raises."""
    names = []
    for c in _registry:
        c.get(force=True)
        names.append(c.name)
    log.info("forced refresh of %d cache(s): %s", len(names), names)
    return names


def start_refresher(interval):
    """Daemon thread: force-refresh every registered cache every `interval` s."""
    def loop():
        while True:
            time.sleep(interval)
            for c in _registry:
                try:
                    c.get(force=True)
                except Exception:                    # noqa: BLE001 — Cached.get already logs
                    pass
    threading.Thread(target=loop, name="portal-refresher", daemon=True).start()
    log.info("catalog refresher started: every %ss, %d source(s)", interval, len(_registry))


if __name__ == "__main__":
    # ponytail self-check: last-known-good on producer failure, TTL expiry, cold default.
    seq = iter([["a"], RuntimeError("boom"), ["b"]])

    def prod():
        v = next(seq)
        if isinstance(v, Exception):
            raise v
        return v

    c = Cached("t", prod, ttl=0, default=[])
    assert c.get() == ["a"]                 # first good
    assert c.get() == ["a"]                 # ttl=0 → refresh attempted, fails → last good
    assert c.get() == ["b"]                 # recovers
    cold = Cached("cold", lambda: (_ for _ in ()).throw(RuntimeError()), ttl=0, default=[])
    assert cold.get() == []                 # cold failure → default
    print("cache self-check ok")
