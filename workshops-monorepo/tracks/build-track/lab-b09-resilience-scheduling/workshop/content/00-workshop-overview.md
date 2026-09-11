---
title: "Resilience & Scheduling"
---

The platform **will** move your Pods.

Nodes are drained for maintenance, clusters are upgraded, workloads are rebalanced. None of
it asks your permission, and all of it is routine.

What you get instead is a way to state your **terms** — and a shutdown path that decides
whether being moved costs you an outage or nobody notices.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Tell **voluntary** disruption from **involuntary**, and say what protects against each.
- Write a [**PodDisruptionBudget**](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) and read from its own status how many Pods the platform may take right now.
- Explain why a budget that allows **nothing** is a problem rather than extra safety.
- Explain what happens at shutdown — `SIGTERM`, `terminationGracePeriodSeconds`, `preStop` — and what a container that ignores `SIGTERM` costs.
- Spread replicas with [**topology spread constraints**](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/), and choose between a spread you *prefer* and one you *require*.

## Prerequisites

- **Health & Resources** — replicas, probes and readiness, which everything here builds on.
- Helpful: **Services & Cluster Networking**, for why endpoints and shutdown interact.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You deploy the app here, in your own
namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

You will **not** drain a node — that is the platform's action, not a tenant's. You will do the
tenant half: declare what the platform must respect, and check that it has understood.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) — voluntary versus involuntary, and where a PDB fits.
- [Pod Lifecycle: termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) — the exact order of events at shutdown.
- [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) — maxSkew, topologyKey and the two `whenUnsatisfiable` options.
