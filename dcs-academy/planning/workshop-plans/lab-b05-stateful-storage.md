# Workshop Plan: lab-b05-stateful-storage

## 1. Workshop Metadata

- **Name:** `lab-b05-stateful-storage`
- **Title:** Stateful Workloads & Storage
- **Description:** Give the sample app persistence — request a PVC from a DCS storage class, mount it, write data, and prove the data survives a pod restart.
- **Duration:** 35m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer) — *optional*
- **Prerequisites:** B01 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (see the PVC bind)
- Examiner: `enabled: true`
- Budget: `medium`
- **vcluster decision:** `false` — native session namespace.
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs; storage class name via a param (e.g. `{{< param dcs_storage_class >}}`) so it's not hard-coded to the cluster.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Request storage with a PersistentVolumeClaim and choose an appropriate DCS storage class.
- Mount a volume into the app and write to it.
- Explain access modes (RWO vs RWX) and when each applies.
- Demonstrate that data persists across a pod restart (and does not with `emptyDir`).

## 4. Connection to Previous Workshop

**Already known:** deploy/scale the app (B01/B03); A07 (Storage) introduced PVCs and DCS storage classes at the platform level.

**New here:** the *developer* view — attaching a PVC to your own app, writing to it, and reasoning about access modes vs replicas.

**Do NOT re-teach:** what a storage class / PVC is (A07) — reference it; focus on wiring it into the app and proving persistence.

## 5. Exercise Files to Create

- `exercises/pvc.yaml` — PVC `hello-dcs-data`, `storageClassName: {{< param dcs_storage_class >}}`, RWO, a small size within budget.
- `exercises/deployment-stateful.yaml` — hello-dcs Deployment with the PVC mounted at a data path and a tiny init/write so there's something to persist.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; recap "pods are ephemeral" (B01) as the motivation; objectives; open `pvc.yaml`.
- **`01-why-persistence.md`** — ephemeral container filesystem vs a PVC; the promise: data outlives the pod. Contrast with `emptyDir`. Examiner: none (concept).
- **`02-request-a-volume.md`** — apply the PVC; `oc get pvc` → Bound; which DCS storage class and why (RWO default). Examiner: PVC exists and is **Bound**.
- **`03-mount-and-write.md`** — apply `deployment-stateful.yaml`; `oc exec` to write a file into the mounted path; read it back. Examiner: the mount exists and the file is present.
- **`04-prove-it-persists.md`** — delete the pod (or `oc rollout restart`); watch a new pod attach the **same** PVC; read the file again — still there. Optionally show an `emptyDir` variant losing it. Examiner: after restart, the data is still readable (persistence proven).
- **`99-workshop-summary.md`** — recap PVC/storage class/access modes/persistence. Note RWO + multiple replicas caveat (→ real stateful apps often want an operator, e.g. CloudNativePG in Module F). Check Your Understanding (4–5 Q). This is the last app-lifecycle lab; suggest **B06 Dev Spaces** (develop *on* DCS) or Module E/F.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes.
- Patterns: `oc apply -f`, `oc get pvc`, `oc exec deploy/hello-dcs -- sh -c 'echo ... > /data/f; cat /data/f'`, `oc delete pod -l app=hello-dcs`, split-terminal `watch oc get pods,pvc`.

## 8. Design Notes

- Covers **course-topics idea 11** (stateful workloads / storage). Marked *optional* in the module map — self-contained so it can be skipped without breaking the B chain.
- Storage class is **parameterised** (`{{< param dcs_storage_class >}}`) — never hard-code a cluster-specific class (house standard: variablize everything).
- **RWO vs replicas:** flag honestly that a single RWO volume doesn't fan out to many replicas — bridges to the operator-managed stateful pattern (Module F, CloudNativePG) rather than pretending an app can naively scale a shared volume.
- Reuses the A07 storage foundation from the developer's seat; keeps the size tiny for CRC/DCS determinism.
