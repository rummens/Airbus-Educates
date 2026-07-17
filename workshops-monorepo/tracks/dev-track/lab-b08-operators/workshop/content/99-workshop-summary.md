---
title: Summary
---

You went from "an Operator adds a resource type" to a running, reconciled PostgreSQL
instance — and, more importantly, learned exactly where {{< param product_short >}}'s
responsibility for it ends and yours begins.

## What You Did

- **Learned the Operator pattern**: a controller that reconciles a Custom Resource
  toward its desired state, continuously.
- **Distinguished CRD from CR**: the CloudNativePG `Cluster` CRD is the type; `sample-db`
  is the instance you created.
- **Confirmed OLM/OperatorHub installed the Operator** cluster-wide, and that
  {{< param product_short >}}'s OperatorHub is curated and air-gapped.
- **Created a `Cluster` CR** and watched it go from an empty status to
  `Cluster in healthy state`, reconciled by the Operator without you touching a single
  Pod.
- **Stated the {{< param product_short >}} ownership model**: platform owns the
  Operator; you own the instance — its sizing, config, data, backups, and incidents.

## Check Your Understanding

1. What does an Operator's reconciliation loop actually do?

{{< note >}}
**Answer:** It continuously compares the actual state of the cluster to the desired
state declared in a Custom Resource, and acts to close any gap — not just once at
creation, but for as long as the Operator runs.
{{< /note >}}

2. What's the difference between a CRD and a CR?

{{< note >}}
**Answer:** A CRD (CustomResourceDefinition) defines a new resource *type* — like
`Cluster` for CloudNativePG. A CR (Custom Resource) is an *instance* of that type, the
same way a specific Deployment is an instance of the built-in Deployment type. The
Operator is installed once and defines the CRD; you create as many CRs as you need.
{{< /note >}}

3. On {{< param product_short >}}, who owns the `sample-db` instance you created — the
   platform, or you?

{{< note >}}
**Answer:** You do. The platform owns installing and upgrading the CloudNativePG
Operator and its CRDs — that part was already done before this lab started. Everything
about the instance itself — sizing, configuration, data, backups, upgrading it when you
choose to, and responding when something goes wrong — is yours. This is the core
{{< param product_short >}} distinction: Operators, not managed-aaS.
{{< /note >}}

## Next Steps

This lab kept things at the pattern and ownership level, using CloudNativePG only as a
concrete example. {{< param product_short >}}'s dedicated **Operators / Platform
Services** track goes deep on each service the platform actually offers this way —
**GitLab**, **Argo CD**, and **CloudNativePG** again, this time as a real, day-2-operated
tenant database rather than a teaching example. If your team is about to adopt any of
those services, that track is where the depth lives — this workshop was the on-ramp to
it, not a substitute for it.
