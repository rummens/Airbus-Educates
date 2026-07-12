---
title: Workshop Overview
---

Welcome back. In this workshop, part of **{{< param product_name >}}**, you'll give a
workload **persistent storage** — storage that outlives the container it's attached to —
using a PersistentVolumeClaim, and see how {{< param product_short >}} turns that request
into a real disk.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

In A02 you deployed the stateless `hello-dcs` app. If a pod restarted, anything written
inside the container was gone — a container's filesystem is **ephemeral**. Most real
applications need data to survive restarts: uploads, a database's files, a cache. That's
what a **volume** backed by persistent storage gives you, and it's what you'll add here.

We don't just run commands — for each concept you'll learn *what* it is, *why* it exists,
and *how* the pieces fit together.

## What You'll Learn

By the end you will be able to:

- Explain the **PVC → StorageClass → PV** model and how {{< param product_short >}} provisions storage dynamically.
- Distinguish [**File**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) storage (RWX, shared) from **Block** storage (RWO, single-writer), and choose the right one.
- Request a volume with a [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and mount it into a workload.
- Prove that data **survives a pod restart**.
- Explain how **data classification** drives storage-class choice on {{< param product_short >}}, and how **object (S3) storage** is obtained.

## Prerequisites

- **lab-a02-kubernetes-essentials** — you should be comfortable creating a
  [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and
  running `oc` commands against your project.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} project. The sample application image is served from the
{{< param product_short >}} Harbor registry. Commands are run with `oc` in the terminal.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Beginner

## Further Reading

- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
