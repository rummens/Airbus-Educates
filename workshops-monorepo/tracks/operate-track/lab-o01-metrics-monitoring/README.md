# Metrics & Monitoring

**The platform already collects Pod metrics. Application metrics need the app to expose them.**

CPU, memory and restarts come for free. They tell you whether a Pod is healthy, not whether
requests are failing.

You expose metrics from the app, read the exposition format it serves, then ask to be scraped
with a **ServiceMonitor**, and check that its selector matches a Service, because a
ServiceMonitor that matches nothing reports no error.

Then you query your own series back with **PromQL**, from the terminal, through the platform's
tenant query endpoint.

In the last step you query your own namespace and get an answer, then query somebody else's
and get **Forbidden**. Tenancy applies to metrics too.

> **💡 Tip:** the platform runs Prometheus for you. You create one ServiceMonitor in your own
> namespace and the platform's monitoring picks it up.

- **Track:** Operate & Observe
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** **Services & Cluster Networking** (a ServiceMonitor selects a Service, by label and port name). Helpful: **Health & Resources**.

## By the end of this lab you'll be able to

- Explain the path a metric takes from your container to a query, and who owns each hop.
- Read the Prometheus exposition format your app serves.
- Create a ServiceMonitor and confirm that it selects a Service.
- Query your series with `rate()` and `sum by`.
- Explain why the same query about another namespace is refused.

## What you'll do

1. **Deploy** the app and look at what it exposes.
2. **Generate** traffic and watch the counter move.
3. **Ask** to be scraped, and verify the selector matches.
4. **Query** your own metrics, then ask a real question with PromQL.
5. **Get refused** asking about a namespace that is not yours.
