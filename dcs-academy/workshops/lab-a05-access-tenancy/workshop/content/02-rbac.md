---
title: What You're Allowed To Do
---

Your identity from the last page only matters because of what it *permits*. On
{{< param product_short >}} that's decided by
[RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) — role-based access
control. This page keeps it to the basics: reading your own access and proving its boundary.
(The full object-level treatment is the RBAC deep-dive lab.)

## What can I do here?

The most useful RBAC command asks the cluster directly. List everything you're allowed to do
in your current namespace:

```terminal:execute
command: oc auth can-i --list
```

You'll see a table of resources and the verbs you hold on them. This is your effective access
in this namespace, computed from every role bound to your identity.

```examiner:execute-test
name: verify-can-i-list
title: Your permissions are listable
timeout: 10
```

Ask a specific question — can you create Deployments here?

```terminal:execute
command: oc auth can-i create deployments
```

Expected: `yes` — this is your namespace, so you can run workloads in it.

```examiner:execute-test
name: verify-self-can-i
title: You CAN create deployments in your namespace
args:
- create
- deployments
- "yes"
timeout: 10
```

## The boundary

Now the important half — your access **stops** at your tenant's namespaces. Ask whether you
can read Pods in `kube-system`, a namespace that isn't yours:

```terminal:execute
command: oc auth can-i get pods -n kube-system
```

Expected: `no`. That single word is multi-tenancy working: on a shared cluster you simply
cannot see into other tenants' or the platform's namespaces.

```examiner:execute-test
name: verify-isolation
title: You CANNOT read pods in kube-system
args:
- get
- pods
- kube-system
timeout: 10
```

## See a binding take effect

Access comes from **RoleBindings** — a binding grants a **Role** (a set of permissions) to a
subject. Apply a small one in your own namespace:

```editor:open-file
file: ~/exercises/sample-role.yaml
```

It defines a `pod-reader` Role (read Pods) and binds it to authenticated users. Apply it:

```terminal:execute
command: oc apply -f sample-role.yaml
```

```examiner:execute-test
name: verify-role
title: The pod-reader Role was created
args:
- pod-reader
timeout: 10
```

```examiner:execute-test
name: verify-rolebinding
title: The pod-reader RoleBinding was created
args:
- pod-reader-binding
timeout: 10
```

You can list the bindings in your namespace to see it alongside the others:

```terminal:execute
command: oc get rolebindings
```

That's the whole basis of access: roles hold permissions, bindings grant them to you, and
`oc auth can-i` tells you the result. The deep-dive lab takes these objects apart properly.
