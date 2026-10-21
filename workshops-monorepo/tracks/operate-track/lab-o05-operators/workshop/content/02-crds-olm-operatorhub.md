---
title: CRDs, OLM and OperatorHub
---

Two pieces are already on the cluster, put there by the platform: the resource type the
Operator adds, and the mechanism that installed it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/crds
```

## CRD: a new resource type

Every built-in resource you have used (`Deployment`, `Secret`, `Service`) is defined by
Kubernetes itself. A [**CustomResourceDefinition (CRD)**](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
lets an Operator add its own resource type: a new kind of object the API server accepts,
stores and serves exactly like a built-in one.

The CRD is the **type**. An object of that type is a **Custom Resource (CR)**, an instance.
The relationship is the same as `Deployment` against one specific Deployment named
`hello-dcs`, for a type the Operator brought with it.

This lab uses [**CloudNativePG**](https://cloudnative-pg.io/docs/), an Operator for running
PostgreSQL. It adds a CRD named `Cluster`, under its own API group so it never collides with
another `Cluster`-named type, plus supporting CRDs for backups and connection pooling.

Confirm the cluster knows those kinds. **Discovery** (what `oc` itself uses to work out
which types exist) is readable by any authenticated user, so this works from inside your own
namespace without any cluster-wide permission:

```terminal:execute
command: oc api-resources --api-group=postgresql.cnpg.io
```

```examiner:execute-test
name: verify-crds-present
title: Verify the CloudNativePG operator's CRDs are installed
timeout: 10
```

You should see several CRDs ending in `.postgresql.cnpg.io`, including
`clusters.postgresql.cnpg.io`, the one this lab uses. Each line is evidence that the operator
is installed: nobody creates these by hand, and the Operator's installation registered
them.

## Confirm the type is usable

A CRD being present means the API server knows the type. `oc explain` goes one step
further and reads the schema the CRD registered, which is how you find out what fields an
unfamiliar kind accepts without looking for documentation:

```terminal:execute
command: oc explain cluster.spec --api-version=postgresql.cnpg.io/v1 | head -25
```

```section:begin
name: breakdown-explain-cluster
prefix: Breakdown
title: What each part of the command does
```

- **`oc explain cluster.spec`** — prints the schema of the `spec` field of a `Cluster`, with a description of each field.
- **`--api-version=postgresql.cnpg.io/v1`** — picks the CloudNativePG `Cluster`, in case another API group also has a kind named `Cluster`.
- **`| head -25`** — shows only the first 25 lines.

```section:end
name: breakdown-explain-cluster
```

```examiner:execute-test
name: verify-api-resource-present
title: Verify the Cluster (CNPG) kind is registered as an API resource
timeout: 10
```

You get the top-level fields of a `Cluster` spec, with a description for each, served from
the CRD itself.

## How the operator got there: OLM and OperatorHub

Those CRDs did not arrive as hand-written YAML. Operators are installed and upgraded by the
[**Operator Lifecycle Manager (OLM)**](https://olm.operatorframework.io/), which manages an
Operator's install, upgrade and CRDs as one unit, cluster-wide.
[**OperatorHub**](https://operatorhub.io/) is the catalog OLM installs from.

{{< note >}}
**📌 Note:** on {{< param product_short >}}, OperatorHub is **curated and air-gapped**, the
same model as the [Harbor image registry]({{< param dcs_docs_base_url >}}/registry/overview).
Only Operators the platform has vetted and mirrored are offered, and installation is a
platform action. That is why this lab installs nothing: the CRDs you just found show that the
platform already did.
{{< /note >}}

The type exists and its schema is readable. Next, create an instance of it.
