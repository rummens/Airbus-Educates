---
title: Summary
---

You opened up RBAC and saw it's just four objects in a chain — and you built that chain
yourself, then proved it with impersonation.

## What You Did

- Distinguished **Role** (namespaced) from **ClusterRole** (cluster-wide).
- Read **rules** as `apiGroups × resources × verbs`, and saw permissions only ever add.
- Read a **RoleBinding**'s `roleRef` and `subjects`, and the three subject kinds.
- Created a Role + ServiceAccount + RoleBinding and proved the granted and denied verbs with `oc auth can-i --as`.

## Challenge

Do it yourself, unguided: **give `app-viewer` permission to `get configmaps`** as well, by
editing the Role, then prove it. Run the check when ready.

```examiner:execute-test
name: verify-can-i
title: Challenge — app-viewer CAN get configmaps
args:
- get
- configmaps
- app-viewer
- "yes"
timeout: 10
```

{{< note >}}
**Hint:** the Role `pod-service-viewer` has one rule in the core API group (`""`). Add
`configmaps` to that rule's `resources` (it already allows `get`), and re-apply.
{{< /note >}}

{{< note >}}
**Reveal solution** — if you're stuck, run this:

```terminal:execute
command: |-
  oc apply -f - <<'EOF'
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: pod-service-viewer
  rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps"]
    verbs: ["get", "list", "watch"]
  EOF
```
{{< /note >}}

## Check Your Understanding

1. What is the difference between a Role and a ClusterRole?

{{< note >}}
**Answer:** A Role is namespaced — its permissions apply only in its namespace. A
ClusterRole is cluster-wide and reusable (and can grant access to cluster-scoped
resources).
{{< /note >}}

2. A RoleBinding connects two things — what are they?

{{< note >}}
**Answer:** A **subject** (user, group, or ServiceAccount) and a **role** (its `roleRef`).
The binding grants the role's rules to the subject, within the binding's namespace.
{{< /note >}}

3. How do you test what a ServiceAccount is allowed to do, without logging in as it?

{{< note >}}
**Answer:** `oc auth can-i <verb> <resource> --as=system:serviceaccount:<namespace>:<sa>`
— impersonation evaluates the effective permissions and answers yes/no.
{{< /note >}}

## Next Steps

You now understand how access is wired on {{< param product_short >}}. The Security and
Architect tracks build directly on this; the Operators track relies on it for
ServiceAccount permissions.
