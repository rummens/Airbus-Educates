---
title: Workshop Overview
---

Welcome to the Developer track. In this workshop, part of **{{< param product_name >}}**,
you'll do the thing every developer does first on a container platform: take an application
from an image in the registry to a **running, reachable workload** in your own namespace —
and confirm it actually responds.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

In Foundations you learned the pieces in isolation. Here you put them together as a
**developer workflow** on one real application:

- **Deploy** the app from a Harbor image with a Deployment.
- **Give it a stable address** with a Service.
- **Expose it** so you can open it in a browser.
- **Iterate** on it the way you would day to day.

You'll meet the **`hello-dcs`** sample app here and keep working with it through the rest of
the Developer track — later workshops add configuration, health probes, and storage to the
very same manifests. We don't just run commands: for each step you'll learn *what* you're
doing, *why* it matters, and *how* it fits the workflow.

## What You'll Learn

By the end you will be able to:

- Deploy the sample app to your DEV namespace with a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and a [Service](https://kubernetes.io/docs/concepts/services-networking/service/).
- Expose the app through the workshop **session ingress** and reach it in a browser.
- Verify the app is healthy from both the CLI and the web console.
- Explain why self-service exposure in a DEV namespace uses the session proxy, while a real external **Route** requires a PROD namespace.

## Prerequisites

- **Module A (Foundations)** — you should be comfortable with `oc`, and with what a Deployment and Service are (**A02**), the DEV/PROD namespace model (**A03**), and in-cluster networking (**A06**). This workshop builds directly on those.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} **DEV namespace** — a native OpenShift project that is
self-service, with no Kyverno enforcement to get in your way. The sample application image
is served from the {{< param product_short >}} Harbor registry.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Beginner

Ready? Open the Deployment manifest you'll start from:

```editor:open-file
file: ~/exercises/deployment.yaml
```
