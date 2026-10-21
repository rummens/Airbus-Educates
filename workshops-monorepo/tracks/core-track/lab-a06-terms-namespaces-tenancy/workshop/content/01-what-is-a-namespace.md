---
title: What Is a Namespace?
---

You have been working inside a [**Namespace**](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
this whole time, without a name for it.

A namespace **groups** and **isolates** a set of workloads — the Deployments, Pods,
Services, ConfigMaps and so on that belong together.

Objects in one namespace do not see or collide with objects in another.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/namespace
```

On {{< param product_short >}} the namespace is also the **unit of consumption**: you
request namespaces and ship applications into them.

"Namespace as a Service" means that {{< param product_short >}} gives you namespaces, not
servers.

Learn more in the
[{{< param product_short >}} tenancy & access overview]({{< param dcs_docs_base_url >}}/services/tenants).

{{< note >}}
**💡 Think of an office building.** The **Tenant** is your organisation renting space in it:
named on the contract, billed monthly, accountable for what happens inside. A **Namespace**
is one room your organisation was given; what is in it stays separate from the rooms next
door. **RBAC** decides who holds a key to which room. The **PROD** rooms have the alarm
system switched on and follow stricter rules.
The platform team runs the building; you decide what happens in your rooms.
{{< /note >}}

## Your active namespace

Your **active namespace** is the one your `oc` context points at right now — the default
for every command that does not name a different one. Show it with `oc project`, which
prints the active namespace and the cluster server it is on:

```terminal:execute
command: oc project | tee ~/exercises/project.txt
```

```examiner:execute-test
name: verify-active-namespace
title: Verify you have an active namespace
timeout: 10
```

{{< note >}}
**📌 Note:** {{< param product_short >}} shows this as a **project**. On OpenShift, "project" is just
the word for a namespace with a little extra metadata — it is **not** a separate layer
above it. We'll come back to that on the Tenancy page.
{{< /note >}}

## What's in it

Everything you create lands here unless you say otherwise. List your workloads. Passing
a comma-separated list of kinds (`deployments,pods,services`) asks `oc` for all three at
once, so you see the whole picture in a single command:

```terminal:execute
command: oc get deployments,pods,services 2>&1 | tee ~/exercises/workloads.txt
```

```examiner:execute-test
name: verify-get-all
title: Verify you can list workloads in your namespace
timeout: 10
```

In this fresh session your namespace is empty. Whatever you deploy is scoped to this
namespace. Next, you test that by running the same app in two *other* namespaces side by
side.
