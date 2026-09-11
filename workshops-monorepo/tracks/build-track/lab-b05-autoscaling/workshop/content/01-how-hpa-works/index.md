---
title: How an HPA Works
---

An HPA is a controller that runs a loop, not a rule that fires once.

Every few seconds it asks the same question: *given what these Pods are actually using, how
many of them should there be?*

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/hpa-loop
```

## The loop

![The metrics pipeline feeds the HPA controller, which compares average CPU against the request-based target and writes a new replica count onto the Deployment, which creates or removes Pods](hpa-loop.svg)

1. The platform's **metrics pipeline** collects CPU and memory use per Pod.
2. The **HPA controller** reads it, and averages CPU across the Pods it owns.
3. It compares that average with its **target**.
4. It writes a new **replica count** onto the Deployment — which then creates or removes
   Pods, exactly as if you had run `oc scale` yourself.

## Requests are the denominator

The target is a **percentage of the Pod's CPU request**, not of a core:

- Each Pod requests **100m** CPU (a tenth of a core).
- The HPA targets **50%** utilisation, so **50m** per Pod.
- Four Pods averaging 90m are at 180% of target, so the HPA scales out.

This is why the **Health & Resources** lab matters before this one: with **no** CPU request
there is nothing to take a percentage *of*, and the HPA reports `<unknown>` forever, never
scaling at all.

{{< warning >}}
**⚠️ Watch out:** requests are also what the scheduler and your namespace quota count. Set
them too high and the HPA scales out later than you expect, while each replica eats more of
the budget.
{{< /warning >}}

## What it does not do

- It does **not** make a slow app fast — it adds copies of the same app.
- It does **not** help a workload that is slow for a reason other than CPU, unless you give
  it the metric that actually reflects the bottleneck.
- It does **not** exceed `maxReplicas`, and it cannot beat the namespace budget.

Next you create one.
