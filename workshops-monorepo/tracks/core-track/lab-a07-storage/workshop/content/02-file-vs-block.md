---
title: File vs Block Storage
---

{{< param product_short >}} offers two kinds of storage through a PVC — **File** and
**Block** — and picking the right one matters. The difference comes down to **access modes**:
how many workloads, on how many nodes, can use the volume at once.

## Access modes

A PVC declares an
[access mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).
The two that matter here:

- **ReadWriteMany (RWX)** — many Pods, on many nodes, can mount the volume read-write **at the
  same time**. This is **File** storage (a shared filesystem).
- **ReadWriteOnce (RWO)** — the volume is mounted read-write by **one node** at a time (a
  single writer). This is **Block** storage.

## When to use which

| | **File** (RWX) | **Block** (RWO) |
|---|---|---|
| Access | shared across pods/nodes | single-writer, one node |
| Typical use | shared uploads, content many replicas read/write | a database's data dir, a single-owner volume |
| Performance | good for sharing | lower latency for one writer |

Rule of thumb: if **several Pods must write the same files at once**, you need **File** (RWX).
If a **single workload owns its data** — most databases — **Block** (RWO) is the better,
lower-latency fit. Choosing RWO for something that needs sharing (or vice versa) leads to Pods
that won't schedule or apps that can't see each other's data.

In the exercise files you have both: `pvc-file.yaml` requests RWX against the File class, and
`pvc-block.yaml` requests RWO against the Block class. The next page mounts the File one; the
challenge uses the Block one.

{{< note >}}
Access mode and storage class must be compatible: a File class supports RWX; a Block class
supports RWO. Requesting RWX from a Block class leaves the PVC **Pending** — the provisioner
can't satisfy it.
{{< /note >}}
