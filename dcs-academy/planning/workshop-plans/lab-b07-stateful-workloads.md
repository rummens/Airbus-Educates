# Workshop Plan: lab-b07-stateful-workloads

## 1. Workshop Metadata

- **Name:** `lab-b07-stateful-workloads`
- **Title:** Stateful Workloads
- **Description:** Build a StatefulSet with a volume per replica — stable names, per-Pod DNS, ordered rollout — then prove identity and data survive a Pod deletion, and see what scaling down leaves behind.
- **Duration:** 25m
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `70`
- **Prerequisites (curricular only):** Core *Store Data* (a PVC mounted once); **Services & Cluster Networking** (b06 — the headless Service a StatefulSet requires)
- **Status:** New lab, written 2026-09-11.

## 2. Workshop Configuration

Terminal `split`, editor, slides, examiner. Budget `medium` (two 1Gi claims plus one more on scale-up). **vcluster `false`** — real claims from the cluster's storage class and real per-Pod DNS both belong in the session namespace. Self-contained: the learner creates the Service, the StatefulSet and the volumes.

## 3. Learning Objectives

- Say when a workload needs a StatefulSet rather than a Deployment.
- Explain the three guarantees: **stable identity**, **stable storage**, **ordered lifecycle**.
- Use `volumeClaimTemplates` to give every replica its own claim.
- Address one specific replica by its per-Pod DNS name.
- Predict what a Pod deletion, a scale-up and a scale-down each leave behind.

## 4. Connection to the rest of the course

**Builds on b06:** the headless Service is the prerequisite, and the per-Pod DNS record is the same mechanism seen from the other end — b06 showed one record per Pod, here those records get *stable names*.

**Builds on Core Store Data:** the PVC and the non-root mount path (`/opt/app-root/src/data` plus `fsGroup: 1001`) are the pattern Core proved; this lab multiplies it per replica.

**Deliberately not here:** databases (an operator's job — the Operators track), backup and restore, storage classes by data classification (Core covers the concept; the class name is a platform value).

## 5. Exercise Files

- `service-headless.yaml` — `clusterIP: None`, named by `spec.serviceName`.
- `statefulset.yaml` — 2 replicas, `volumeClaimTemplates` (1Gi, RWO, **no `storageClassName`** so the default class provisions and the manifest stays portable), `fsGroup: 1001`, mount inside the image's writable home, readiness on `/healthz`.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — interchangeable vs identity, objectives, both prerequisites.
- **`01-why-statefulset/`** — what a Deployment gives, what a StatefulSet adds, why ordering is a real guarantee rather than pedantry, and the warning that a StatefulSet is not a database. **SVG** `statefulset-vs-deployment.svg`.
- **`02-build-one.md`** — headless Service, then the StatefulSet applied while watching the lower pane: ordinal names, and the ordering visible as *what you do not see*. Then one bound claim per replica, with the `<template>-<statefulset>-<ordinal>` naming explained.
- **`03-identity-and-data.md`** — resolve one replica's own DNS name; write the Pod's own `$HOSTNAME` into its own volume and read both back. The two different answers are the proof the volumes are not shared.
- **`04-survive-a-restart.md`** — record the UID, delete `hello-dcs-0`, watch the **same name** come back as a **new Pod**, and find the marker still there. The claim belongs to the ordinal.
- **`05-scale-and-leftovers.md`** — scale to 3 (new Pod, new claim), scale to 2 (highest ordinal removed, **claim kept**), why that default is right, and the quota warning that follows from it.
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, 4-question knowledge check.

## 7. Examiner Coverage (10 checks, one per command)

`verify-headless-service` · `verify-statefulset-ready` · `verify-pvc-per-replica` · `verify-pod-dns-identity` · `verify-marker-per-replica` · `verify-identity-after-restart` · `verify-data-after-restart` · `verify-scaled-up-with-pvc` · `verify-pvc-kept-after-scaledown` · `verify-storage-quota-read`

Three are doing more than they look:

- **`verify-marker-per-replica`** is what proves the volumes are **separate** — if the replicas shared one, both would report the same owner and the check fails.
- **`verify-pod-dns-identity`** compares each per-Pod DNS answer against that Pod's own `status.podIP`, so a record pointing at a sibling or at a Service IP cannot pass.
- **`verify-pvc-kept-after-scaledown`** asserts a **survival**. A cluster configured with a `persistentVolumeClaimRetentionPolicy` that deletes claims makes it fail loudly — correct, because the page's claim would not hold there.

## 8. Environment notes

- The test cluster's default class is `WaitForFirstConsumer`, so a claim stays `Pending` until its Pod is scheduled; every PVC check polls rather than reading once.
- The smoke plan deliberately does **not** patch `imagePullPolicy`: editing a StatefulSet's Pod template triggers an ordered rollout in the middle of the lab.
- `fsGroup: 1001` is the pattern Core's storage lab proved on this platform; without it the marker write fails with `Permission denied` on a freshly provisioned volume.

## 9. Design Notes

- The lab's spine is **three proofs, not three descriptions**: separate volumes (different markers), real identity (same name, new UID), and the surviving claim (Pod gone, claim `Bound`).
- Scale-down's leftover claim is framed as a **feature with a cost** — it is the right default *and* the quiet way a storage quota fills up. Both halves are said out loud.
