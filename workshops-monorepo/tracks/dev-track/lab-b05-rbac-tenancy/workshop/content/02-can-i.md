---
title: Start From "Can I?"
---

Before opening up the RBAC objects, start from the question they answer.
[`oc auth can-i`](https://kubernetes.io/docs/reference/access-authn-authz/authorization/#checking-api-access)
asks the cluster, in real time, whether *you* (or anyone else, as you'll see later) are
allowed to perform an action — without you having to read a single Role or RoleBinding
first.

## Everything you can do here

List every permission you currently hold in your namespace:

```terminal:execute
command: oc auth can-i --list
```

```examiner:execute-test
name: verify-can-i-list
title: Verify your permission list is returned
timeout: 10
```

You'll see a table: a `Verbs` column (`get`, `list`, `create`, `delete`, …) against
`Resources` and `APIGroups` columns. This is the full, concrete set of things you're allowed
to do in your namespace right now — normally granted by a RoleBinding to a broad role like
`admin` or `edit`, which you'll go and find on the next page.

## Ask about one specific action

Rather than reading the whole list, ask a direct yes/no question:

```terminal:execute
command: oc auth can-i create deployments
```

```examiner:execute-test
name: verify-can-i-create-deployments-yes
title: Verify you can create Deployments in your own namespace
timeout: 10
```

You should get back exactly `yes`. Your namespace access includes creating workloads — that
matches what you've been doing in every lab so far.

## Ask about someone else's namespace

Now point the same question at a namespace that isn't yours:

```terminal:execute
command: oc auth can-i get pods -n kube-system
```

Here, `-n <namespace>` (short for `--namespace`) targets a **different** namespace than the
one you're currently in — everywhere else in this lab, commands default to your own
namespace, so this is the one deliberate exception.

```examiner:execute-test
name: verify-can-i-get-pods-kube-system-no
title: Verify access to another namespace is denied
timeout: 10
```

You should get back `no`. This is namespace isolation in action: your tenant's access
doesn't extend into `kube-system` or any other namespace that isn't yours — regardless of
how much you can do inside your own.

Two identical-looking questions, two different answers. Something behind the scenes decides
this per namespace, per resource, per verb. Next page: what that something actually is.
