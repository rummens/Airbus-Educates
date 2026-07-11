# Workshop Plan: lab-a07-storage

## 1. Workshop Metadata

- **Name:** `lab-a07-storage`
- **Title:** Storage on DCS
- **Description:** Request persistent storage on DCS with a PVC, understand File vs Block storage classes, and see how data classification drives storage-class choice.
- **Duration:** 40m
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A02 (Kubernetes Essentials on DCS)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (view PVC/PV binding visually)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Sample image: reuse `{{< param dcs_registry >}}/samples/hello-dcs:1.0`
- **Storage-class params (new):** storage-class names must be **variables**, not literals, for easier maintenance — add `dcs_sc_file` and `dcs_sc_block` to the param set (placeholders until confirmed). All exercise manifests reference `{{< param dcs_sc_file >}}` / `{{< param dcs_sc_block >}}`.

## 3. Learning Objectives

- Explain the **PVC → StorageClass → PV** model: a PersistentVolumeClaim requests storage; a StorageClass provisions it dynamically.
- Distinguish the two DCS-offered access types delivered via PVC: **File** storage (RWX-capable, shared) and **Block** storage (RWO, single-node) — and when to pick each.
- Request a volume with a PVC using a DCS storage class and mount it into a workload.
- Verify data **persists across a pod restart**.
- Explain that the right storage class depends on **data and security classification** (multi-national residency) — different classifications may require different SCs.
- Know that **object (S3) storage** is available on DCS **via an ITSM ticket to the storage team** (not self-service PVC).

## 4. Connection to Previous Workshop

A02 deployed a stateless `hello-dcs` workload; a pod restart lost anything written inside the container. This workshop adds **persistence**: attach a PVC so data survives restarts. Reuses the same sample app — do not re-teach Deployment mechanics; focus on the storage objects.

*(This is the Foundations storage **concept** lab. The Developer track's `lab-b05-stateful-storage` is the hands-on stateful-workload deep dive and assumes this.)*

## 5. Exercise Files to Create

- `exercises/pvc-file.yaml` — a PVC using `{{< param dcs_sc_file >}}` (File storage, RWX).
- `exercises/pvc-block.yaml` — a PVC using `{{< param dcs_sc_block >}}` (Block storage, RWO).
- `exercises/hello-dcs-with-volume.yaml` — the A02 Deployment+Service with a volume mount backed by the PVC.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **storage** blurb + link `{{< param dcs_docs_base_url >}}/concepts/storage`.
- **`01-storage-model.md`** — concept. The **PVC → StorageClass → PV** chain and dynamic provisioning; why apps request storage declaratively rather than mounting host paths. Analogy (tapering): a PVC is like ordering a disk from the platform's catalog — you state size/type, DCS provisions it. Inline blurb + DCS docs; [PersistentVolumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/) upstream.
  - `oc get storageclass` → check: DCS storage classes listed (the File and Block SCs). **SVG diagram** of the PVC→SC→PV relationship (structural concept → page bundle).
- **`02-file-vs-block.md`** — concept. **File** (RWX, shareable across pods/nodes) vs **Block** (RWO, single-writer, lower-latency); when each fits. Reference the SC names via variables. Access modes → [upstream](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).
- **`03-request-and-mount.md`**
  - `editor:open-file` pvc-file.yaml; `oc apply -f pvc-file.yaml` → polling check: PVC **Bound**.
  - `oc apply -f hello-dcs-with-volume.yaml` (mounts the PVC) → polling check: workload ready with the volume mounted.
  - Write a file into the mounted volume (`oc exec ... -- sh -c 'echo ... > /data/marker'`) → check: file present.
- **`04-persistence-and-classification.md`**
  - Restart the pod (`oc delete pod` / rollout restart) → polling check: new pod ready.
  - Read the marker back from the volume → check asserts the data **survived** (the persistence proof point).
  - Concept: **data & security classification drives SC choice** — multi-national residency (e.g. DE/ES) and classification may mandate a specific storage class; picking the wrong SC is a compliance issue, not just a performance one. Inline blurb + DCS docs (data classification). Ties to Security track (C — governance/residency).
  - Concept: **object (S3) storage** is provisioned **via an ITSM ticket to the storage team**, not a PVC — model the request, no live provisioning. DCS docs link.
- **`99-workshop-summary.md`** — recap PVC/SC/PV, File vs Block, persistence, classification-driven choice, S3-via-ticket. **Challenge**: request a Block PVC (`pvc-block.yaml`) and attach it, examiner-validated + hint + reveal. **Check Your Understanding** (3 Q): what a StorageClass does; File vs Block access modes; how you get S3 on DCS.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`; manifests referenced by relative name. Commands scoped to the session namespace. Track that the marker file lives in the mounted volume path (`/data`), not the container filesystem — that's the whole point.

## 8. Design Notes

- **SC names are variables (`dcs_sc_file`, `dcs_sc_block`)** — never hardcode storage-class names; DCS may rename or re-tier them. Placeholders until confirmed with the storage team (P2 in tasks.md).
- DCS offers **File and Block via PVC** (self-service) and **S3 via ITSM ticket** (not self-service) — keep that distinction crisp so learners don't look for an S3 storage class.
- **Classification-driven SC selection** is the DCS-specific hook; keep it conceptual in Foundations, deepen in the Security/Architect tracks (residency, data classification matrix).
- Reuses the A02 sample app + `hello-dcs` image — no new images.
- Overlaps deliberately with Developer B05 (stateful workloads): A07 = concept + persistence proof (everyone); B05 = real stateful app pattern (Developer track). Cross-reference both ways.
