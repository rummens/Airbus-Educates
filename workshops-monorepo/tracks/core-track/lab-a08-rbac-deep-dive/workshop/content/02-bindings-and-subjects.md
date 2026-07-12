---
title: Bindings and Subjects
---

A role on its own grants nothing — it's just a named set of permissions. A **binding** is
what connects those permissions to a **subject**. This page reads the bindings already in
your namespace.

## List the bindings

```terminal:execute
command: oc get rolebindings -o wide
```

```examiner:execute-test
name: verify-clusterroles
title: RBAC objects are readable
timeout: 10
```

The `-o wide` output shows each binding's **role** and its **subjects** side by side — that's
the middle of the chain made visible.

## Read one binding

Pick one and describe it:

```terminal:execute
command: oc describe rolebinding -n $SESSION_NAMESPACE $(oc get rolebindings -o name | head -n1 | cut -d/ -f2)
```

Two fields matter:

- **RoleRef** — which Role or ClusterRole's permissions this binding grants. (A RoleRef is
  immutable; to change the role you replace the binding.)
- **Subjects** — who gets them. A subject is one of three kinds:
  - a **User** (a human identity, e.g. from SSO),
  - a **Group** (many users at once),
  - a **ServiceAccount** (a non-human identity used by workloads).

A **RoleBinding** grants within its namespace; a **ClusterRoleBinding** grants cluster-wide.
Binding a *ClusterRole* with a *RoleBinding* is a common trick — it reuses a cluster-wide
permission set but scopes it to one namespace.

{{< note >}}
This is exactly what `oc auth can-i` evaluates under the hood: it walks every binding that
names you (or your groups/ServiceAccount), collects the referenced rules, and answers
yes/no. Next you'll create the objects and watch the answer change.
{{< /note >}}
