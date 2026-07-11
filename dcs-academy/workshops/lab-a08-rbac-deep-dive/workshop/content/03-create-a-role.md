---
title: Create a Role and Prove It
---

Now build the chain yourself: a Role with a couple of rules, a ServiceAccount to be the
subject, and a RoleBinding to connect them — then prove the permissions took effect.

## Create the Role

```editor:open-file
file: ~/exercises/role-viewer.yaml
```

It grants read-only (`get`, `list`, `watch`) on Pods and Services — one rule in the core
API group. Apply it:

```terminal:execute
command: oc apply -f role-viewer.yaml
```

```examiner:execute-test
name: verify-role
title: The Role was created
args:
- pod-service-viewer
timeout: 10
```

## Create the subject and binding

```editor:open-file
file: ~/exercises/rolebinding-viewer.yaml
```

This creates a **ServiceAccount** `app-viewer` and a **RoleBinding** that grants it the
role. Apply it:

```terminal:execute
command: oc apply -f rolebinding-viewer.yaml
```

```examiner:execute-test
name: verify-rolebinding
title: The RoleBinding was created
args:
- app-viewer-binding
timeout: 10
```

## Prove it — the granted verb

Use impersonation (`--as`) to ask what the ServiceAccount can do. It should be allowed to
**get pods**:

```terminal:execute
command: oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:app-viewer
```

Expected output: `yes`.

```examiner:execute-test
name: verify-can-i
title: app-viewer CAN get pods
args:
- get
- pods
- app-viewer
- "yes"
timeout: 10
```

## Prove it — the denied verb (least privilege)

The role granted only read verbs, so **delete** must be refused:

```terminal:execute
command: oc auth can-i delete pods --as=system:serviceaccount:$SESSION_NAMESPACE:app-viewer
```

Expected output: `no`.

```examiner:execute-test
name: verify-can-i
title: app-viewer CANNOT delete pods
args:
- delete
- pods
- app-viewer
- "no"
timeout: 10
```

That `no` is least privilege working: the subject has exactly the verbs its role grants and
nothing more. Change the rules, and the answer changes with them.
