---
title: Workshop Overview
---

Welcome back. In this workshop, part of **{{< param product_name >}}**, you'll take the
stateless `hello-dcs` app you already know and give it **persistent storage** — storage
that outlives the container it's attached to — by requesting a PersistentVolumeClaim,
mounting it, and proving that data survives a pod restart.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

In B01 you deployed `hello-dcs`, and it's already running in your project now. But a pod is
**ephemeral**: anything written inside the container is gone the moment the pod is replaced —
and from A02 you know how readily that happens. Most real apps need data to survive: uploads,
a database's files, a queue. This is the *developer's* view of storage — wiring a volume into
**your own** app — building on A07, which introduced PVCs and DCS storage classes at the
platform level. We don't re-explain what a storage class is; we put one to work.

We don't just run commands — for each concept you'll learn *what* it is, *why* it exists,
and *how* the pieces fit together.

## What You'll Learn

By the end you will be able to:

- Request storage with a [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and choose an appropriate {{< param product_short >}} storage class.
- Mount a volume into your app and write to it.
- Explain [access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) (RWO vs RWX) and when each applies.
- Prove that data **survives a pod restart** — and reason about why a single volume doesn't fan out to many replicas.

## Prerequisites

- **lab-b01-deploy-your-first-app** — you should be comfortable creating and scaling a
  [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) with `oc`.
- **lab-a07-storage** (recommended) — the platform view of PVCs and {{< param product_short >}} storage classes.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} project, with `hello-dcs` already deployed. The sample
application image is served from the {{< param product_short >}} Harbor registry. Commands
are run with `oc` in the terminal.

Open the PVC manifest you'll start with:

```editor:open-file
file: ~/exercises/pvc.yaml
```

## Time and Difficulty

- **Estimated time:** 35 minutes
- **Difficulty:** Intermediate
