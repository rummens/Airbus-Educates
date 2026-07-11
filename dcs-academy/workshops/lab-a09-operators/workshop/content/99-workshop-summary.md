---
title: Summary
---

You met the Operator pattern, created a real Custom Resource, watched an operator reconcile
it into a running database, and — most importantly — learned who owns what on
{{< param product_short >}}.

## What You Did

- Explained the **Operator pattern**: a controller reconciling a Custom Resource toward desired state.
- Distinguished a **CRD** (a new type) from a **CR** (an instance), and confirmed the operator's CRDs are installed.
- Learned that **OLM/OperatorHub** install operators cluster-wide — done by the platform, curated and air-gapped on {{< param product_short >}}.
- Created a CloudNativePG `Cluster` CR and watched the operator build a PostgreSQL instance.
- Learned the **DCS ownership model**: platform owns the operator; **you** own the instance (config, data, backups, upgrades, day-2).

## Check Your Understanding

1. What does an Operator do, in one sentence?

{{< note >}}
**Answer:** It's a controller that continuously reconciles a Custom Resource toward its
desired state — encoding the operational knowledge for one application.
{{< /note >}}

2. What's the difference between a CRD and a CR?

{{< note >}}
**Answer:** A CRD defines a new resource *type* (installed with the operator); a CR is an
*instance* of that type (which you create).
{{< /note >}}

3. On {{< param product_short >}}, who owns the database instance an operator manages for you?

{{< note >}}
**Answer:** **You**, the tenant. DCS provides and maintains the *operator*; you own the
*instance* — its config, data, backups, upgrades, monitoring, and incidents. It is not a
managed DBaaS.
{{< /note >}}

## Next Steps

This is the foundation for the **Operators track (Module F)**, where you apply this model to
real services: **GitLab**, **Argo CD**, and **CloudNativePG** — each time provisioning an
instance you own.
