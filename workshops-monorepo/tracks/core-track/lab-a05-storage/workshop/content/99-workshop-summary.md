---
title: Summary & Challenge
---

Your app can now remember things. You claimed a volume, mounted it, wrote to it, and proved
the data survived a Pod restart — the last piece of the {{< param product_name >}} Core
happy path.

## What You Did

- Learned the **PVC → StorageClass → PV** model and dynamic provisioning.
- Claimed a **File** PVC and mounted it at `/opt/app-root/src/data`.
- Wrote a marker, restarted the Pod, and **read it back** — persistence proven.
- Compared **File (RWX)** vs **Block (RWO)** and saw that **classification** drives the choice.
- Learned that **S3** comes via an **ITSM ticket**, not a PVC.

## Challenge — claim a Block volume

You've done File. Now claim a **Block** (ReadWriteOnce) volume and confirm it binds.

```terminal:execute
command: oc apply -f pvc-block.yaml && oc get pvc hello-dcs-block
```

```examiner:execute-test
name: verify-block-bound
title: Verify the Block PVC is Bound
timeout: 20
retries: .INF
delay: 2
```

{{< note >}}
**Hint:** `pvc-block.yaml` is already in `~/exercises` — open it to see the `ReadWriteOnce`
access mode that makes it Block rather than File. Depending on the storage class, the claim
either binds right away or shows **Pending until a Pod mounts it** (a "wait for first
consumer" policy) — both mean it was accepted correctly.
{{< /note >}}

## Check Your Understanding

1. What does a **StorageClass** do?

{{< note >}}
**Answer:** It defines a kind of storage the platform offers and the provisioner that
creates volumes for it. A PVC that names (or defaults to) a class gets a matching PV
provisioned dynamically.
{{< /note >}}

2. **File** vs **Block** — what's the key difference?

{{< note >}}
**Answer:** Access mode. File is ReadWriteMany (many Pods can mount it at once); Block is
ReadWriteOnce (a single writer, lower latency). File for shared data, Block for things like
a single database.
{{< /note >}}

3. What **proved** the data persisted?

{{< note >}}
**Answer:** After deleting and recreating the Pod, the marker file was still readable with
its original value — because it lives on the PV, which is independent of the Pod.
{{< /note >}}

4. How do you get **S3 object storage** on {{< param product_short >}}?

{{< note >}}
**Answer:** Via an **ITSM ticket** to the storage team — it's not a self-service PVC and
has no storage class. File and Block are PVCs; S3 is a request.
{{< /note >}}

## Next Steps

That's the Core happy path complete: **what DCS is → deploy → configure & fix → expose →
persist**. Next come the orientation labs — **A06** (the terms: namespaces & tenancy),
**A07** (the ITSM self-service console), **A08** (the OpenShift web console) — and then the
**Developer track** for the mechanisms behind everything you just did.
