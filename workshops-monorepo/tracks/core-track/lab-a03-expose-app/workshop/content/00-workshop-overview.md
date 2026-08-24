---
title: "Expose Your App"
---

So far your app has only been reachable through a **local tunnel** — a `port-forward` that
runs only while a single terminal command is open.

That works for a quick test, but not for anything real.

In this workshop on **{{< param product_name >}}** you give the app a proper address:

1. a stable **in-cluster** name;
2. a real **external** URL that anyone can reach.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the {{< param product_short >}} traffic chain: [Service](https://kubernetes.io/docs/concepts/services-networking/service/) → [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) (OpenShift docs) → external load balancer, with managed DNS.
- Give the app a stable in-cluster address with a Service and reach it by DNS.
- Expose the app externally with a real Route, reachable outside the session.
- Surface the running app as a new in-session dashboard tab.
- State that a Route requires a PROD-type namespace.

DCS networking is covered in the
[{{< param product_short >}} networking concepts]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/openshift-networking).

## Prerequisites

- **Deploy Your First App.** You know Deployments, Pods, and labels/selectors.

## Your Environment

A browser-based session with a split **terminal** and an **editor**. Your session
namespace is a **PROD-type** namespace for this lab — which, as you'll see, is what lets
you create a Route.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Beginner
