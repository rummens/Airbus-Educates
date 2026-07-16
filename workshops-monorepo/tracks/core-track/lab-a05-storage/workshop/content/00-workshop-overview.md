---
title: Workshop Overview
---

Restart your app and everything it wrote is **gone**. That's by design — a container's
filesystem is temporary, and A03 showed you Pods get replaced all the time. For anything
worth keeping, you need storage that lives *outside* the Pod. This workshop on
**{{< param product_name >}}** gives your app exactly that, and proves it survives a
restart.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the [PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) → [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) → PV model and dynamic provisioning.
- Request a volume with a PVC and mount it into the app.
- Prove data persists across a Pod restart.
- Distinguish **File** (RWX) from **Block** (RWO) storage and when to use each.
- State that classification drives storage-class choice, and that S3 comes via an ITSM ticket.

DCS storage is covered in the
[{{< param product_short >}} storage concepts]({{< param dcs_docs_base_url >}}/concepts/storage).

## Prerequisites

- **A02 — Deploy Your First App.** You know Deployments and restarts (A03 helps).

## Your Environment

A browser-based session with a split **terminal** and an **editor**. The PVC and volume
manifests are in `~/exercises`.

## Time and Difficulty

- **Estimated time:** 30 minutes
- **Difficulty:** Intermediate
