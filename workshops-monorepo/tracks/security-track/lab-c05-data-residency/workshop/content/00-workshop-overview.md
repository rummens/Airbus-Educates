---
title: Workshop Overview
---

Welcome. In this workshop, part of **{{< param product_name >}}**, you'll look at the platform
through a **governance and compliance** lens: how {{< param product_short >}} classifies data,
how it guarantees that data stays inside the right **European region**, and how a workload's
placement is expressed and governed. The earlier Security labels hardened the *image* and the
*runtime*; this one places what you run inside the **EU data-residency** frame.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

{{< param product_short >}} runs **on-prem and air-gapped** across a **multi-national European**
footprint (for example Germany and Spain). That is exactly what makes a **data-residency**
guarantee possible: if the data physically cannot leave the platform, keeping it in a permitted
region becomes a structural property, not just a promise on paper. This workshop is mostly
**concept and observe** — you'll read governance artefacts and inspect how placement is
declared, rather than deploy anything.

## What You'll Learn

By the end you will be able to:

- Explain the {{< param product_short >}} **Data Classification** scheme and the multi-national
  **data-residency** guarantee that pins each classification to permitted region(s).
- Describe how workload **placement** is expressed — standard region/zone labels plus
  [`nodeSelector`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) —
  and inspect it in a manifest.
- Read the **Responsibility Matrix (RACI)** to tell platform duties from tenant duties.
- Describe the **Security Exception Process** and the **Terms & Conditions** governing data and
  registry use.
- Identify the tenant **compliance loop**: classify data, tag and place the workload, request an
  exception via **ITSM** when a control can't be met.

## Prerequisites

- **Module A (esp. tenancy & quotas)** — you should know the Tenant → Namespaces model and be
  comfortable running `oc get` with `jsonpath`.
- Familiarity with standard
  [labels/selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
  and [`nodeSelector`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
  — the mechanics of placement — which we build on rather than re-teach.

No governance background is assumed — the classification scheme, RACI, and exception process
are introduced here.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} session namespace. The governance artefacts you'll read — a
classification matrix, a classified workload manifest, and a Responsibility Matrix — ship as
**fixtures** in `~/exercises`. You inspect them with `oc`, `yq`, and `grep`; nothing here is
deployed, because residency is a platform guarantee, not something a tenant edits directly.

## Time and Difficulty

- **Estimated time:** 35 minutes
- **Difficulty:** Intermediate

## Further Reading

- [{{< param product_short >}} governance & compliance]({{< param dcs_docs_base_url >}}/governance/overview) — classification, RACI, exceptions, T&Cs.
- [Labels and selectors (Kubernetes)](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- [Assigning Pods to nodes (Kubernetes)](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
