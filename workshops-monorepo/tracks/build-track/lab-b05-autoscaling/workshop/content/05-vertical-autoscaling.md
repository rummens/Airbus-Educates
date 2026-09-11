---
title: The Other Autoscaler
---

The HPA changes **how many** Pods you run. It never touches what each Pod asks for.

That is the other autoscaler's job. A
[**VerticalPodAutoscaler**](https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-vertical-autoscaler.html)
(VPA) watches actual consumption over time and recommends — or applies — better
`requests` and `limits`.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/vpa
```

## Two different questions

- **HPA** — "one Pod is not enough for this load." Answer: more Pods.
- **VPA** — "this Pod asked for 500m and has never used more than 40m." Answer: a smaller
  request, so the namespace budget goes further and the scheduler can pack honestly.

Both matter on a platform where your quota is finite and someone is paying for it. Wrong
`requests` are the most common reason a namespace runs out of budget while its Pods sit idle.

## Recommendation before automation

A VPA can run in several modes. The useful one to start with is **recommendation only**: it
publishes what it thinks the requests should be, changes nothing, and leaves the decision to
you.

That matters because applying a new request means **replacing the Pod** — vertical scaling is
not free, and an eviction you did not expect is worse than a request that is 20% too high.

{{< warning >}}
**⚠️ Watch out:** do not point a VPA and an HPA at the **same resource** on the same
workload. If both control CPU they fight — the HPA reacts to utilisation while the VPA moves
the very request that utilisation is measured against. Pick one per resource: commonly HPA on
CPU, VPA on memory, or VPA in recommendation mode only.
{{< /warning >}}

## On {{< param product_short >}}

VPA arrives as an **operator** the platform installs, not as something a tenant deploys — the
same ownership split as every other operator-provided capability: the platform owns the
controller, you own the object that uses it.

More in the
[{{< param product_short >}} autoscaling docs]({{< param dcs_docs_base_url >}}/concepts/autoscaling).

Whether a VPA is available in your own namespace is a question for your platform contact —
and one worth asking before you spend an afternoon tuning requests by hand.
