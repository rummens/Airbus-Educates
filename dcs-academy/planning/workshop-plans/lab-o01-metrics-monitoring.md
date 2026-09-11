# Workshop Plan: lab-o01-metrics-monitoring

## 1. Metadata
- **Name:** `lab-o01-metrics-monitoring` · **Title:** Metrics & Monitoring
- **Duration:** 25m · **Difficulty:** intermediate · **Track:** Operate & Observe, order `10`
- **Prerequisites (curricular):** *Services & Cluster Networking* (a ServiceMonitor selects a Service by label and port name); helpful: *Health & Resources*
- **Status:** New lab, 2026-09-11. Live-verified 16/16.

## 2. Measured before authoring — this shaped the whole lab
| Fact | Measured |
|---|---|
| Tenant metrics queries | **No platform grant needed.** The Thanos **tenancy port** (`thanos-querier.openshift-monitoring.svc:9092`, `namespace` param, session token) authorizes on `get pods` **in the namespace asked about**. Own namespace → 200; another → `Forbidden`. |
| The public `thanos-querier` **route** | the cluster-wide port; it *does* demand `prometheuses/api` in `openshift-monitoring`. **Not used by the lab.** |
| ServiceMonitors in the session role | **absent** — no `monitoring.coreos.com` rules at all. Granted via `session.objects`. |
| The proxy's authorization decisions | **cached.** A query issued before the session's RBAC settled is refused and stays refused; the same request returned 200 a minute later. A `view` binding makes the first answer unambiguous. |

## 3. Design notes
- The cross-namespace refusal is a **page**, not a footnote: tenancy is enforced in the metrics path, not only in the API.
- The lab leans on the one failure that gives nothing to read — a ServiceMonitor whose selector matches no Service, or names a port the Service does not, reports **no error and no data**. `verify-selector-matches` asserts both halves so the lab cannot pass while teaching a silent misconfiguration.
- Requires a `hello-dcs` image serving `/metrics` (added 2026-09-11). The smoke forces `imagePullPolicy: Always` because `:1.0` is a mutable tag.
