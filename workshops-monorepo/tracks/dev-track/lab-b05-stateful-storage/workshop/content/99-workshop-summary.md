---
title: Summary
---

Your app can now keep its data on **{{< param product_name >}}**. You moved from an
ephemeral container filesystem to real persistent storage — and proved it survives.

## What You Did

- Explained why a container's own filesystem is **ephemeral**, and when that matters.
- Requested storage with a **PersistentVolumeClaim** and watched it reach **Bound**.
- Chose a **{{< param product_short >}} storage class** (`{{< param dcs_storage_class >}}`) and understood the RWO access mode.
- **Mounted** the volume into the app and wrote data to it.
- Deleted the Pod and proved the data was **still there** on the new Pod — persistence, demonstrated.

## Challenge

Now prove it yourself, unguided. Write a marker file into the mounted volume, restart the
Pod, and confirm the marker survives. When you think it's done, run the check.

```examiner:execute-test
name: verify-marker
title: Challenge — data survives a pod restart
timeout: 10
retries: 5
delay: 3
```

{{< note >}}
**Hint:** write into the mounted path with `oc exec`, then `oc delete pod -l app=hello-dcs`
and read the file back once the new Pod is Ready.
{{< /note >}}

## Check Your Understanding

1. What is the difference between a **PersistentVolumeClaim** and a **PersistentVolume**?

{{< note >}}
**Answer:** The PVC is your *request* for storage (size + access mode + class). The PV is
the actual piece of storage that satisfies it. On {{< param product_short >}} the storage
class provisions the PV dynamically when your PVC is created.
{{< /note >}}

2. Why did you set `storageClassName` from a **variable** rather than a fixed value?

{{< note >}}
**Answer:** Storage class names differ per cluster. Using `{{< param dcs_storage_class >}}`
lets the same workshop deploy anywhere without editing manifests — a house standard.
{{< /note >}}

3. Your PVC is **RWO** (ReadWriteOnce). What does that mean for scaling the app to many replicas?

{{< note >}}
**Answer:** RWO binds the volume to one node at a time, so multiple replicas can't all
mount it read-write. Genuinely scalable stateful apps use an operator (e.g. CloudNativePG
in the Operators module) that manages per-instance storage, not one shared RWO volume.
{{< /note >}}

4. What happened to the data when the Pod was deleted and recreated — and why?

{{< note >}}
**Answer:** It survived. The data lives on the PersistentVolume, not in the Pod. The new
Pod re-mounted the same PVC, so the files were still there.
{{< /note >}}

## Next Steps

That's the app-lifecycle arc of the Developer track — deploy, configure, scale, debug, and
persist. Next: **Cloud Development with OpenShift Dev Spaces** — develop *on*
{{< param product_short >}}, not just deploy to it. Or head to the **Operators** module to
own an operator-managed database instead of hand-rolling stateful storage.
