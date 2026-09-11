---
title: Summary
---

You built a workload whose replicas are **somebody** — with names, disks and an order.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Created** the headless Service a StatefulSet needs for per-Pod DNS.
2. **Applied** a StatefulSet with `volumeClaimTemplates`, and watched `hello-dcs-0` become
   Ready before `hello-dcs-1` was created.
3. **Confirmed** one bound claim per replica, named by ordinal.
4. **Addressed** one specific replica by its own DNS name, and wrote a different marker into
   each replica's own volume.
5. **Deleted** replica 0 and watched the same name, the same DNS record and the same **data**
   come back on a new Pod.
6. **Scaled** up (new replica, new disk) and down (Pod gone, **disk kept**), and found the
   leftover claim in the namespace quota.

## Check Your Understanding

1. A replacement Pod in a Deployment gets a new name; in a StatefulSet it does not. What
   depends on that?

{{< note >}}
**❓ Answer:** its **DNS name** and its **volume**. The claim is bound to the ordinal
(`data-hello-dcs-0`), so a Pod called `hello-dcs-0` gets that disk back, and clients that
addressed `hello-dcs-0.hello-dcs...` keep reaching the same member.
{{< /note >}}

2. You scale a StatefulSet from 3 to 2. What happened to replica 2's data?

{{< note >}}
**❓ Answer:** nothing — the claim `data-hello-dcs-2` is still there and still `Bound`. Scale
back to 3 and the new `hello-dcs-2` re-attaches it. It also still counts against your storage
quota until somebody deletes it deliberately.
{{< /note >}}

3. Why is scaling a StatefulSet out slower than scaling a Deployment out?

{{< note >}}
**❓ Answer:** each new replica needs its **own volume provisioned** and must become Ready
before the next ordinal is created. Ordering plus storage, instead of "start them all".
{{< /note >}}

4. Does using a StatefulSet make an app highly available?

{{< note >}}
**❓ Answer:** no. It provides the **identity and storage guarantees** a clustered app needs.
Replication, leader election, failover and backups are the application's job — or an
**operator's**, which is what the Operators track is about.
{{< /note >}}

## Next Steps

Not every container should run forever. **Short-Lived & Helper Containers** covers the other
shapes: **Jobs** and **CronJobs** that run to completion, **init containers** that must finish
before the app starts, and **sidecars** that run beside it.
