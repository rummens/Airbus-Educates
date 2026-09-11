---
title: CRDs, OLM and OperatorHub
---

Before you create anything, it helps to see the two pieces that are already on the
cluster — put there by the platform, not by you — that make an Operator usable at all:
the resource type it adds, and the mechanism that installed it.

## CRD: a new resource type

Every built-in resource you've used (`Deployment`, `Secret`, `Service`) is defined by
Kubernetes itself. A [**CustomResourceDefinition (CRD)**](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
lets an Operator add its *own* resource type — a new kind of object the API server will
accept, store, and serve, exactly like a built-in one. The CRD is the **type**; when you
create an object of that type, that object is a **Custom Resource (CR)** — an *instance*.
The relationship is the same as `Deployment` (the type Kubernetes ships) versus one
specific Deployment named `hello-dcs` (an instance of it) — just for a type the Operator
brought with it instead of one Kubernetes ships out of the box.

This lab uses [**CloudNativePG**](https://cloudnative-pg.io/docs/) — an Operator for
running PostgreSQL — as the example throughout. It adds a CRD named `Cluster` (under its
own API group, so it never collides with any other `Cluster`-named type), plus a handful
of supporting CRDs for backups and connection pooling.

Confirm they're already on the cluster. `oc get crds` lists every CustomResourceDefinition
registered with the API server — `crds` is the plural short name for
CustomResourceDefinition, the same way `po` is short for Pod. Piping to `grep` filters
that (potentially long) list down to just the group we care about:

```terminal:execute
command: oc get crds | grep cnpg
```

```examiner:execute-test
name: verify-crds-present
title: Verify the CloudNativePG operator's CRDs are installed
timeout: 10
```

You should see several CRDs ending in `.postgresql.cnpg.io` — including
`clusters.postgresql.cnpg.io`, the one this lab uses. Each line is proof the operator is
installed: nobody creates these by hand, the Operator's own installation registered them.

## Confirm the type is usable

A CRD being present means the API server *knows about* the type. Check that it's actually
callable the way any other resource type is, with [`oc api-resources`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/openshift-cli-commands.html) —
it lists every resource type the API server currently serves, built-in and CRD-added
alike, which is a useful way to discover what a cluster can do beyond the handful of
types you already know:

```terminal:execute
command: oc api-resources | grep -i postgresql
```

```examiner:execute-test
name: verify-api-resource-present
title: Verify the Cluster (CNPG) kind is registered as an API resource
timeout: 10
```

You'll see a row for `clusters` (kind `Cluster`, API group `postgresql.cnpg.io`) among
the others — the exact information `oc get cluster.postgresql.cnpg.io` needs to know
which object you mean.

## How the operator got there: OLM and OperatorHub

Those CRDs didn't appear by hand-written YAML. Operators are installed and upgraded by
the [**Operator Lifecycle Manager (OLM)**](https://olm.operatorframework.io/), which
manages an Operator's whole lifecycle — install, upgrade, and the CRDs that come with
it — as a unit, cluster-wide, once. [**OperatorHub**](https://operatorhub.io/) is the
catalog OLM installs from: browse available Operators, pick one, and OLM handles the
rest.

{{< note >}}
On {{< param product_short >}}, OperatorHub is **curated and air-gapped** — the same
model as the [Harbor image registry]({{< param dcs_docs_base_url >}}/registry/overview):
only Operators the platform has vetted and mirrored are offered, and installation is a
platform action, not something a tenant triggers themselves. That's why this lab never
installs anything — the CRDs you just found are proof the platform already did.
{{< /note >}}

Take a look at what's installed from the console. Open the Console tab:

```dashboard:open-dashboard
name: Console
```

Browse to the **Custom Resource Definitions** view under the cluster-scoped resources —
you'll find `clusters.postgresql.cnpg.io` listed there, the same object `oc get crds`
showed you, just in a GUI. This console is the Kubernetes web console bound to your
session, not the OpenShift-branded console, so its resource list is generic rather than
grouped by "Installed Operators" the way the full OpenShift console would show it — but
the CRD it added is the same either way.

Once you've had a look, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```

The type exists, and it's callable. Next, create an instance of it.
