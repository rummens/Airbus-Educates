---
title: Sandbox and PROD Clusters
---

{{< param product_name >}} runs as **more than one** cluster. As a tenant you use two: a
**Sandbox** cluster and a **PROD** cluster. They run the same platform with the same
capabilities, and you work with them the same way. Sandbox is not a smaller version of
PROD.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/clusters
```

## How they differ: rollout timing and maintenance

The clusters differ in one way: **when new platform features arrive**, and **how much
notice you get for maintenance**.

New platform features flow through a monthly pipeline:

**DEV/QA → Sandbox → PROD**

A feature that is ready lands on **Sandbox in month 1** and on **PROD in month 2** — so
PROD always runs the same platform, just **one month behind**, once features have been
proven on Sandbox.

- **Sandbox** — where new platform features land first. Because it moves faster,
  maintenance windows are announced **shorter-term**, which means a slightly lower SLA.
  Good for trying the newest capabilities.
- **PROD** — where you run production workloads. Features arrive a month later, already
  proven on Sandbox. Maintenance is announced with **longer notice** and it carries a
  **higher SLA**.

{{< note >}}
**⚠️ A cluster is not a namespace type.** Don't confuse a **cluster** (Sandbox or PROD)
with a **DEV/PROD namespace type**. A *cluster* is **where** the platform runs — the
whole Sandbox or PROD environment. A *namespace type* is **how a single namespace is
governed** (its controls and lifecycle), which you'll meet later in the course. The
words overlap, but they mean different things.
{{< /note >}}

Read more in the [{{< param product_short >}} cluster model]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/clusters).

## Next

Next: what containers and images are.
