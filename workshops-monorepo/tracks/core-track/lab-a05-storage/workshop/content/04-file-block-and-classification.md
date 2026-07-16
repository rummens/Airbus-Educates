---
title: File, Block & Classification
---

You used a File volume. {{< param product_short >}} offers more than one kind, and picking
the right one is part performance, part **compliance**.

## File vs Block

The difference is mostly the [**access mode**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes):

| | **File** (`{{< param dcs_sc_file >}}`) | **Block** (`{{< param dcs_sc_block >}}`) |
|---|---|---|
| Access mode | ReadWriteMany (RWX) | ReadWriteOnce (RWO) |
| Shared? | Many Pods/nodes at once | One writer at a time |
| Good for | Shared files, content, uploads | Databases, single-writer, low latency |

{{< note >}}
A single RWO Block volume **won't** fan out across many replicas — only one Pod can mount
it read-write. Multi-replica stateful apps use an operator that gives each replica its own
volume (a Developer/Module F topic), not one shared Block PVC.
{{< /note >}}

## Classification drives the choice

On a multi-national platform, **data and security classification** can *mandate* a
particular storage class — where and how data is stored may be a legal requirement (e.g.
DE vs ES residency). Picking the wrong class isn't just slow, it can be a **compliance
breach**. So on {{< param product_short >}}, the storage class you name is a governance
decision, not only a technical one. See the
[{{< param product_short >}} storage concepts]({{< param dcs_docs_base_url >}}/concepts/storage).

## What about object storage (S3)?

Object (S3-style) storage is **not** a self-service PVC. You request an S3 bucket via an
**ITSM ticket** to the storage team, and consume it over the S3 API from your app — there
is no `storageClassName` for it. So: **File and Block via a PVC; S3 via a ticket.** Don't
go hunting for an S3 storage class — there isn't one.
