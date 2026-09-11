---
title: "Health & Resources"
---

An app running as **one replica**, with no probes and no resource numbers, is a demo.

It has no redundancy, it cannot tell the platform whether it is actually working, and it
quietly draws whatever default share of the namespace budget it is given.

This lab fixes all three on **{{< param product_name >}}**, in the order the problems
actually bite: scale it, hit the budget, right-size it, then make it prove its own health.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Scale a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and reason about replica count against a namespace budget.
- Read a [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) to tell whether a rollout has room to land.
- Diagnose a quota rejection from cluster events, and fix it by right-sizing [requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
- Explain what a **readiness** probe protects and what a **liveness** probe protects, and configure both.
- Delete a Pod and explain what brings a replacement back.

## Prerequisites

- The Core labs **Deploy Your First App** and **Configure & Troubleshoot Your App** — you
  know `oc scale`, the Deployment → ReplicaSet → Pod chain, and how to read
  `oc describe` / `oc get events` when something goes wrong.

This lab does not re-teach that mechanics. It puts it under a **real budget**, which is
where those numbers start to matter.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You deploy the app here, in your own
namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

Your namespace carries a **`medium`** resource budget — deliberately sized so you can hit
it on purpose before you learn to fit inside it.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Managing Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) — requests, limits, and how the scheduler and kubelet use them.
- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — the upstream how-to behind this lab's probes.
- [ResourceQuotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) — the object behind every "exceeded quota" event you will see today.
