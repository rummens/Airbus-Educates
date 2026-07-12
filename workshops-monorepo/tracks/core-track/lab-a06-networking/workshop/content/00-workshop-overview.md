---
title: Workshop Overview
---

In this workshop, part of **{{< param product_name >}}**, you'll take an app that only you
can reach and make it reachable — first in the browser through the session proxy, then via
an OpenShift **Route** — and you'll see the limits {{< param product_short >}} puts on
network traffic on an air-gapped platform.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, and the clickable actions you'll use here.
{{< /note >}}

You already know how to deploy a workload and reach it in-cluster. This workshop is about
**exposure**: how traffic gets from a browser to your Pod, the DCS path it travels, and why
some traffic (like calls out to the internet) simply doesn't go anywhere.

## What You'll Learn

By the end you will be able to:

- Reach a **Service** in-cluster by DNS.
- Expose an app to the browser via the **session proxy**.
- Create an OpenShift **Route** and explain the DCS chain: Service → Route → External Load Balancer with DCS-managed DNS.
- Explain why a Route on {{< param product_short >}} requires a **PROD-type namespace**.
- Read a **Network Policy** and explain how it isolates workloads, and why **egress** is restricted on an air-gapped platform.

## Prerequisites

- **lab-a02-kubernetes-essentials** — you should be comfortable applying a Deployment and Service and using `oc`.

## Your Environment

A **split terminal**, an editor, the web console, and an **App** tab that appears once you
expose the sample app through the session proxy. The sample image is served from the
{{< param product_short >}} Harbor registry.

## Time and Difficulty

- **Estimated time:** 55 minutes
- **Difficulty:** Beginner
