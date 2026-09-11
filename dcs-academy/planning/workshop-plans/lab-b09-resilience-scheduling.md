# Workshop Plan: lab-b09-resilience-scheduling

## 1. Workshop Metadata

- **Name:** `lab-b09-resilience-scheduling`
- **Title:** Resilience & Scheduling
- **Description:** State your terms for planned disruption with a PodDisruptionBudget, learn what a container that ignores SIGTERM costs at shutdown, and spread replicas so one node's failure is not your outage.
- **Duration:** 25m
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `90` — **the last lab in the track**
- **Prerequisites (curricular only):** **Health & Resources**; helpful: **Services & Cluster Networking**
- **Status:** New lab, written 2026-09-11. Covers the author's PDB + graceful-shutdown + scheduling topics in one lab.

## 2. Workshop Configuration

Terminal `split`, editor, slides, examiner. Budget `medium` (3 small replicas). **vcluster `false`**. Self-contained.

## 3. Learning Objectives

- Tell **voluntary** disruption from **involuntary**, and match each to its defence.
- Write a PodDisruptionBudget and read `disruptionsAllowed` from its status.
- Explain why a budget that allows nothing blocks the maintenance that patches the cluster.
- Explain the shutdown sequence (`preStop`, `SIGTERM`, grace period, `SIGKILL`) and what ignoring `SIGTERM` costs.
- Spread replicas, and choose between `ScheduleAnyway` and `DoNotSchedule`.

## 4. What was measured before writing (not assumed)

| Claim | Measured on the test cluster |
|---|---|
| A tenant can create a PDB | `educates-admin-session-role` grants `policy/poddisruptionbudgets` create/patch/delete |
| A tenant **cannot** evict a Pod | the same role has **no** `pods/eviction` — so the PDB cannot be demonstrated by evicting |
| 3 replicas, `minAvailable: 2` | `disruptionsAllowed: 1`, `currentHealthy: 3`, `expectedPods: 3` |
| Scaled to 2 | `disruptionsAllowed: 0` |
| `preStop: sleep 10` + grace 30s | `oc delete pod` took **31 seconds** |

The eviction finding shaped the whole lab: **the PDB is taught through its own status**, which is honest for a tenant who never runs a drain, and fully observable in a session namespace.

The 31-second measurement shaped page 03: `hello-dcs` is a plain Python server that does **not** handle `SIGTERM`, so the kubelet waits out the entire grace period and then `SIGKILL`s it. That is a better lesson than a tidy 10 seconds, and the check reports which case it saw.

## 5. Exercise Files

- `deployment.yaml` — 3 replicas, `terminationGracePeriodSeconds: 30`, `preStop: sleep 10`.
- `pdb.yaml` — `minAvailable: 2`.
- `deployment-spread.yaml` — adds `topologySpreadConstraints` (`maxSkew: 1`, `kubernetes.io/hostname`, **`ScheduleAnyway`**) and a preferred `podAntiAffinity`.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — the platform will move your Pods; states plainly that the learner will **not** drain a node, because that is not a tenant's action. Objectives, prerequisites.
- **`01-two-kinds-of-disruption/`** — involuntary vs voluntary, the defence for each, and the fact that both end in the same shutdown sequence. **SVG** `disruption-kinds.svg`.
- **`02-a-budget-for-maintenance.md`** — deploy 3, apply the PDB, read the five status columns together, then scale to the floor and watch `disruptionsAllowed` reach **0**. The warning that this blocks patching, and the real fix (more replicas, not a lower floor).
- **`03-shutting-down-well.md`** — the sequence and its race, read the configured values, **time a real deletion** into `/tmp/shutdown-seconds.txt`, then account for the full grace period: the app ignores `SIGTERM`. Closes on a too-short grace period being worse than a too-long one.
- **`04-spreading-replicas.md`** — where the Pods are now, the two ways to ask for spread, and the `whenUnsatisfiable` decision. Names the single-node case explicitly so a training cluster does not look broken.
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, 4-question knowledge check, and the track-closing pointer to Operate & Observe.

## 7. Examiner Coverage (10 checks)

`verify-app-ready` · `verify-pdb-created` · `verify-disruptions-allowed` · `verify-disruptions-blocked` · `verify-headroom-restored` · `verify-grace-settings` · `verify-shutdown-took-time` · `verify-replacement-ready` · `verify-spread-constraints` · `verify-all-replicas-scheduled`

Notable:

- **`verify-pdb-created`** asserts `expectedPods >= 1`, so a PDB whose selector matches nothing — the classic silent mistake — cannot pass.
- **`verify-shutdown-took-time`** reads the duration the page measured, requires ≥ 8s (the `preStop` pause alone), and *reports* whether the full grace period was spent.
- **`verify-all-replicas-scheduled`** deliberately passes on a single-node cluster and says so in its message, because `ScheduleAnyway` is precisely what makes that case work.

Every check that waits on an eventual state polls internally.

## 8. Design Notes

- **No node drain, by design.** Draining is the platform's action and needs cluster-admin; the tenant half is declaring the budget and verifying the platform understood. The lab says this out loud rather than pretending.
- The PDB pages are a **rise and fall**: 1 allowed → 0 allowed → back to 1. The middle state is the memorable one, and it is the one that causes real incidents.
- Spreading is taught as a **decision**, not a recipe: the interesting field is `whenUnsatisfiable`, and the trade-off (Pending Pods) is stated where a reader will meet it.
