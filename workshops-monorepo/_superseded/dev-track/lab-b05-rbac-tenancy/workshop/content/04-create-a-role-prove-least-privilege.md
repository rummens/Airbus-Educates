---
title: Create a Role and Prove Least Privilege
---

Reading someone else's RBAC objects is one thing; now build the chain yourself, end to end,
for a subject you create — and prove exactly what it can and can't do.

## Create a subject to test with

You'll bind permissions to a [**ServiceAccount**](https://kubernetes.io/docs/concepts/security/service-accounts/) —
a non-human identity, normally used by a workload rather than a person — so the permissions
you prove belong to this ServiceAccount alone, not mixed in with your own broader access.

```editor:open-file
file: ~/exercises/serviceaccount-viewer.yaml
```

Create it:

```terminal:execute
command: oc apply -f serviceaccount-viewer.yaml
```

```examiner:execute-test
name: verify-serviceaccount-created
title: Verify the viewer-bot ServiceAccount exists
timeout: 10
```

## Check its access before granting anything

`viewer-bot` exists, but no Role or RoleBinding names it yet, so it should have no access at
all. Prove that with `--as`, which lets you ask `can-i` **on behalf of another subject**
instead of yourself — a central tool for testing RBAC without having to actually log in as
that subject. The value is the same `system:serviceaccount:<namespace>:<name>` format you
just read in a RoleBinding's `Subjects` section:

```terminal:execute
command: oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:viewer-bot
```

```examiner:execute-test
name: verify-can-i-get-pods-as-before
title: Verify viewer-bot has no access yet (before)
timeout: 10
```

You should get back `no` — the **before** state. No rule grants `viewer-bot` anything yet.

## Author the Role

Open the Role you'll apply:

```editor:open-file
file: ~/exercises/role-viewer.yaml
```

Its one rule grants `get`, `list` and `watch` — read-only verbs — on `pods` and
`configmaps`. Nothing else: no `create`, no `delete`, no other resource types. Apply it:

```terminal:execute
command: oc apply -f role-viewer.yaml
```

```examiner:execute-test
name: verify-role-viewer-created
title: Verify the role-viewer Role exists with the expected rule
timeout: 10
```

A Role alone grants nothing to anyone — it's a shelf of permissions with no one assigned to
it yet. The RoleBinding is what connects it to `viewer-bot`.

## Bind the Role to the ServiceAccount

```editor:open-file
file: ~/exercises/rolebinding-viewer.yaml
```

Its `subjects` entry names `viewer-bot` with a `namespace` placeholder,
`${SESSION_NAMESPACE}` — filled in with your real namespace at apply time by
[`envsubst`](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html),
the same substitution pattern used for `${DCS_REGISTRY}` elsewhere in these labs:

```terminal:execute
command: envsubst < rolebinding-viewer.yaml | oc apply -f -
```

```examiner:execute-test
name: verify-rolebinding-viewer-created
title: Verify the rolebinding-viewer RoleBinding exists and binds viewer-bot
timeout: 10
```

## Check its access again — the after state

Run the exact same `can-i` check as before:

```terminal:execute
command: oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:viewer-bot
```

```examiner:execute-test
name: verify-can-i-get-pods-as-after
title: Verify viewer-bot can now get pods (after)
timeout: 15
retries: .INF
delay: 2
```

Now it returns `yes`. Same question, same subject — the only thing that changed between
**before** and **after** is the Role + RoleBinding you just created. That's the whole
mechanism, made visible.

## Prove least privilege

The rule you wrote granted read-only verbs. Prove it doesn't grant anything more by asking
for a verb you never included:

```terminal:execute
command: oc auth can-i delete pods --as=system:serviceaccount:$SESSION_NAMESPACE:viewer-bot
```

```examiner:execute-test
name: verify-can-i-delete-pods-as-no
title: Verify viewer-bot cannot delete pods (least privilege)
timeout: 10
```

`no` — `viewer-bot` can read pods, and only pods and configmaps, and only read them. This is
**least privilege** in practice: the RoleBinding grants exactly the rule you wrote, nothing
implied and nothing extra.

You've now walked the whole chain in both directions: read someone else's (last page), and
authored, applied and proved your own (this page). Last stop: the budget your namespace
operates inside.
