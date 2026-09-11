---
title: "Services & Cluster Networking"
---

"Just expose it" hides at least five different answers.

A [**Service**](https://kubernetes.io/docs/concepts/services-networking/service/) is not one
thing: the `type` field changes what gets created, what lands in DNS, and whether anything
outside the cluster can reach it at all.

This lab walks the types a tenant can actually use on **{{< param product_name >}}**, and the
two that look right and are not.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Name the Service types and say what each one is **for**.
- Resolve a Service through [cluster DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) and explain what came back.
- Explain the difference between a **ClusterIP** and a **headless** Service, by their DNS answers.
- Use an **ExternalName** Service as a stable in-cluster name for something that lives elsewhere.
- Say why **NodePort** and **LoadBalancer** are the wrong tools on {{< param product_short >}}, and what you use instead.

## Prerequisites

- The Core lab **Expose Your App** — you have created a Service and a Route once.
- Helpful: **Health & Resources**, for readiness probes, since endpoints follow readiness.

This lab is the depth behind Core's happy path: there you exposed an app, here you find out
what the alternatives were and why the platform chose for you.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You deploy the app here, in your own
namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Service](https://kubernetes.io/docs/concepts/services-networking/service/) — the types, selectors and ports.
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) — the names this lab resolves by hand.
- [Configuring Routes](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) — the OpenShift object that replaces a LoadBalancer Service here.
