# Workshop Plan: lab-b03-scaling-health

## 1. Workshop Metadata

- **Name:** `lab-b03-scaling-health`
- **Title:** Scaling, Health & Resources
- **Description:** Make the sample app resilient and quota-friendly — scale it, add liveness/readiness probes, and set requests/limits that fit your DEV namespace budget.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B01 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (watch replicas + events)
- Examiner: `enabled: true`
- Budget: `medium` — **deliberately sized so the learner can hit the quota when over-requesting**, then right-size.
- **vcluster decision:** `false` — native session namespace; the namespace budget *is* the quota the learner works within.
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs (pre-deployed via `session.objects`).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Scale a Deployment and reason about replica count vs quota.
- Add liveness and readiness probes and explain the difference.
- Set resource requests/limits that fit the namespace budget.
- Diagnose and resolve a quota rejection by right-sizing requests.

## 4. Connection to Previous Workshop

**Already known** (B01/B02): deploy/expose the app, `oc scale`, config via ConfigMap/Secret, the DEV namespace.

**New here:** liveness vs readiness probes; requests vs limits; the namespace **ResourceQuota/LimitRange** as a real constraint; the failure mode when total requests exceed the budget.

**Do NOT re-teach:** `oc scale` mechanics (seen in A02/B01) — use it, focus on the *reasoning* (quota, health).

## 5. Exercise Files to Create

- `exercises/deployment-probes.yaml` — hello-dcs Deployment with `livenessProbe` + `readinessProbe` (HTTP GET on 8080) and a modest `resources` block.
- `exercises/deployment-oversized.yaml` — same app with **intentionally large** requests that exceed the namespace budget (used to trigger, then diagnose, a quota rejection).
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; recap B01 single replica / no health; objectives; open `deployment-probes.yaml`.
- **`01-scaling-and-the-quota.md`** — scale to N; `oc get resourcequota`/`oc describe quota`; what the DEV namespace budget means on DCS. VM-world analogy (very light now — advanced audience): "your namespace is a resource pool with a cap." Examiner: quota object present; N replicas ready.
- **`02-hitting-the-limit.md`** — apply `deployment-oversized.yaml`; observe pods stuck **Pending** with a quota/`FailedCreate` event (`oc get events`, `oc describe`); read the message. Examiner: the oversized rollout is *not* fully ready (proves the constraint bites).
- **`03-right-sizing.md`** — requests (scheduling) vs limits (enforcement); pick values within budget; re-apply; pods schedule. Examiner: pods Running within budget; requests ≤ a sane ceiling.
- **`04-liveness-and-readiness.md`** — why probes: readiness gates traffic, liveness restarts a hung container; add both; show a pod flipping Ready; break readiness briefly (bad path) and watch it leave/return to endpoints in a split terminal. Examiner: probes present; pod Ready and in Service endpoints.
- **`99-workshop-summary.md`** — recap scale/quota/requests/limits/probes. Note the app is healthy but *will still break in ways you must diagnose* → motivates **B04 Debugging & Logs**. Check Your Understanding (4–5 Q).

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes.
- Patterns: `oc scale deploy/hello-dcs --replicas=N`, `oc get resourcequota`, `oc describe quota`, `oc get events --sort-by=.lastTimestamp`, split-terminal `watch oc get pods -o wide`.

## 8. Design Notes

- Covers **course-topics idea 9** (scaling, health & resources under quota).
- The **oversized-then-right-size** arc makes the DCS namespace budget tangible — mirrors A03's "quota is real" message from the developer's seat.
- Probes use the app's own `/` on 8080 (no extra endpoint needed); keep values gentle so the lab is deterministic on CRC/DCS.
- **Deliberate limitation:** everything here is "make it work well"; **B04** deliberately breaks it so the learner practises diagnosis.
