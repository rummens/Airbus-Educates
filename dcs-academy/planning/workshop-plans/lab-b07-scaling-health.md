# Workshop Plan: lab-b07-scaling-health

## 1. Workshop Metadata

- **Name:** `lab-b07-scaling-health`
- **Title:** Scaling, Health & Resources
- **Description:** Make the sample app resilient and quota-friendly — scale it, hit the namespace budget and right-size, add liveness/readiness probes, then kill a Pod and watch it self-heal.
- **Duration:** 35m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** Module A (Core)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (watch replicas + events)
- Examiner: `enabled: true`
- Budget: `medium` — **deliberately sized so the learner can hit the quota when over-requesting**, then right-size.
- **vcluster decision:** `false` — native session namespace; the namespace budget *is* the quota the learner works within.
- Workshop image: `dcs-workshop-base`
- Sample app: `hello-dcs` (pre-deployed via `session.objects`), image via `${DCS_REGISTRY}/samples/hello-dcs:1.0`.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Scale a Deployment and reason about replica count vs quota.
- Add liveness and readiness probes and explain the difference.
- Set resource requests/limits that fit the namespace budget.
- Diagnose and resolve a quota rejection by right-sizing requests.
- Delete a Pod and confirm the platform self-heals it back to desired state.

## 4. Connection to Previous Workshop

**What the learner already knows** (from Module A, Core):
- Deploy and expose the app, `oc scale`, config via ConfigMap/Secret, and that a namespace has a budget (Core A02/A03; the quota was read in B05).

**What is new in this workshop:**
- Liveness vs readiness probes; requests vs limits; the namespace **ResourceQuota/LimitRange** as a real constraint that *bites*; the failure mode when total requests exceed the budget; self-healing seen live.

**What should NOT be re-taught:**
- Do not re-teach `oc scale` mechanics (Core A02) — use it, focus on the *reasoning* (quota, health).
- Do not re-teach ConfigMap/Secret or quota vocabulary — reference it.

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the Scaling, Health & Resources workshop."

### exercises/deployment-probes.yaml
**Purpose:** The healthy target Deployment (page 04).
**Initial contents:** `hello-dcs` Deployment with `livenessProbe` + `readinessProbe` (HTTP GET on 8080) and a modest `resources` block. Image via `${DCS_REGISTRY}/samples/hello-dcs:1.0`.

### exercises/deployment-oversized.yaml
**Purpose:** Trigger, then diagnose, a quota rejection (page 02).
**Initial contents:** Same app with **intentionally large** requests that exceed the namespace budget. Image via `${DCS_REGISTRY}/samples/hello-dcs:1.0`.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Set up the "make it robust within the budget" goal.
**Content outline:**
- First-time note; recap the single-replica, no-health app from Core; state objectives; open `deployment-probes.yaml` (`editor:open-file`). 35m / intermediate. No cluster actions yet.

### 01-scaling-and-the-quota.md
**Purpose:** Scale up and meet the namespace budget.
**Content outline:**
- `oc scale deploy/hello-dcs --replicas=N` (`terminal:execute`) → examiner check: N replicas ready.
- `oc describe quota` / `oc get resourcequota` → check: the quota object is present; explain what the DEV namespace budget means on DCS. Light VM-world analogy (advanced audience): "your namespace is a resource pool with a cap."

### 02-hitting-the-limit.md
**Purpose:** Over-request and see the constraint bite.
**Content outline:**
- `envsubst < deployment-oversized.yaml | oc apply -f -` (image ref uses `${DCS_REGISTRY}` — never plain `oc apply`) → observe Pods stuck **Pending** with a quota/`FailedCreate` event.
- `oc get events --sort-by=.lastTimestamp` / `oc describe` → read the message. Examiner: the oversized rollout is *not* fully ready (proves the constraint bites).

### 03-right-sizing.md
**Purpose:** Fit within budget.
**Content outline:**
- Requests (scheduling) vs limits (enforcement); pick values within budget (`editor:replace-matching-text` or re-apply `deployment-probes.yaml`); `envsubst < deployment-probes.yaml | oc apply -f -` → Pods schedule. Examiner: Pods Running within budget; requests ≤ a sane ceiling.

### 04-liveness-and-readiness.md
**Purpose:** Add health probes.
**Content outline:**
- Why probes: readiness gates traffic, liveness restarts a hung container; add both (already in `deployment-probes.yaml`); show a Pod flipping Ready. Break readiness briefly (bad path) and watch it leave/return to endpoints in a split terminal (`execute-2` runs `watch oc get pods -o wide`). Examiner: probes present; Pod Ready and in Service endpoints.

### 05-self-healing.md
**Purpose:** Prove the platform maintains desired state.
**Content outline:**
- `oc get pods` then `oc delete pod <name>` (`terminal:execute`) → in the split terminal watch a replacement Pod appear and reach Ready. Explain the ReplicaSet/Deployment reconciliation that drove it. Examiner: replica count restored to desired; new Pod Ready. Constructs → [upstream](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

### 99-workshop-summary.md
**Purpose:** Recap and place the lab in the track.
**Content outline:**
- Recap scale/quota/requests/limits/probes/self-heal.
- **Check Your Understanding** (4 Q): replicas vs quota; readiness vs liveness; requests vs limits; what self-heals a deleted Pod.
- Point onward in the Developer track (e.g. **B08** Operators for the advanced capstone); note observability/debugging basics live in Core now.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes.
- Command patterns: `oc scale deploy/hello-dcs --replicas=N`, `oc describe quota`, `oc get events --sort-by=.lastTimestamp`, `envsubst < f.yaml | oc apply -f -` for any manifest with a `${DCS_REGISTRY}` image ref, `oc delete pod <name>`, split-terminal `watch oc get pods -o wide` on `execute-2`.

## 8. Design Notes

- **Renumbered from old B03 (Scaling, Health & Resources) → B07**; prereq changed from old B01 to **Module A (Core)** since app-lifecycle basics moved into Core. Covers course-module-b idea 9.
- The **oversized-then-right-size** arc makes the namespace budget tangible from the developer's seat; the delete-a-Pod self-heal is the memorable proof of declarative desired-state.
- Probes use the app's own `/` on 8080 (no extra endpoint); keep values gentle so the lab is deterministic on CRC/DCS.
- **Carry-forward bug:** manifests with `${DCS_REGISTRY}` are applied with `envsubst < f.yaml | oc apply -f -`, never plain `oc apply`.
- The old B03 bridged forward to "B04 Debugging & Logs" — that content moved to **Core A03**, so this summary no longer points there.
