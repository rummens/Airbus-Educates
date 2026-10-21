---
title: Summary
---

You created a PostgreSQL instance from a Custom Resource, watched the operator build the
objects behind it, and learned where {{< param product_short >}}'s responsibility ends and
yours begins.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

- **Learned the Operator pattern**: a controller that reconciles a Custom Resource
  toward its desired state, continuously.
- **Distinguished CRD from CR**: the CloudNativePG `Cluster` CRD is the type; `sample-db`
  is the instance you created.
- **Confirmed OLM/OperatorHub installed the Operator** cluster-wide, and that
  {{< param product_short >}}'s OperatorHub is curated and air-gapped.
- **Created a `Cluster` CR** and watched the Operator create its volume claim, Services,
  secrets and Pods without you writing any of them.
- **Stated the {{< param product_short >}} ownership model**: platform owns the
  Operator; you own the instance, its sizing, config, data, backups, and incidents.

## Check Your Understanding

1. What does an Operator's reconciliation loop do?

{{< note >}}
**❓ Answer:** It continuously compares the actual state of the cluster to the desired
state declared in a Custom Resource, and acts to close any gap, for as long as the
Operator runs rather than only once at creation.
{{< /note >}}

2. What's the difference between a CRD and a CR?

{{< note >}}
**❓ Answer:** A CRD (CustomResourceDefinition) defines a new resource *type* — like
`Cluster` for CloudNativePG. A CR (Custom Resource) is an *instance* of that type, the
same way a specific Deployment is an instance of the built-in Deployment type. The
Operator is installed once and defines the CRD; you create as many CRs as you need.
{{< /note >}}

3. On {{< param product_short >}}, who owns the `sample-db` instance you created — the
   platform, or you?

{{< note >}}
**❓ Answer:** You do. The platform owns installing and upgrading the CloudNativePG
Operator and its CRDs; that was done before this lab started. Everything about the
instance itself is yours: sizing, configuration, data, backups, upgrading it when you
choose to, and responding when something goes wrong. On {{< param product_short >}},
services are offered as Operators, not as managed services.
{{< /note >}}

## Next Steps

This lab covered the pattern and the ownership model, using CloudNativePG as an example. A
planned {{< param product_short >}} **Operators / Platform Services** track covers each
service the platform offers this way (**GitLab**, **Argo CD** and **CloudNativePG**), as a
tenant-owned instance you operate day to day. If your team is about to adopt one of those
services, take that track; this workshop is an introduction only.
