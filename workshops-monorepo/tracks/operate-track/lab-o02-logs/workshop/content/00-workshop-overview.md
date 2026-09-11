---
title: "Logs"
---

Metrics tell you **that** something changed. Logs tell you **what happened**.

Both matter, and they are read at different moments: a graph tells you the error rate rose at
14:05, and the logs tell you it was a database timeout.

This lab is about reading logs **well** on **{{< param product_name >}}** — and about the
moment `oc logs` runs out, which is exactly the moment aggregation earns its keep.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain where a container's logs actually live, and who rotates them.
- Read logs with intent: [`oc logs`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/openshift-cli-commands.html) with `-f`, `--tail`, `--since`, `-c` and label selectors.
- Recover the output of a container that has already **crashed and restarted**.
- Say exactly when `oc logs` can no longer help you.
- Describe how aggregated logging works on {{< param product_short >}}, and what LogQL asks for.

## Prerequisites

- The Core lab **Configure & Troubleshoot Your App** — you have read a Pod's logs once.
- Helpful: **Metrics & Monitoring**, the previous lab, for the other half of observability.

{{< note >}}
**📌 Note:** nothing is carried over. You deploy both workloads here, in your own namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Logging architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/) — where container output goes, and what rotates it.
- [Viewing logs](https://docs.openshift.com/container-platform/latest/support/troubleshooting/investigating-pod-issues.html) — the OpenShift view of investigating a Pod.
- [LogQL](https://grafana.com/docs/loki/latest/query/) — the query language the aggregated store uses.
