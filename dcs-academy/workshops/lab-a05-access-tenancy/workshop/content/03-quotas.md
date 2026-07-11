---
title: How Much You Can Use
---

RBAC decides *what* you can do; **quotas** decide *how much*. On a shared platform, finite
capacity is divided between tenants, so your namespace comes with limits — and knowing how to
read them explains a lot of "why won't this schedule?" moments.

## Read your quota

A [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) caps the total
resources a namespace may consume. Look at yours:

```terminal:execute
command: oc describe quota
```

You'll see used-vs-hard columns for things like CPU, memory, and object counts, for example:

```
Name:            compute-resources
Resource         Used   Hard
--------         ----   ----
limits.cpu       100m   2
limits.memory    64Mi   4Gi
pods             1      10
```

The **Hard** column is your ceiling; **Used** is what you're consuming now. When you scaled a
Deployment in an earlier lab, this is what you were spending against.

```examiner:execute-test
name: verify-quota
title: A ResourceQuota is set on your namespace
timeout: 10
```

On {{< param product_short >}}, quotas come in two flavours: a **Basic** default applied to
every namespace, and a **Customized** quota for tenants with agreed higher needs. Egress IPs
are quota'd too — outbound access is a limited resource, not a free one.

## Read your limit ranges

A [LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/) sets per-object
defaults and bounds — e.g. a default CPU request a container gets if it doesn't ask for one,
or the maximum it may request. Look at yours:

```terminal:execute
command: oc describe limitrange
```

```examiner:execute-test
name: verify-limitrange
title: A LimitRange is set on your namespace
timeout: 10
```

Together, ResourceQuota (namespace total) and LimitRange (per-object) are why a workload that
asks for too much is rejected before it ever schedules — the platform protects shared capacity.

## Need more? That's a ticket, not a command

You **cannot** raise your own quota with `oc` — and that's by design. A quota increase is a
governed change: you raise an
**[ITSM request]({{< param dcs_docs_base_url >}}/quotas/limits-and-requests)**, it's reviewed
against capacity and cost (recharging), and the platform applies it. So there's no command to
run here — the takeaway is knowing *where* the limit comes from and *how* to change it: through
the service-management workflow, not self-service cluster edits.

{{< note >}}
This is a recurring {{< param product_short >}} pattern: self-service where it's safe (deploy,
scale within quota), governed requests where it affects shared capacity or cost (quota
increases, mirroring, new projects).
{{< /note >}}
