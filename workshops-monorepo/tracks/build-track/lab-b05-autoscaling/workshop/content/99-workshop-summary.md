---
title: Summary
---

You handed the replica count to a controller, and it did the job you would otherwise be
awake for.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Deployed** the app with an explicit CPU `request` — the number an HPA measures against.
2. **Created** a `HorizontalPodAutoscaler` targeting 50% CPU utilisation, from 1 to 6 replicas.
3. **Watched** it read live metrics, and read its conditions and events.
4. **Drove** the app under load from your own terminal and watched it **scale out**.
5. **Learned** why scale-in waits out a 5-minute stabilisation window.
6. **Checked** a full scale-out against the namespace budget — the ceiling you were given.
7. **Placed** VPA: the autoscaler for `requests`, not replica count.

## Check Your Understanding

1. An HPA on CPU reports `<unknown>` for its current utilisation and never scales. What is
   the first thing to check on the Deployment?

{{< note >}}
**❓ Answer:** whether the container sets a CPU **request**. The HPA's target is a percentage
*of the request*, so with no request there is nothing to measure against and the utilisation
is unknowable.
{{< /note >}}

2. Load has been gone for a minute and the replica count is still high. Is the HPA broken?

{{< note >}}
**❓ Answer:** no. Scale-in waits out a **stabilisation window** — 5 minutes by default — and
uses the highest recommendation in it. Quick to add, slow to remove, so a brief lull does not
cause thrashing. Tune it with `behavior.scaleDown.stabilizationWindowSeconds`.
{{< /note >}}

3. You raise `maxReplicas` from 6 to 20 in a `medium` namespace where each replica has a 200m
   CPU limit. What happens under heavy load?

{{< note >}}
**❓ Answer:** the HPA asks for replicas the namespace cannot pay for. 20 × 200m is 4 CPU
against a 2 CPU limit budget, so the Pods past the ceiling are **refused at admission** and
the HPA reports `ScalingLimited`. Set `maxReplicas` from the budget you have.
{{< /note >}}

4. What does a VPA change that an HPA never does?

{{< note >}}
**❓ Answer:** the Pod's own `requests` and `limits` — its size, not the number of copies.
Applying a new request replaces the Pod, which is why recommendation-only mode is the sane
starting point, and why you do not point both autoscalers at the same resource.
{{< /note >}}

## Next Steps

The autoscaler assumes any replica can serve any request. **Services & Cluster Networking**
takes that assumption apart: the Service types, cluster DNS, headless Services, and why
{{< param product_short >}} hands you a Route for anything that has to be reachable from
outside.
