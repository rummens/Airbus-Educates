# Resilience & Scheduling

**The platform evicts Pods during maintenance. This lab covers how to avoid an outage when it does.**

Node maintenance, upgrades and rebalancing evict Pods routinely. A PodDisruptionBudget sets
how many may be evicted at once.

You set a **PodDisruptionBudget** and read from its status how many Pods the platform may
take right now, then scale down until that number is **zero** and see why a budget nobody can
satisfy blocks maintenance.

Then **shutdown**. You time a real Pod deletion and measure
what a container that ignores `SIGTERM` costs.

Last, **spreading** replicas across nodes, and the trade-off between a spread you prefer and
one you require.

> **⚠️ Watch out:** you will not drain a node, because that is the platform's action. You do the
> tenant half: declare what it must respect, then read the budget's status to confirm it is in
> effect.

- **Track:** Build & Run — the last lab
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** **Health & Resources**. Helpful: **Services & Cluster Networking**.

## By the end of this lab you'll be able to

- Tell voluntary disruption from involuntary, and say what defends against each.
- Write a PodDisruptionBudget and read how much room it leaves the platform.
- Explain why a budget that allows nothing blocks cluster maintenance.
- Explain the shutdown sequence, and what `SIGTERM` handling is worth.
- Spread replicas across nodes, and choose how hard that request should be.

## What you'll do

1. **Deploy** three replicas with a grace period and a `preStop` hook.
2. **Declare** a budget and read `disruptionsAllowed`.
3. **Squeeze** it to zero, then fix it properly.
4. **Time** a deletion and account for every second.
5. **Ask** to be spread, and pick between preferring and requiring it.
