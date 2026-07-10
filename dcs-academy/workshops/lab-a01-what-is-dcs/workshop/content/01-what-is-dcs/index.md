---
title: What is DCS?
---

**{{< param product_name >}}** is Airbus Defence and Space's on-prem, multi-national
(European) container platform, built on Red Hat OpenShift. It gives teams a governed,
secure place to run containerised applications without managing the underlying
infrastructure — and because it runs on-premises and **air-gapped**, everything you
need (images, tools) is provided from within the platform.

## From Virtual Machines to Containers

Think of a **virtual machine** like a private house: it brings its own foundation,
plumbing, and walls — a full operating system — which is powerful but heavy. A
**container** is more like an apartment in a modern building: it carries only what your
application needs and shares the building's infrastructure. Containers start in seconds,
are lightweight, and run the same way everywhere.

A [container image](https://kubernetes.io/docs/concepts/containers/images/) is the
blueprint; a [container](https://kubernetes.io/docs/concepts/containers/) is a running
instance of that blueprint.

## Why DCS?

Airbus Commercial adopted OpenShift to modernise how applications are built and run.
Airbus Defence and Space faces the same need at greater scale and under stricter
security and sovereignty requirements — which is what {{< param product_short >}}
delivers: a **Namespace as a Service** platform where teams request namespaces and ship
applications, while the platform handles the clusters, security, and compliance.

{{< param product_short >}} runs your workloads on a **shared cluster** by default (the
most efficient option, with tenants isolated from one another), with **dedicated
managed clusters** available where isolation or capacity needs demand it. Learn more in
the [{{< param product_short >}} services overview]({{< param dcs_docs_base_url >}}/services/overview).

![DCS at a glance](dcs-architecture.svg)

## Next

Next, you'll open your environment and run your first commands.
