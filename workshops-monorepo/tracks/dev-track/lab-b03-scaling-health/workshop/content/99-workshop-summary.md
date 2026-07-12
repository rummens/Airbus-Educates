---
title: Summary
---

Your app is now resilient and a good tenant of its namespace on
**{{< param product_name >}}** — it scales, fits its budget, and tells the platform when it's
healthy.

## What You Did

- **Scaled** the Deployment and saw replica count meet the namespace **quota**.
- Asked for too much and watched the quota **reject** it — a **Pending** Pod + a clear event.
- **Right-sized** requests and limits so the app fits the budget.
- Added **readiness** (gates traffic) and **liveness** (restarts a hang) probes.

## Challenge

Now do it yourself, unguided. Make sure the `hello-dcs` Deployment is running **2 healthy,
ready replicas** within budget. When you think it's done, run the check.

```examiner:execute-test
name: verify-replicas
title: Challenge — 2 ready replicas
args:
- hello-dcs
- "2"
timeout: 5
retries: 6
delay: 3
```

{{< note >}}
**Hint:** if any Pod is Pending, your requests are too big for the budget — right-size them
(`deployment-probes.yaml` is already sized correctly) and re-apply.
{{< /note >}}

## Check Your Understanding

1. What is the difference between a **request** and a **limit**?

{{< note >}}
**Answer:** The request is what the scheduler reserves (and what counts against quota); the
limit is the ceiling the container may burst to before it's throttled (CPU) or OOM-killed
(memory).
{{< /note >}}

2. You applied a Deployment and a Pod stayed **Pending** with an "exceeded quota" event. What's the fix?

{{< note >}}
**Answer:** Right-size the **requests** to what the app actually needs so the total fits the
namespace budget. Raising the quota is a tenancy request, not the first move.
{{< /note >}}

3. A **readiness** probe is failing. What happens to traffic, and does the Pod restart?

{{< note >}}
**Answer:** The Service removes the Pod from its endpoints, so it receives **no traffic** —
but it is **not** restarted. Only a failing **liveness** probe triggers a restart.
{{< /note >}}

4. Why did `oc rollout restart` not cause downtime even with probes?

{{< note >}}
**Answer:** New Pods must pass readiness before they receive traffic, and old Pods are only
removed once new ones are Ready — so the Service always has healthy endpoints.
{{< /note >}}

## Next Steps

Next in the Developer track: **Debugging & Logs** — your app is healthy now, but one day it
won't be. You'll walk into a *broken* deployment and learn a repeatable way to diagnose and
fix it.
