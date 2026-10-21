---
title: Start From "Can I?"
---

Start from the question the RBAC objects answer.
[`oc auth can-i`](https://kubernetes.io/docs/reference/access-authn-authz/authorization/#checking-api-access)
asks the cluster whether you, or anyone else, may perform an action, without reading a single
Role or RoleBinding first.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/can-i
```

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

You get a table: a `Verbs` column (`get`, `list`, `create`, `delete`, …) against `Resources`
and `APIGroups`. That is the full set of things you may do in your namespace right now,
normally granted by a RoleBinding to a broad role such as `admin` or `edit`, which you find on
the next page.

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

You get back `yes`. Your namespace access includes creating workloads, which matches what
you have been doing in every lab so far.

## Ask about someone else's namespace

Now point the same question at a namespace that is not yours:

```terminal:execute
command: oc auth can-i get pods -n kube-system
```

`-n <namespace>` (short for `--namespace`) targets a **different** namespace than the one
you are in. Everywhere else in this lab, commands default to your own namespace.

```examiner:execute-test
name: verify-can-i-get-pods-kube-system-no
title: Verify access to another namespace is denied
timeout: 10
```

You get back `no`. Your tenant's access does not extend into `kube-system` or any other
namespace that is not yours, however much you can do inside your own.

The two questions look the same but get different answers, because RBAC decides per
namespace, per resource and per verb. The next page shows the objects that make that decision.
