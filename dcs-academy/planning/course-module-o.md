# Module O — Operate & Observe (Track `operate`)

The other half of running an application on DCS: seeing what it does, and understanding the
platform mechanics underneath it. Five labs, roughly two hours, every one live-verified.

Created 2026-09-11 in the split described in
[TRACK-PLAN-build-operate.md](TRACK-PLAN-build-operate.md).

| Order | Lab | Duration | Verified |
|---|---|---|---|
| 10 | [Metrics & Monitoring](workshop-plans/lab-o01-metrics-monitoring.md) | 25m | 16/16 |
| 20 | [Logs](workshop-plans/lab-o02-logs.md) | 20m | 17/17 |
| 30 | [RBAC & Tenancy](workshop-plans/lab-o03-rbac-tenancy.md) | 25m | 32/32 |
| 40 | [DEV vs PROD Namespaces](workshop-plans/lab-o04-dev-prod-namespaces.md) | 25m | 22/22 |
| 50 | [Operators on DCS](workshop-plans/lab-o05-operators.md) | 25m | 12/12 |

## The through-line

**Every boundary in this track is the same boundary.** Metrics stop at your namespace because
the query endpoint asks "may you read Pods here". Logs stop there for the same reason. RBAC is
where that line is drawn, DEV vs PROD is what the platform enforces on top of it, and Operators
is who owns the machinery on the other side of it.

That is why RBAC sits in the middle rather than first: by the time a learner reaches it, they
have already been refused twice and want to know why.

## Environment dependencies

| Lab | Needs | Status on the test cluster |
|---|---|---|
| o01 | cluster monitoring **and** user-workload monitoring; a `/metrics` endpoint on the sample app | enabled 2026-09-11; `/metrics` added the same day |
| o02 | nothing for the hands-on half | LokiStack absent (too heavy for CRC) — aggregation is taught, not run |
| o03 | nothing | — |
| o04 | Kyverno on the host cluster | present |
| o05 | an operator (CloudNativePG) | present; its operand cannot start under Educates' SCC, so the lab asserts the reconcile |

## Next in this track

**Alerts** — a `PrometheusRule` is a query with a threshold and a duration, and needs nothing
o01 did not already teach. It is the obvious sixth lab.
