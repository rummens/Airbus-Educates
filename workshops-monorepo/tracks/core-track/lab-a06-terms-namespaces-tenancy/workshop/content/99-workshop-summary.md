---
title: Summary
---

You now have the vocabulary — and you've *seen* the thing the words describe.

## What You Did

- Named the **Namespace**: the {{< param product_short >}} unit of isolation and
  consumption, and found your **active** one with `oc project`.
- Deployed the **same app into two namespaces** and watched identical names coexist.
- Proved **actions don't leak**: scaling `app-a` to zero left `app-b` running.
- Listed why tenants split into namespaces: separate DEV/QA/PROD instances, blast-radius
  isolation, independent quotas/RBAC, and naming freedom.
- Placed it all in the **Tenant → Namespaces** model — no "project" layer — and named the
  **DEV/PROD** namespace types.

## Check Your Understanding

1. What does a **namespace** isolate?

{{< note >}}
**Answer:** The objects within it (Deployments, Pods, Services, ConfigMaps, …), their
**names**, and **actions** taken on them. Objects in one namespace don't see or affect
objects in another.
{{< /note >}}

2. Give **one concrete reason** to run multiple namespaces.

{{< note >}}
**Answer:** Any of: separate DEV/QA/PROD instances of one app; team / blast-radius
isolation; independent quotas and RBAC; naming freedom (no cross-team name coordination).
{{< /note >}}

3. Is **"project"** a separate layer between Tenant and Namespace on {{< param product_short >}}?

{{< note >}}
**Answer:** No. "Project" is just OpenShift's word for a namespace. The model is two
levels only: **Tenant → Namespaces**.
{{< /note >}}

## Next Steps

That's the *landscape*. The **deep model** is the Developer track: **B05** (RBAC, Tenancy
& Namespaces — the access rules in full) and **B06** (DEV vs PROD by policy — how PROD is
enforced with Kyverno and why only PROD can expose apps with a Route).
