---
title: Two Kinds of Disruption
---

Your Pod can stop for two very different reasons, and they need different answers.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/disruption
```

![Involuntary disruption — a node fails, a Pod is OOM-killed — answered by replicas, probes and spreading; voluntary disruption — a drain, an upgrade, a rebalance — answered by a PodDisruptionBudget; and graceful shutdown, which both paths run through](disruption-kinds.svg)

## Involuntary: nobody chose this

A node fails. A kernel panics. A container exceeds its memory limit and is `OOMKilled`.

Nothing negotiates with these. Your defences are the ones from earlier labs:

- **more than one replica**, so losing one is not losing the service;
- **probes**, so a broken replica leaves the Service's endpoints;
- **spreading**, so one node's failure does not take every replica with it.

## Voluntary: the platform chose it, deliberately

A node is **drained** for maintenance. The cluster is upgraded. A rebalance moves workloads.

These are planned, and planned actions can wait. That is what a
[**PodDisruptionBudget**](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
(PDB) is for: it tells the platform *how much of your app must stay up while it works*.

{{< note >}}
**📌 On {{< param product_short >}} you never run the drain.** Node maintenance is the
platform's job. Your PDB is how you constrain it without being in the room — which is exactly
why it has to be written before the maintenance window, not during it.
{{< /note >}}

## Both paths end in shutdown

Whichever reason ends a Pod, the ending itself is the same sequence: the Pod leaves the
Service's endpoints, `preStop` runs, `SIGTERM` arrives, and after the grace period `SIGKILL`
follows.

An app that handles that sequence well is one nobody notices being moved. An app that ignores
it drops requests every time the platform touches it — and you will measure exactly what that
costs, two pages from now.

## What this lab does

1. Declare a budget, and read back **how many Pods the platform may take right now**.
2. Squeeze it until the answer is **zero**, and see why that is not "safer".
3. Time a shutdown and find out what `SIGTERM` handling is worth.
4. Ask for replicas to be **spread**, and choose how hard an ask it is.
