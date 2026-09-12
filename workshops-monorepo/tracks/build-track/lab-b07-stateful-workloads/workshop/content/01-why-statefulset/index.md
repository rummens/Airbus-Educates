---
title: Identity, Not Interchangeability
---

The difference is not that stateful apps need storage. A Deployment can mount a volume.

The difference is whether one replica is distinguishable from another.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/identity
```

![A Deployment's Pods have generated names, share one Service IP and share one volume; a StatefulSet's Pods have ordinal names, a DNS record each and a PersistentVolumeClaim each, re-attached to the same ordinal after a restart](statefulset-vs-deployment.svg)

## What a Deployment gives you

- Pods with **generated** names such as `hello-dcs-7f8b9c6d4-x2k9p`. A new Pod gets a new
  name.
- One volume, **shared** by every replica, if you mount one at all.
- Replacements created in **any order**, several at once.

That is what a stateless app wants, and the opposite of what a replica that owns data
needs.

## What a StatefulSet adds

Three guarantees:

1. **Stable identity.** Pods are `hello-dcs-0`, `hello-dcs-1`, in order. A replacement for
   `hello-dcs-0` is *also* called `hello-dcs-0`, and gets the same DNS name back.
2. **Stable storage.** `volumeClaimTemplates` creates **one PersistentVolumeClaim per
   replica**, `data-hello-dcs-0` and `data-hello-dcs-1`, and re-attaches each claim to its own
   ordinal. Replica 1 never gets replica 0's disk.
3. **Ordered lifecycle.** `hello-dcs-0` is Ready before `hello-dcs-1` is created. A rollout
   replaces one Pod at a time, highest ordinal first. Scale-down removes the highest first.

## Why the order matters

For a database cluster, "start replica 0 first" is how the first member initialises before
the others try to join it.

Ordering lets an app assume something about its peers. A Deployment makes no such promise.

{{< warning >}}
**⚠️ Watch out:** a StatefulSet is not a database. It gives an app the identity and storage
guarantees a database needs; replication, failover and backups remain the app's problem, or an
**operator's**. That is the Operators lab.
{{< /warning >}}

Next, build one.
