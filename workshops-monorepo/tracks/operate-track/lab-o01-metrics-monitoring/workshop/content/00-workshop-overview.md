---
title: "Metrics & Monitoring"
---

**{{< param product_name >}}** already measures your Pods: CPU, memory, restarts. You get that
for free, and it tells you nothing about what your application is actually doing.

How many requests? How many of them failed? How long did they take?

Only the app knows — so the app has to **say so**, and something has to come and collect it.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the path a metric takes from your container to a query, and who owns each hop.
- Read the [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/) your app serves on `/metrics`.
- Ask to be scraped with a [**ServiceMonitor**](https://docs.openshift.com/container-platform/latest/observability/monitoring/managing-metrics.html), and confirm it worked.
- Query your own series with **PromQL** from the terminal.
- Explain why the same query about another tenant's namespace is refused.

## Prerequisites

- **Services & Cluster Networking** — a ServiceMonitor selects a **Service**, by label and by
  port name.
- Helpful: **Health & Resources**, since the platform metrics you already have come from there.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You deploy the app, the Service and the
ServiceMonitor here, in your own namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with
`oc`, and queries go to the platform's tenant query endpoint, which your session token already
lets you use for **your own** namespace.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Exposition formats](https://prometheus.io/docs/instrumenting/exposition_formats/) — what a `/metrics` endpoint must look like.
- [Querying basics (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/basics/) — selectors, ranges and functions.
- [Managing metrics](https://docs.openshift.com/container-platform/latest/observability/monitoring/managing-metrics.html) — ServiceMonitors and user-workload monitoring on OpenShift.
