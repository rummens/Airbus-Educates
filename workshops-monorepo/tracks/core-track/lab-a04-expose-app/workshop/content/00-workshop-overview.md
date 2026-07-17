---
title: "Expose Your App"
---

So far your app has only ever answered a **local tunnel** — a `port-forward` that lived and
died with a single terminal command. That's fine for a quick test, useless for anything
real. In this workshop on **{{< param product_name >}}** you'll give the app a proper
address: first a stable in-cluster name, then a real external URL that anyone can reach.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the {{< param product_short >}} traffic chain: [Service](https://kubernetes.io/docs/concepts/services-networking/service/) → [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) → external load balancer, with managed DNS.
- Give the app a stable in-cluster address with a Service and reach it by DNS.
- Expose the app externally with a real Route, reachable outside the session.
- Surface the running app as a new in-session dashboard tab.
- State that a Route requires a PROD-type namespace.

DCS networking is covered in the
[{{< param product_short >}} networking concepts]({{< param dcs_docs_base_url >}}/concepts/networking).

## Prerequisites

- **A02 — Deploy Your First App.** You know Deployments, Pods, and labels/selectors.

## Your Environment

A browser-based session with a split **terminal** and an **editor**. Your session
namespace is a **PROD-type** namespace for this lab — which, as you'll see, is what lets
you create a Route.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate
