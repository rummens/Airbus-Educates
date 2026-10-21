---
title: File, Block & Classification
---

You used a File volume. {{< param product_short >}} offers more than one kind, and picking
the right one is part performance, part **compliance**.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/file-block
```

## File vs Block

The difference is mostly the [**access mode**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes):

| | **File** (`{{< param dcs_sc_file >}}`) | **Block** (`{{< param dcs_sc_block >}}`) |
|---|---|---|
| Access mode | ReadWriteMany (RWX) | ReadWriteOnce (RWO) |
| Shared? | Many Pods/nodes at once | One writer at a time |
| Good for | Shared files, content, uploads | Databases, single-writer, low latency |

{{< note >}}
**⚠️ Watch out:** a single RWO Block volume **will not** fan out across many replicas — only one Pod can mount
it read-write. Multi-replica stateful apps use an operator that gives each replica its own
volume (covered in the **Stateful Workloads** lab), not one shared Block PVC.
{{< /note >}}

## Classification drives the choice

On a multi-national platform, **data and security classification** can *mandate* a
particular storage class.

The deciding factor is the **classification level**, not the country. Some data — for
example **NATO** or otherwise international-restricted material — must sit on **physically
separated** disks, kept apart from national data. That means its own dedicated
**StorageClass**.

Picking the wrong class can be a **compliance breach**.

So on {{< param product_short >}}, choosing a storage class is also a **governance**
decision. See the
[{{< param product_short >}} storage concepts]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/kubernetes-storage).

## What about object storage (S3)?

Object (S3-style) storage **is** available on {{< param product_short >}}, but it is not
self-service. Instead of naming a `storageClassName`, you request a bucket through an
**ITSM ticket** to the storage team, then use it over the S3 API from your app. File and
Block come through a PVC; S3 comes by request. If your app needs object storage, plan for
that request instead of looking for a storage class.
