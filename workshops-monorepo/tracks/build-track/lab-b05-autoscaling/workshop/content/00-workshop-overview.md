---
title: "Autoscaling"
---

Setting the replica count by hand works only while somebody is watching.

A [**HorizontalPodAutoscaler**](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
(HPA) takes that decision over: it reads how hard your Pods are working, compares it with
the `requests` you gave them, and changes the replica count to hold a target.

In this lab you hand the replica count to an HPA on **{{< param product_name >}}**, drive
the app under load from your own terminal, and watch it react.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain how an HPA turns CPU metrics plus your **CPU requests** into a replica count.
- Create an HPA with `autoscaling/v2` and read its status.
- Drive an app under load and watch it **scale out**.
- Explain why scale-**in** is deliberately slow, and what a stabilisation window is.
- Say what happens when the **namespace budget**, not the load, is the real ceiling.
- Say what **VPA** does differently, and why you do not point both at CPU.

## Prerequisites

- **Health & Resources** — this lab builds directly on the `requests` you set there. An HPA
  on CPU cannot work without them.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You deploy the app here, in your own
namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace, which carries a **`medium`** budget. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) — the controller, the algorithm and the stabilisation windows.
- [Automatically scaling pods with the HPA](https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-autoscaling.html) — the OpenShift view, including `oc autoscale`.
- [Vertical Pod Autoscaler](https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-vertical-autoscaler.html) — the other autoscaler, for `requests` rather than replicas.
