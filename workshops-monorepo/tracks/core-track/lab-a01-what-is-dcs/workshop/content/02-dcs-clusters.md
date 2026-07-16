---
title: Sandbox and PROD Clusters
---

{{< param product_name >}} isn't a single cluster — it runs as **more than one**. As a
tenant you meet two of them: a **Sandbox** cluster and a **PROD** cluster. The important
thing to know up front is that they are **essentially identical**: same platform, same
capabilities, same way of working. Sandbox is not a smaller or weaker version of PROD.

## The one real difference: rollout timing and maintenance

There is exactly **one** axis on which the two clusters differ — **when new platform
features arrive**, and **how much notice you get for maintenance**.

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

That rollout-timing and maintenance-notice difference is the **only** difference. Both
clusters give you the same platform and the same capabilities.

{{< note >}}
**A cluster is not a namespace type.** Don't confuse a **cluster** (Sandbox or PROD)
with a **DEV/PROD namespace type**. A *cluster* is **where** the platform runs — the
whole Sandbox or PROD environment. A *namespace type* is **how a single namespace is
governed** (its controls and lifecycle), which you'll meet later in the course. The
words overlap, but they describe two completely different things.
{{< /note >}}

Read more in the [{{< param product_short >}} cluster model]({{< param dcs_docs_base_url >}}/concepts/clusters).

## Next

Next, a quick grounding in what containers and images actually are.
