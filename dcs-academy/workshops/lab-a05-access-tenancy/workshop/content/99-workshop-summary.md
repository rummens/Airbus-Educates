---
title: Summary
---

You saw who you are on {{< param product_short >}}, what you're allowed to do, and how much
you can use — all by inspecting the platform's real configuration rather than deploying
anything.

## What You Did

- Learned the {{< param product_short >}} tenancy model: **Tenant → Namespaces**, with "project" just meaning "namespace".
- Confirmed your **SSO identity** and current namespace.
- Used `oc auth can-i` to read your permissions, proved you **can** work in your namespace and **cannot** reach `kube-system` (isolation).
- Applied a **Role + RoleBinding** and saw how access is granted.
- Read your **ResourceQuota** and **LimitRange**, and learned a quota increase is an **ITSM request**, not a command.

## Challenge

Do it yourself, unguided: **prove the isolation boundary from the other direction** — confirm
you are *not* allowed to create Deployments in the `kube-system` namespace. Run the check when
ready.

```examiner:execute-test
name: verify-isolation
title: Challenge — you CANNOT create deployments in kube-system
args:
- create
- deployments
- kube-system
timeout: 10
```

{{< note >}}
**Hint:** the command is the same shape as before, just a different verb and namespace:
`oc auth can-i create deployments -n kube-system`. It should answer `no`.
{{< /note >}}

## Check Your Understanding

1. What are the levels of the {{< param product_short >}} tenancy model?

{{< note >}}
**Answer:** Two: a **Tenant** (the org-level unit, for recharging and accountability) that
owns one or more **Namespaces**. "Project" is just OpenShift's word for a namespace — not a
third level.
{{< /note >}}

2. How is one tenant kept isolated from another on a shared cluster?

{{< note >}}
**Answer:** **RBAC** scopes what you can do to your own namespaces (you can't act in others),
and **Network Policies** restrict which workloads can talk to each other.
{{< /note >}}

3. Your workload needs more CPU than your quota allows. What do you do?

{{< note >}}
**Answer:** Raise an **ITSM request** for a quota increase — it's reviewed against capacity
and cost, then applied by the platform. You can't raise your own quota with `oc`.
{{< /note >}}

## Next Steps

Want the full picture of how permissions are wired? **RBAC Deep Dive** takes Roles,
ClusterRoles, and bindings apart. Otherwise, continue the Foundations spine.
