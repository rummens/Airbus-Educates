---
title: What Is a Namespace?
---

You've been working *inside* a [**Namespace**](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
this whole time without a name for it. A namespace groups and isolates a set of
workloads: the Deployments, Pods, Services, ConfigMaps and so on that belong together.
Objects in one namespace don't collide with — or see — objects in another.

On {{< param product_short >}}, the namespace is also the **unit of consumption**: you
request namespaces and ship applications into them. That's what "Namespace as a Service"
means — the namespace, not a server, is the thing you're given. Learn more in the
[{{< param product_short >}} tenancy & access overview]({{< param dcs_docs_base_url >}}/concepts/tenancy-and-access).

## Your active namespace

Your **active namespace** is the one your `oc` context points at right now — the default
for every command that doesn't say otherwise. Show it:

```terminal:execute
command: oc project
```

```examiner:execute-test
name: verify-active-namespace
title: Verify you have an active namespace
timeout: 10
```

{{< note >}}
{{< param product_short >}} shows this as a **project**. On OpenShift, "project" is just
the word for a namespace with a little extra metadata — it is **not** a separate layer
above it. We'll come back to that on the Tenancy page.
{{< /note >}}

## What's in it

Everything you create lands here unless you say otherwise. List it all:

```terminal:execute
command: oc get all
```

```examiner:execute-test
name: verify-get-all
title: Verify oc get all runs against your namespace
timeout: 10
```

In this fresh session your namespace is empty — that's fine. The point is that
*whatever* you deploy is scoped to this one namespace. Next, you'll prove that scoping is
real by running the same app in two *other* namespaces side by side.
