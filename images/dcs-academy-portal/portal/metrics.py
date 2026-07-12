"""Prometheus metrics.

Two kinds:
  * in-process counters/histogram (request outcomes, provision latency, errors)
    tracked as events happen;
  * live gauges (running sessions, active users, catalog/track/feedback counts)
    computed at *scrape time* by a custom collector — they mirror cluster/DB
    state, so there's nothing to keep in memory and it's naturally HA-safe.

Run the app single-worker-multi-thread (see Containerfile) so the default
registry is correct without multiprocess bookkeeping.
"""
from prometheus_client import Counter, Histogram, CollectorRegistry, generate_latest
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import Collector

from . import feedback, k8sclient

REGISTRY = CollectorRegistry()

REQUESTS = Counter("dcs_portal_session_requests_total", "Session requests.",
                   ["workshop", "result"], registry=REGISTRY)
PROVISION = Histogram("dcs_portal_session_provision_seconds",
                      "Seconds from request to Running.",
                      buckets=(5, 15, 30, 60, 120, 300, 600), registry=REGISTRY)
ERRORS = Counter("dcs_portal_errors_total", "Portal errors.", ["kind"], registry=REGISTRY)


class _LiveCollector(Collector):
    """Query k8s + feedback lazily at each scrape."""

    def collect(self):
        running = GaugeMetricFamily("dcs_portal_sessions_running",
                                    "Running sessions per workshop.", labels=["workshop"])
        users = GaugeMetricFamily("dcs_portal_users_active",
                                  "Distinct users with a running session.")
        workshops_g = GaugeMetricFamily("dcs_portal_catalog_workshops", "Workshops in catalog.")
        tracks_g = GaugeMetricFamily("dcs_portal_tracks", "Tracks in catalog.")
        fb_total = GaugeMetricFamily("dcs_portal_feedback_total",
                                     "Feedback responses per workshop.", labels=["workshop"])
        fb_avg = GaugeMetricFamily("dcs_portal_feedback_rating_avg",
                                   "Average rating per workshop.", labels=["workshop"])
        try:
            sessions = k8sclient.list_sessions()
            per_ws, active_users = {}, set()
            for s in sessions:
                st = (s.get("status", {}) or {}).get("educates", {}) or {}
                if st.get("phase") != "Running":
                    continue
                env = (s.get("spec", {}).get("environment", {}) or {}).get("name", "unknown")
                per_ws[env] = per_ws.get(env, 0) + 1
                u = (s.get("spec", {}).get("session", {}) or {}).get("username")
                if u:
                    active_users.add(u)
            for ws, n in per_ws.items():
                running.add_metric([ws], n)
            users.add_metric([], len(active_users))
            workshops_g.add_metric([], len(k8sclient.list_courses()))
            tracks_g.add_metric([], len(k8sclient.list_tracks()))
        except Exception:            # noqa: BLE001 — metrics must never 500 the scrape
            ERRORS.labels("metrics_k8s").inc()
        try:
            rows, _ = feedback.aggregates()
            for r in rows:
                fb_total.add_metric([r["workshop"]], r["n"] or 0)
                if r["avg_rating"] is not None:
                    fb_avg.add_metric([r["workshop"]], float(r["avg_rating"]))
        except Exception:            # noqa: BLE001
            ERRORS.labels("metrics_feedback").inc()
        yield from (running, users, workshops_g, tracks_g, fb_total, fb_avg)


REGISTRY.register(_LiveCollector())


def render():
    return generate_latest(REGISTRY)
