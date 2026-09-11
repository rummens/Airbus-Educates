# Resilience & Scheduling

**The platform will move your Pods. The question is whether that costs you an outage.**

Node maintenance, upgrades and rebalancing are routine, and none of them ask permission. What
you get is a way to state your terms.

You set a **PodDisruptionBudget** and read from its own status how many Pods the platform may
take right now — then scale down until that number is **zero**, and see why a budget nobody
can satisfy is a problem rather than extra safety.

Then the half most apps get wrong: **shutdown**. You time a real Pod deletion and find out
what a container that ignores `SIGTERM` actually costs.

Last, **spreading** replicas across nodes, and the trade-off between a spread you prefer and
one you require.

> **⚠️ Watch out:** you will not drain a node — that is the platform's action. You do the
> tenant half: declare what it must respect, then check it understood.

- **Track:** Build & Run — the last lab
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
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
