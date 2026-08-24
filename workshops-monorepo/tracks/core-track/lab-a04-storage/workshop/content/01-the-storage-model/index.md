---
title: The Storage Model
---

You do not attach a disk to an app directly on {{< param product_short >}}. You request
storage, and the platform provisions it. Three objects make that work:

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/storage-model
```

![How your app gets storage on DCS](storage-model.svg)

- A [**PersistentVolumeClaim (PVC)**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) —
  your request: "I want this much space, this type." You write this.
- A [**StorageClass**](https://kubernetes.io/docs/concepts/storage/storage-classes/) —
  the platform's offering (File, Block, different tiers). DCS provides these.
- A [**PersistentVolume (PV)**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes) —
  the real volume DCS provisions and **binds** to your claim.

This is **dynamic provisioning**: you never pre-create the disk, you just claim one and DCS
creates and binds a matching PV automatically.

{{< note >}}
**💡 If you have run VMs:** a PVC is like ordering a disk from the platform catalog — you state the
size and type, and the platform attaches a provisioned volume. You don't format a physical
disk yourself.
{{< /note >}}

## See what DCS offers

List the storage classes available to you:

```terminal:execute
command: oc get storageclass | tee ~/exercises/storageclasses.txt
```

```examiner:execute-test
name: verify-storageclass
title: 🔍 Verify storage classes are available
timeout: 10
```

Each row is a kind of storage you can request. On {{< param product_short >}} you'll see
**File** and **Block** classes — more on choosing between them shortly.
