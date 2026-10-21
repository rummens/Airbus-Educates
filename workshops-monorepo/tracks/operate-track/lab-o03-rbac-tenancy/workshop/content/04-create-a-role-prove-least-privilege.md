---
title: Create a Role and Prove Least Privilege
---

Now build the chain yourself, end to end, for a subject you create, and check what it
can and cannot do.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/least-privilege
```

## Create a subject to test with

You bind permissions to a [**ServiceAccount**](https://kubernetes.io/docs/concepts/security/service-accounts/),
which is a non-human identity normally used by a workload rather than a person. That keeps
the permissions you are testing separate from your own broader access.

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

`viewer-bot` exists, but no Role or RoleBinding names it yet, so it should have no access.
Check that with `--as`, which asks `can-i` **on behalf of another subject**. That is how you
test RBAC without logging in as that subject. The value uses the same
`system:serviceaccount:<namespace>:<name>` format you read in a RoleBinding's `Subjects`
section:

```terminal:execute
command: oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:viewer-bot
```

```examiner:execute-test
name: verify-can-i-get-pods-as-before
title: Verify viewer-bot has no access yet (before)
timeout: 10
```

You get back `no`. That is the **before** state: no rule grants `viewer-bot` anything.

## Author the Role

Open the Role you will apply:

```editor:open-file
file: ~/exercises/role-viewer.yaml
```

Its one rule grants the read-only verbs `get`, `list` and `watch` on `pods` and
`configmaps`, and nothing else. Apply it:

```terminal:execute
command: oc apply -f role-viewer.yaml
```

```examiner:execute-test
name: verify-role-viewer-created
title: Verify the role-viewer Role exists with the expected rule
timeout: 10
```

A Role on its own grants nothing to anyone. The RoleBinding is what connects it to
`viewer-bot`.

## Bind the Role to the ServiceAccount

```editor:open-file
file: ~/exercises/rolebinding-viewer.yaml
```

Its `subjects` entry names `viewer-bot` with a `namespace` placeholder,
`${SESSION_NAMESPACE}`, filled in with your real namespace at apply time by
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

Now it returns `yes`. Same question, same subject, and the only change between **before**
and **after** is the Role and RoleBinding you created.

## Prove least privilege

The rule you wrote granted read-only verbs. Prove it does not grant anything more by asking
for a verb you never included:

```terminal:execute
command: oc auth can-i delete pods --as=system:serviceaccount:$SESSION_NAMESPACE:viewer-bot
```

```examiner:execute-test
name: verify-can-i-delete-pods-as-no
title: Verify viewer-bot cannot delete pods (least privilege)
timeout: 10
```

You get back `no`. `viewer-bot` can only read pods and configmaps: the RoleBinding grants the
rule you wrote, and nothing more.

The last page covers the quota your namespace works within.
