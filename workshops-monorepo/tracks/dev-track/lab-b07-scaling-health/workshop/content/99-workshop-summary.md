---
title: Summary
---

Your `hello-dcs` app went from one unmonitored replica to four right-sized, self-proving,
self-healing ones — all inside the budget its namespace was actually given.

## What You Did

- **Scaled** the Deployment to four replicas and read the namespace's `ResourceQuota` to
  see exactly what that cost against the `medium` budget.
- **Applied** a deliberately oversized manifest and watched the quota reject the rollout —
  Pods never even got created, let alone scheduled.
- **Right-sized** `requests`/`limits` to what the app genuinely needs, recovering the
  rollout with real headroom to spare.
- **Added** liveness and readiness probes, broke readiness on purpose, and watched
  {{< param product_short >}} quarantine one Pod from the Service's endpoints while the
  other three kept serving traffic untouched.
- **Deleted** a running Pod outright and watched the ReplicaSet replace it with a new one —
  proof that desired state, not any one Pod, is what the platform actually guarantees.

## Check Your Understanding

1. You scale a Deployment from 4 to 6 replicas and the rollout gets stuck with only 5 of 6
   Pods ready. What's the most likely cause?

{{< note >}}
**Answer:** the namespace's `ResourceQuota` doesn't have room for a 6th Pod's
`requests`/`limits` — the same admission rejection you triggered on purpose in this lab.
`oc describe quota` and `oc get events` are where you'd confirm it.
{{< /note >}}

2. A Pod is running but stuck — it never responds to any request anymore. Will a
   **readiness** probe fix that on its own?

{{< note >}}
**Answer:** no. Readiness only controls whether the Pod is in the Service's endpoints —
pulling a stuck Pod out of rotation, but leaving the hung container running forever. Only
a **liveness** probe failing repeatedly gets the kubelet to kill and restart the container.
{{< /note >}}

3. What's the practical difference between a `requests` value and a `limits` value on the
   same container?

{{< note >}}
**Answer:** `requests` is what the Pod is guaranteed and what the scheduler (and the
namespace quota) counts against; `limits` is the ceiling it's capped at — exceeded on
memory, the container is `OOMKilled`; exceeded on CPU, it's throttled, not killed.
{{< /note >}}

4. You delete a Pod that belongs to a Deployment with `oc delete pod`. What actually brings
   a replacement back?

{{< note >}}
**Answer:** the Deployment's **ReplicaSet**, reconciling the actual replica count back up
to `spec.replicas`. Nothing you ran created the new Pod directly — the platform's
continuous reconciliation loop did.
{{< /note >}}

## Next Steps

You've now taken an app from "it runs" to "it survives" within its own budget — the last
piece of the developer-facing lifecycle. **B08 — Operators** picks up the advanced
capstone: managing a stateful workload (PostgreSQL) through a Kubernetes Operator instead
of a plain Deployment. Observability and debugging basics for day-to-day operation now
live back in the Core track, if you need a refresher.
