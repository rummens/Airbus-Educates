---
title: Request a Volume
---

Persistent storage starts with a **claim**: you describe the storage you want, and the
platform provisions a real volume to match. Open the manifest:

```editor:open-file
file: ~/exercises/pvc.yaml
```

It's a [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
named `hello-dcs-data` asking for **1Gi**, with two fields worth pausing on:

- `accessModes: [ReadWriteOnce]` — **RWO**: a single node mounts this volume read-write at a
  time (single-writer). That's the right default for one app pod. The alternative,
  **ReadWriteMany** (RWX), lets many pods share one volume read-write — you'd choose it only
  when several pods genuinely need the same files. See
  [access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).
- `storageClassName: ${DCS_STORAGE_CLASS}` — **which** {{< param product_short >}} storage
  class provisions the disk. It's a variable, not a hardcoded name, because
  {{< param product_short >}} may rename or re-tier its classes — and because the *right* class
  is a governance decision, not a free choice (more below).

## Apply the claim

`envsubst` fills in the storage-class name from the environment before `oc` sees it:

```terminal:execute
command: envsubst < pvc.yaml | oc apply -f -
```

Expected output:

```
persistentvolumeclaim/hello-dcs-data created
```

{{< note >}}
The StorageClass provisions a real disk and binds it to your claim — this can take a few
seconds. "Done" is the PVC reaching **Bound**.
{{< /note >}}

Watch it bind:

```terminal:execute
command: oc get pvc hello-dcs-data -w --request-timeout=60s
```

Once it shows `Bound`, press `Ctrl+C` to stop watching. A **Bound** PVC means a real
PersistentVolume now backs your claim and is ready to mount.

```examiner:execute-test
name: verify-pvc-bound
title: The PVC is Bound
args:
- hello-dcs-data
timeout: 120
retries: .INF
delay: 3
```

## Which class, and why it's not your call alone

On {{< param product_short >}}, picking a storage class isn't only about performance or
File-vs-Block — it's a **compliance** decision. As a multi-national platform,
{{< param product_short >}} ties storage to **data classification** and residency: data of a
given classification may only live on an approved class. Pick the wrong one and you're not
just slower, you may be **out of compliance**. When you provision real storage, check your
data's classification against the approved classes — see the
[{{< param product_short >}} storage documentation]({{< param dcs_docs_base_url >}}/concepts/storage).
That's exactly why the class name is a variable here, not baked into the manifest.
