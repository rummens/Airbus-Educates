---
title: Scale In, and Ceilings
---

Scaling out is the easy half. What an HPA does *next* is where the design decisions are.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/scale-in
```

## Scale-in is deliberately slow

The load has stopped, so CPU has dropped — but the replica count stays up for a while.

That is not a bug. The HPA applies a **stabilisation window** of **5 minutes by default**
before scaling in, and it uses the *highest* recommendation from that window.

The asymmetry is on purpose:

- **Scaling out late** costs you latency during a spike.
- **Scaling in early** costs you a thrashing app — replicas removed and immediately needed
  again, with every removal interrupting in-flight requests.

So the controller is quick to add and slow to remove.

```terminal:execute
command: oc get hpa hello-dcs
```

```examiner:execute-test
name: verify-hpa-still-reading
title: Verify the HPA is still reporting a current CPU figure
timeout: 90
retries: .INF
delay: 3
```

You can see the window itself in the object's `behavior` section, which is where you would
tune it:

```terminal:execute
command: oc get hpa hello-dcs -o jsonpath='{.spec.behavior}{"\n"}'
```

An empty value means the defaults apply: no delay scaling out, 300 seconds of stabilisation
scaling in.

```examiner:execute-test
name: verify-hpa-behavior-read
title: Verify the HPA behavior field was read
timeout: 15
retries: 3
delay: 2
```

{{< note >}}
**💡 Tip:** waiting out the full five minutes here is not worth your session time. Setting
`behavior.scaleDown.stabilizationWindowSeconds` is how you would shorten it for a workload
that genuinely tolerates it.
{{< /note >}}

## The real ceiling is your budget

`maxReplicas: 6` is the ceiling you *chose*. The namespace budget is the ceiling you were
**given** — and it wins.

Each replica of this app has a **200m CPU / 128Mi** limit, and a `medium` namespace allows
**2 CPU / 2Gi** on the limit side:

- 6 replicas × 200m = **1.2 CPU** — comfortably inside the budget.
- The same HPA with `maxReplicas: 20` would ask for 4 CPU, and the Pods past the budget
  would be **refused at admission**, exactly as in the **Health & Resources** lab.

The HPA would then report a `ScalingLimited` condition and stall — scaling it wanted, Pods it
could not get.

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-quota-fits-max
title: Verify a full scale-out still fits inside the namespace budget
timeout: 15
retries: 3
delay: 2
```

**Set `maxReplicas` from the budget you actually have**, not from the load you imagine. An
autoscaler that cannot get Pods is worse than an honest replica count, because it looks like
it is working.
