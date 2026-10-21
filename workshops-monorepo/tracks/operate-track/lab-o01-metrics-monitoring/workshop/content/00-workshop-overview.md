---
title: "Metrics & Monitoring"
---

**{{< param product_name >}}** already measures your Pods: CPU, memory and restarts. You get
that without asking, but it does not show what your application is doing.

Request counts, failures and request durations are known only to the app, so the app has to
**publish** them, and something has to collect them.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the path a metric takes from your container to a query, and who owns each hop.
- Read the [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/) your app serves on `/metrics`.
- Ask to be scraped with a [**ServiceMonitor**](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/latest/html/configuring_user_workload_monitoring/preparing-to-configure-the-monitoring-stack-uwm#enabling-monitoring-for-user-defined-projects_preparing-to-configure-the-monitoring-stack-uwm), and confirm it worked.
- Query your own series with **PromQL** from the terminal.
- Explain why the same query about another tenant's namespace is refused.

## Prerequisites

- **Services & Cluster Networking**, because a ServiceMonitor selects a **Service** by label
  and by port name.
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
- [Managing metrics](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/latest/html/configuring_user_workload_monitoring/preparing-to-configure-the-monitoring-stack-uwm#enabling-monitoring-for-user-defined-projects_preparing-to-configure-the-monitoring-stack-uwm) — ServiceMonitors and user-workload monitoring on OpenShift.
