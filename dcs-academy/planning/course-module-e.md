# Module E — Observability (Cross-Track Elective)

Observability for tenant applications on DCS. Cross-track: relevant to both Developer and Architect learners. Requires a deployed app (from Developer B01 or equivalent) in addition to Foundations. Names: `lab-e0N-name`.

*Breakdown-level plan — expand to full per-workshop plans when scheduled (see `tasks.md`).*

---

### Workshop E01: Metrics & Dashboards

**Directory name:** `lab-e01-metrics-dashboards`
**Covers ideas:** 20
**Type:** Elective (cross-track)
**Prerequisites:** Module A + a deployed app (B01 or equivalent)
**Learning objectives:** Find application metrics; read a Grafana dashboard; understand the Prometheus/Thanos path.
**Narrative arc:** App is running → where its metrics live → explore a dashboard → interpret key signals.
**Code exercises:** Open a dashboard for the sample app; query a metric; correlate with app behaviour.
**Docs:** Prometheus/Grafana → upstream; DCS-specific access → `dcs_docs_base_url`.

### Workshop E02: Logs

**Directory name:** `lab-e02-logs`
**Covers ideas:** 21
**Type:** Elective (cross-track)
**Prerequisites:** E01 (or Module A + deployed app)
**Learning objectives:** Access and query application logs on DCS.
**Narrative arc:** App emits logs → find them → query/filter → use them to answer a question.
**Code exercises:** Retrieve and filter logs for the sample app; diagnose a seeded issue from logs.

### Workshop E03: Alerts

**Directory name:** `lab-e03-alerts`
**Covers ideas:** 22
**Type:** Elective (cross-track)
**Prerequisites:** E01
**Learning objectives:** Understand how alerts are defined and routed for tenant apps.
**Narrative arc:** From a metric to an alert → define/observe an alert → what happens when it fires.
**Code exercises:** Inspect/observe an alert rule for the sample app; trigger and observe it.

## Future Expansion Ideas

- Tracing / distributed tracing for multi-service apps.
- SLO/SLA workshop building on metrics + alerts.
