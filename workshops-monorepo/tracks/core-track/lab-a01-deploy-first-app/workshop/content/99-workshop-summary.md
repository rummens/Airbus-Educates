---
title: Summary
---

You took an image and turned it into your own running, self-healing app on
**{{< param product_name >}}** — and then read the desired-state document behind it.

## What You Did

- **Deployed** the `hello-dcs` image with `oc create deployment`.
- **Customised** it live with `oc set env GREETING=...` — no rebuild.
- **Reached** it locally with `oc port-forward` and `curl`.
- **Changed** it and watched {{< param product_short >}} **roll out** a new Pod.
- **Revealed** the YAML and read the **Deployment → ReplicaSet → Pod** chain.

## Check Your Understanding

1. What does a **Deployment** guarantee?

{{< note >}}
**Answer:** That the number of Pod copies you asked for (`spec.replicas`) keeps running.
If a Pod dies, the Deployment (via its ReplicaSet) starts a replacement — that's
self-healing.
{{< /note >}}

2. What happens when you run `oc set env` on a Deployment?

{{< note >}}
**Answer:** It changes the Pod template (the desired state), so {{< param product_short >}}
rolls out a new Pod with the new value and retires the old one — no manual restart.
{{< /note >}}

3. What **owns** a Pod created by a Deployment?

{{< note >}}
**Answer:** A **ReplicaSet**. The Deployment creates and manages ReplicaSets; each
ReplicaSet creates and manages the Pods. Deployment → ReplicaSet → Pod.
{{< /note >}}

4. What do **labels and selectors** do?

{{< note >}}
**Answer:** Labels are key/value tags on objects; a selector matches those labels. The
Deployment's `selector.matchLabels` finds the Pods carrying the matching
`template.metadata.labels` — that's how the controller knows which Pods are its own.
{{< /note >}}

## Next Steps

You set config ad-hoc with `oc set env` — fine for one value, but real apps have many
settings and secrets, and things go wrong. **A02 — Configure & Troubleshoot** gives you
ConfigMaps and Secrets, then breaks something on purpose so you learn to diagnose and fix
it.
