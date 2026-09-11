---
title: "Stateful Workloads"
---

A [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)'s
replicas are **interchangeable**. Any Pod can serve any request, and a replacement Pod is as
good as the one it replaced.

Plenty of workloads are not like that. A database replica, a queue broker, a cache with its
own data on disk — each needs the **same name** and the **same volume** back after a restart.

That is what a
[**StatefulSet**](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) is for, and this
lab builds one on **{{< param product_name >}}**.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Say when a workload needs a StatefulSet instead of a Deployment.
- Explain the three guarantees a StatefulSet adds: **stable identity**, **stable storage**,
  **ordered lifecycle**.
- Use `volumeClaimTemplates` to give every replica its **own** PersistentVolumeClaim.
- Address one specific replica by its per-Pod DNS name.
- Prove that a deleted Pod comes back with the same name **and** the same data.
- Say what scaling down leaves behind, and why that is deliberate.

## Prerequisites

- The Core lab **Store Data** — you have created a PersistentVolumeClaim and mounted it once.
- **Services & Cluster Networking** — a StatefulSet needs the **headless** Service you met
  there.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You create the Service, the StatefulSet
and the volumes here, in your own namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

Volumes come from the cluster's **default storage class**, so the manifests stay portable. On
{{< param product_short >}} you would name the class the data's
[classification]({{< param dcs_docs_base_url >}}/concepts/storage) requires.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) — the guarantees, and the limitations.
- [StatefulSet Basics](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/) — the upstream walkthrough this lab compresses.
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) — claims, classes and binding.
