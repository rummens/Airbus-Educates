<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Storage

A container's own filesystem is temporary — replace the Pod and everything it wrote is gone. This lab gives your app storage that lives outside the Pod and survives a restart.

**In this lab:** the PVC → StorageClass → PV model · prove the container filesystem is ephemeral · claim and mount a volume · prove data persists · File vs Block · how S3 is requested.

Digital Container Service · DCS Academy

---

<!-- id: storage-model -->
## The Storage Model

You do not attach a disk to an app directly on DCS. You request storage, and the platform provisions it. Three objects make that work.

- **PVC** — your request: how much space, which type. You write this.
- **StorageClass** — the kind of storage DCS offers (File, Block, tiers). The platform provides these.
- **PV** — the real volume DCS creates and **binds** to your claim.
- **Dynamic provisioning**: you never pre-create the disk; you claim one and DCS creates and binds a matching PV.

```
oc get storageclass
```

![How your app gets storage on DCS](storage-model.svg)

---

<!-- id: ephemeral -->
## Ephemeral by Default

A container's own filesystem is **ephemeral** — it exists only while the Pod exists. Anything written inside a running container is lost when that container is replaced.

- Deploy the app with no volume attached.
- Write a file inside the container, then delete the Pod.
- The Deployment starts a fresh Pod from the clean image.
- The file is gone — that is the default: no Pod, no data.

```
oc create deployment hello-dcs --image="$DCS_REGISTRY/samples/hello-dcs:v1.0.0"
oc exec deploy/hello-dcs -- sh -c 'echo written-inside-the-container > /opt/app-root/src/note'
oc delete pod -l app=hello-dcs
```

Reading the note back on the new Pod fails — the file did not survive.

---

<!-- id: request-mount -->
## Request and Mount

Give the app a volume that keeps its data. Claim it with a PVC, then mount it into the Pod at a path the non-root app can write to.

- The PVC asks for 1Gi of **File** (ReadWriteMany) storage.
- Many storage classes only **bind** once a workload uses the claim (wait-for-first-consumer).
- Mount inside the image's writable home (`/opt/app-root/src/data`), not a root-owned path like `/data`.
- Write a marker onto the volume — this goes on the PV, not the container.

```
oc apply -f pvc-file.yaml
envsubst < hello-dcs-with-volume.yaml | oc apply -f -
oc exec deploy/hello-dcs -- sh -c 'echo persisted-marker-42 > /opt/app-root/src/data/marker'
```

The PVC becomes `Bound` once the Pod is scheduled.

---

<!-- id: persists -->
## Prove It Persists

The key test: destroy the Pod, let DCS create a fresh one, and read the marker back. It survives because it lives on the PV, not on the container.

- `rollout restart` retires the old Pod and starts a new one.
- The new Pod is built from the clean image again.
- The marker is still readable — same value, new Pod.
- The container was replaced; the volume and its data persisted.

```
oc rollout restart deploy/hello-dcs
oc exec deploy/hello-dcs -- cat /opt/app-root/src/data/marker
```

Expected: `persisted-marker-42` — that is persistent storage.

---

<!-- id: file-block -->
## File, Block & Classification

DCS offers more than one kind of storage. Choosing is part performance, part compliance.

- **File** (`dcs-file-rwx`) — ReadWriteMany: many Pods at once. Shared files, content, uploads.
- **Block** (`dcs-block-rwo`) — ReadWriteOnce: one writer, lower latency. Databases, single-writer.
- **Classification** can mandate a class — restricted material may require physically separated disks. Picking wrong can be a compliance breach.
- **S3 object storage** is available, but by **ITSM ticket** to the storage team, not a self-service PVC.

```
oc apply -f pvc-block.yaml
oc get pvc hello-dcs-block
```

A Block PVC either binds immediately or stays `Pending` until a Pod mounts it — both are correct.

---

<!-- id: close -->
## What's Next

You gave an app storage that survives a Pod restart — the last step of the Core basics.

- You learned the **PVC → StorageClass → PV** model and dynamic provisioning.
- You claimed a File PVC, mounted it, wrote a marker, and read it back after a restart.
- You compared **File (RWX)** and **Block (RWO)**, and saw **classification** drive the choice.

Next: the orientation labs (namespaces & tenancy, the ITSM console, the OpenShift web console), then the Developer track for the mechanisms behind everything you just did.
