---
title: "Services & Cluster Networking"
---

Kubernetes has five Service types. The `type` field on a
[**Service**](https://kubernetes.io/docs/concepts/services-networking/service/) changes what
gets created, what lands in DNS, and whether anything outside the cluster can reach it.

This lab covers the types a tenant can use on **{{< param product_name >}}**, and the two
that exist in the API but do not work here.

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

- The Core lab **Expose Your App**, so you have created a Service and a Route once.
- Helpful: **Health & Resources**, for readiness probes, since endpoints follow readiness.

Core exposed an app by the shortest path. This lab covers the alternatives, and why the
platform picked that one for you.

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
- [Configuring Routes](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/ingress_and_load_balancing/routes) — the OpenShift object that replaces a LoadBalancer Service here.
