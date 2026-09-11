---
title: Summary
---

You can now read logs deliberately rather than hopefully — and you know exactly where that
ability stops.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Followed** a container's output from stdout to the node file `oc logs` reads.
2. **Read** logs by workload, across every replica, bounded by time, and live with `-f`.
3. **Recovered** the fatal error from a container that had already crashed, with `--previous`.
4. **Deleted** the workload and watched its logs become unreachable.
5. **Met** the aggregated store that fixes that, its query language, and the rule about secrets.

## Check Your Understanding

1. A Pod is crash-looping. `oc logs` on it shows almost nothing useful. What do you run?

{{< note >}}
**❓ Answer:** `oc logs <pod> --previous`. The container that failed has already been replaced;
its output is the previous container's, and that is where the error is.
{{< /note >}}

2. You run `oc logs deploy/my-app` on a Deployment with three replicas. What are you actually
   reading?

{{< note >}}
**❓ Answer:** **one** Pod's logs — `oc` picks one for you. For all three use a label selector,
`oc logs -l app=my-app --prefix`, or the aggregated store, which has them all.
{{< /note >}}

3. Last night's crash happened on a node that has since been drained. Where are those logs?

{{< note >}}
**❓ Answer:** only in the **aggregated store**. The node's file went with the Pod, so `oc logs`
cannot help — that gap is the entire reason a log store exists.
{{< /note >}}

4. Why is "never log a secret" a stronger rule on a platform than on a laptop?

{{< note >}}
**❓ Answer:** because the line does not stay in the container. It is copied to a central store,
kept for the whole retention period, and readable by everyone entitled to that namespace's
logs. `oc logs` feels private; the aggregate never is.
{{< /note >}}

## Next Steps

Metrics and logs both stop at your namespace boundary, and both got there through RBAC. The
**RBAC & Tenancy** lab is where that boundary is drawn — and if you have already done it,
**DEV vs PROD Namespaces** shows what the platform enforces on top of it.
