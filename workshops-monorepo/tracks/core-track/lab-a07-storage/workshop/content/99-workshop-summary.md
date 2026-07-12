---
title: Summary
---

You gave a workload real, persistent storage on **{{< param product_name >}}** — requested a
volume, mounted it, and proved the data outlives the Pod.

## What You Did

- Learned the **PVC → StorageClass → PV** model and dynamic provisioning.
- Distinguished **File** (RWX, shared) from **Block** (RWO, single-writer) storage and when to use each.
- Requested a PVC (with a variabilised storage-class name), mounted it, and wrote data to `/data`.
- Deleted the Pod and proved the data **survived** on the volume.
- Learned that **data classification** drives storage-class choice, and that **S3** comes via an ITSM request, not a PVC.

## Challenge

Do it yourself, unguided: **request a Block volume.** Apply `pvc-block.yaml` (it uses the
Block storage class, ReadWriteOnce) and get it to **Bound**. Run the check when ready.

```examiner:execute-test
name: verify-pvc-bound
title: Challenge — the Block PVC is Bound
args:
- hello-dcs-block
timeout: 120
retries: .INF
delay: 3
```

{{< note >}}
**Hint:** the manifest uses the `DCS_SC_BLOCK` variable, so apply it the same way you applied
the File PVC — through `envsubst`:
`envsubst < pvc-block.yaml | oc apply -f -`.
{{< /note >}}

## Check Your Understanding

1. What does a StorageClass do?

{{< note >}}
**Answer:** It's the provisioner — it knows how to create a real PersistentVolume to satisfy
a PVC. You name a StorageClass in your claim and the platform dynamically provisions matching
storage; you never pre-create disks.
{{< /note >}}

2. What's the difference between File and Block storage in access-mode terms?

{{< note >}}
**Answer:** File is **ReadWriteMany** (many pods/nodes mount it read-write at once — shared).
Block is **ReadWriteOnce** (a single node mounts it read-write — single-writer, e.g. a
database).
{{< /note >}}

3. How do you get S3 object storage on {{< param product_short >}}?

{{< note >}}
**Answer:** By raising an **ITSM request** to the storage team — there's no S3 storage class
to claim with a PVC. File and Block are self-service via PVC; S3 is provisioned by ticket.
{{< /note >}}

## Next Steps

You've completed the Foundations storage lab. The Developer track's **Stateful Workloads &
Storage** workshop builds on this with a real stateful application pattern.
