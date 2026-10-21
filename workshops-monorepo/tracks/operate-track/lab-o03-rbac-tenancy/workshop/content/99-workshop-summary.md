---
title: Summary
---

You read the RBAC objects behind Tenant and Namespace, and built your own Role and
RoleBinding.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

- Confirmed the **Tenant → Namespaces** model in depth, and why "project" is not a separate layer.
- Started from `oc auth can-i` and saw isolation deny access outside your own namespace.
- Read the RBAC objects behind that answer, a built-in **ClusterRole** and the
  **RoleBinding** already granting you access, and traced **subject → binding → role →
  rule**.
- Created a **ServiceAccount**, a **Role**, and a **RoleBinding** of your own, and proved
  their exact effect, before and after, with `--as` impersonation, including proving what
  the Role does **not** grant (least privilege).
- Read your namespace's **ResourceQuota** and **LimitRange**, and learned that a quota
  increase is an **ITSM request**, not a self-service edit.

## Check Your Understanding

1. What's the difference between a **Role** and a **ClusterRole**?

{{< note >}}
**❓ Answer:** A Role's permissions apply only inside the namespace it is created in. A
ClusterRole grants the same kind of permissions cluster-wide, and can also be bound
namespace-by-namespace via a RoleBinding when the same permission set is reused in several
namespaces (the built-in `view` role works this way). See the
[Kubernetes RBAC reference](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).
{{< /note >}}

2. What does a **RoleBinding** connect?

{{< note >}}
**❓ Answer:** A subject (User, Group, or ServiceAccount) to a Role or ClusterRole, inside one
namespace. The Role/ClusterRole alone grants nothing to anyone until a binding names a
subject for it.
{{< /note >}}

3. How do you test whether **another** subject — not yourself — has a given permission?

{{< note >}}
**❓ Answer:** `oc auth can-i <verb> <resource> --as=<subject>` — e.g.
`--as=system:serviceaccount:<namespace>:<name>` for a ServiceAccount. It asks the same
`can-i` question on that subject's behalf, without needing to authenticate as them.
{{< /note >}}

## Next Steps

You have now covered *what* a namespace lets you do (RBAC) and *how much* (quota). The other
half of "what your namespace can do" is its **lifecycle posture**: DEV or PROD, and the
controls each one enforces. That is the next lab, **DEV vs PROD Namespaces**. The Role and
RoleBinding skills from this lab are also the prerequisite for **Operators on DCS**, where
what a ServiceAccount is (and is not) allowed to do matters directly.
