---
title: CRDs, OLM and OperatorHub
---

Before you create an instance, two vocabulary items and one piece of machinery.

## CRD vs CR

- A **CustomResourceDefinition (CRD)** adds a *new resource type* to the cluster's API — it
  teaches the API server about, say, a `Cluster` kind for PostgreSQL. Installing an operator
  installs its CRDs.
- A **Custom Resource (CR)** is an *instance* of that type — one actual database you ask for.

You don't create CRDs (the platform does, by installing the operator); you create **CRs**.
Confirm the CloudNativePG operator's type is installed by looking for its CRD:

```terminal:execute
command: oc get crds | grep cnpg
```

```examiner:execute-test
name: verify-crds
title: The operator's CRDs are installed
args:
- cnpg
timeout: 10
```

And that the new kind is a first-class API resource you can use:

```terminal:execute
command: oc api-resources | grep cnpg
```

```examiner:execute-test
name: verify-api-resource
title: The Cluster kind is available
args:
- cnpg
timeout: 10
```

## OLM and OperatorHub

How do those CRDs and the controller get onto the cluster? Through the **Operator Lifecycle
Manager (OLM)** — it installs, updates, and manages operators — and **OperatorHub**, the
catalog you install them from. On {{< param product_short >}}, OperatorHub is **curated and
air-gapped**: only vetted, mirrored operators are available, and the platform team performs
the install cluster-wide.

See it in the console — switch to the **Installed Operators** view:

```dashboard:open-dashboard
name: Console
```

Browse to **Operators → Installed Operators** to see CloudNativePG listed. Then come back
to the terminal:

```dashboard:open-dashboard
name: Terminal
```

{{< note >}}
You never installed the operator — the platform did. That's the model: operators are a
cluster-wide, platform-owned capability. What *you* do is create instances, next.
{{< /note >}}
