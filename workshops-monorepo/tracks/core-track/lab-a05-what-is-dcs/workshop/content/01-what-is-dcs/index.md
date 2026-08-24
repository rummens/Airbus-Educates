---
title: What is DCS?
---

**{{< param product_name >}}** is Airbus Defence and Space's on-prem, multi-national
(European) container platform, built on Red Hat OpenShift. It gives teams a governed,
secure place to run containerised applications without managing the underlying
infrastructure — and because it runs on-premises and **air-gapped**, everything you
need (images, tools) is provided from within the platform.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/platform
```

{{< note >}}
**Who it is for.** {{< param product_short >}} is the container platform of **Airbus
Defence and Space** — its tenants are D&S programmes and teams. Other Airbus divisions run
their own platforms; the section below explains why D&S built its own rather than joining
one of them.
{{< /note >}}

## Why DCS?

Airbus Commercial adopted OpenShift to modernise how applications are built and run.
Airbus Defence and Space faces the same need at greater scale and under stricter
security and sovereignty requirements — which is what {{< param product_short >}}
delivers: a **Namespace as a Service** platform where teams request namespaces and ship
applications, while the platform handles the clusters, security, and compliance.

The payoff for you as a tenant: it's **air-gapped and sovereign** (your workloads and
data stay inside the platform), it's **managed** (the platform team runs the clusters,
security, and compliance), and it's **self-service** (you request a namespace and ship,
without raising infrastructure tickets). Learn more in the
[{{< param product_short >}} services overview]({{< param dcs_docs_base_url >}}/services).

![DCS at a glance](dcs-architecture.svg)

## Next

Next, you'll see how {{< param product_short >}} is delivered as more than one cluster.
