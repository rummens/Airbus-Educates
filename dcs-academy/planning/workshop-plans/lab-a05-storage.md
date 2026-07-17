# Workshop Plan: lab-a05-storage

> **RESOLVED (2026-07-16, built):** the author's storage demo (`Lightning Talk Demo_ OpenShift Storage 101 v2 .docx`) is a Flask **counter** web app on a PVC (`/mnt/data/counter.txt`), delete-pod → recount → persists, plus an optional "try to delete the PVC while a pod uses it (blocked)" step. Its Flask-in-a-ConfigMap app was **not** imported: it needs Flask (breaks air-gapped/no-new-image). Instead the demo's **arc** — PVC → mount → write → restart → read-back — was folded onto the existing air-gapped **hello-dcs** app using an `oc exec` marker file (`/data/marker`), which proves persistence identically without a new image. Built as `lab-a05-storage`; pages 02–03 are the demo slot. The docx "delete PVC while in use is blocked" step is a candidate future add-on.

## 1. Workshop Metadata

- **Name:** `lab-a05-storage`
- **Title:** Storage
- **Description:** Give your app storage that survives a restart — request a PVC from a DCS storage class, mount it, write data, restart, and prove the data persists — and learn when to pick File vs Block and how S3 is requested.
- **Duration:** 30m
- **Difficulty:** intermediate
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A02 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view/apply PVC + volume manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: **not** enabled — console tour is A08.
- Examiner: `enabled: true`
- Budget: `medium`
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs, pre-deployed via `session.objects`.
- **Storage-class params:** SC names must be **variables**, not literals — `dcs_sc_file` and `dcs_sc_block` added to the param set (placeholders until confirmed with the storage team). All manifests reference `{{< param dcs_sc_file >}}` / `{{< param dcs_sc_block >}}`.
- **vcluster decision:** `false` — plain session namespace; PVCs are namespace-scoped self-service, no cluster-scoped work.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:
- Explain the **PVC → StorageClass → PV** model and dynamic provisioning.
- Request a volume with a PVC using a DCS storage class and mount it into the app.
- Prove data **persists across a pod restart**.
- Distinguish DCS **File** (RWX, shared) vs **Block** (RWO, single-writer) storage and when to pick each.
- State that **data/security classification drives SC choice** (multi-national residency) and that **object (S3) storage comes via an ITSM ticket**, not a self-service PVC.

## 4. Connection to Previous Workshop

**Already known** (from A02–A04): the hello-dcs Deployment; rolling out / restarting pods (A03); applying declarative manifests (A03); that a restart replaces the pod — and, crucially, that anything written inside the container is lost when it does. That data-loss pain is the motivation this workshop resolves.

**What is new here:**
- **PersistentVolumeClaim (PVC)** — requesting storage declaratively.
- **StorageClass** — how DCS provisions the volume dynamically (File vs Block).
- Mounting a volume and proving persistence across a restart.
- Classification-driven SC selection and the S3-via-ITSM path.

**What should NOT be re-taught:** Deployment/rollout/restart mechanics (A02/A03 — reference them); how to apply a manifest (A03).

## 5. Exercise Files to Create

> These are the **default** exercise files; if the author's storage demo supersedes them, reconcile per the TODO above (keep the persistence proof point).

- `exercises/pvc-file.yaml` — PVC using `{{< param dcs_sc_file >}}` (File, RWX), small size within budget.
- `exercises/pvc-block.yaml` — PVC using `{{< param dcs_sc_block >}}` (Block, RWO) — the challenge PVC.
- `exercises/hello-dcs-with-volume.yaml` — the hello-dcs Deployment with the PVC mounted at a data path (e.g. `/data`).
- `exercises/README.md` — placeholder.

Note: if any manifest uses `${DCS_...}` substitution, apply with `envsubst < file.yaml | oc apply -f -`, never plain `oc apply` (carry-forward bug). Prefer ytt params for SC names.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note. Recap the A04 gap: "restart your app and anything it wrote is gone — let's fix that." Objectives; DCS-specific storage blurb + `{{< param dcs_docs_base_url >}}/concepts/storage`.
- **`01-the-storage-model.md`** — concept, folded: the **PVC → StorageClass → PV** chain and dynamic provisioning; why apps request storage declaratively instead of mounting host paths (analogy, tapering: "a PVC is like ordering a disk from the platform catalog — you state size/type, DCS provisions it"). `oc get storageclass` → check: DCS storage classes listed. **SVG diagram** of PVC→SC→PV (page bundle). [PersistentVolumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) + [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/) upstream. Examiner: `oc get storageclass` succeeds and the File/Block SCs are present.
- **`02-ephemeral-storage.md`** *(demo slot — motivate the problem)* — before any PVC, show ephemeral behaviour (from the Storage-101 lightning-talk demo). Deploy the app with no volume (`oc create deployment hello-dcs --image=…`), write a note into the container filesystem (`/opt/app-root/src/note`), delete the Pod, and show the note is **gone** on the fresh Pod. Lesson: the container filesystem dies with the Pod → "no Pod, no data". Examiner: app ready; note absent after the Pod is replaced.
- **`03-request-and-mount.md`** *(demo slot)* — `editor:open-file` `pvc-file.yaml`; `oc apply -f pvc-file.yaml` → polling check: PVC **Bound**. Re-apply the app now carrying the volume (`envsubst < hello-dcs-with-volume.yaml | oc apply -f -`) → polling check: workload ready with the volume mounted. **Mount under the image's writable home — `/opt/app-root/src/data`, NOT `/data`** (the image is non-root; a root-owned mount at `/data` gets `Permission denied`; note this as a teaching point). Write a marker: `oc exec deploy/hello-dcs -- sh -c 'echo persisted-marker-42 > /opt/app-root/src/data/marker'` → check: file present. Examiner: PVC Bound; volume mounted; marker file exists.
- **`04-prove-it-persists.md`** *(demo slot — the payoff)* — restart the pod (`oc rollout restart deploy/hello-dcs` or `oc delete pod -l app=hello-dcs`); in the **lower split terminal** `watch oc get pods,pvc` (`execute-2`); when the new pod is Ready, read the marker back: `oc exec deploy/hello-dcs -- cat /opt/app-root/src/data/marker` → the same value. This is the persistence proof. Examiner: after restart, the marker is **still readable** with the original value.
- **`05-file-block-and-classification.md`** — concept, folded: **File** (RWX, shareable across pods/nodes) vs **Block** (RWO, single-writer, lower-latency) and when each fits ([access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) upstream, SC names via variables). Then the DCS hooks: **data & security classification drives SC choice** — framed as **classification level, not just country**: national vs international/**NATO** data, where higher/international classification may mandate **physically separated** disks (a dedicated SC); wrong SC is a *compliance* issue, not just performance. And **object (S3) storage is available on DCS, requested via an ITSM ticket** (consumed over the S3 API) — not a self-service PVC; frame it as *available, different path*, not a dead end. Inline blurbs + DCS docs (storage / data classification). No new commands.
- **`99-workshop-summary.md`** — recap PVC/SC/PV, persistence proof, File vs Block, classification-driven choice, S3-via-ticket. **Challenge** (unguided): request the **Block** PVC (`pvc-block.yaml`) and confirm it binds — examiner-validated + hint + reveal. This closes the Core happy-path spine (A01→A05: what is DCS → deploy → configure/fix → expose → persist); point forward to the orientation labs (A06 vocabulary, A07 ITSM, A08 console) and the Developer track for the mechanisms. **Check Your Understanding** (4 Q): what a StorageClass does; File vs Block access modes; what proves persistence; how you get S3 on DCS.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`. No `cd`.
- **Split terminal:** upper `execute-1` = apply/exec/read; lower `execute-2` = `watch oc get pods,pvc` during the restart.
- **Key tracking point:** the marker lives in the **mounted volume path** (`/data`), not the container filesystem — that's the whole point of the persistence proof.
- Patterns: `oc get storageclass`, `oc apply -f pvc-file.yaml`, `oc get pvc`, `oc apply -f hello-dcs-with-volume.yaml`, `oc exec deploy/hello-dcs -- sh -c 'echo ... > /data/marker'`, `oc rollout restart deploy/hello-dcs`, `oc exec deploy/hello-dcs -- cat /data/marker`.

## 8. Design Notes

- Covers **course-topics idea 6b** — merges old **A07 (Storage, concept + persistence proof)** + old **B05 (Stateful Storage, developer hands-on)** into one Core lab: the persistence proof is the spine (everyone), File-vs-Block + classification is the folded concept, and the Block PVC is the challenge.
- **Author's storage demo (pending):** see the TODO at the top. Pages 02–03 are designed as the "demo slot" — whatever app/manifests the demo supplies, the arc stays PVC → mount → write → **restart** → read-back proof. Reconcile exercise files before implementation.
- **SC names are variables** (`dcs_sc_file`, `dcs_sc_block`) — never hardcode; DCS may rename/re-tier them (P2 in tasks.md). Old B05 used a single `dcs_storage_class` param — this plan standardises on the File/Block pair from old A07.
- **File + Block via PVC (self-service); S3 via ITSM ticket (not self-service)** — keep the distinction crisp so learners don't hunt for an S3 storage class.
- **RWO vs replicas caveat** (from old B05): a single RWO Block volume doesn't fan out to many replicas — worth a one-line honest note; the operator-managed stateful pattern (e.g. CloudNativePG) is a later/Developer-track topic, not Core.
- **Classification-driven SC selection** is the DCS-specific hook — keep it conceptual in Core; the Security/Architect tracks deepen residency + the data-classification matrix.
- Reuses the shared **hello-dcs** app — no new images. This is the last of the A01–A05 happy-path spine.
