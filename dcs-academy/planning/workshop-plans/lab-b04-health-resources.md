# Workshop Plan: lab-b04-health-resources

## 1. Workshop Metadata

- **Name:** `lab-b04-health-resources`
- **Title:** Health & Resources
- **Description:** Scale the sample app, hit your namespace quota on purpose, right-size its requests and limits, then give it liveness and readiness probes and watch the platform keep it alive.
- **Duration:** 25m (tune to the observed median after the first live runs)
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `40`
- **Prerequisites (curricular only):** Core — *Deploy Your First App*, *Configure & Troubleshoot Your App*
- **Status:** Re-authored 2026-09-11 from the superseded `lab-b07-scaling-health`.

## 2. Workshop Configuration

- Terminal `split`, editor enabled, slides enabled, examiner enabled
- Console (Kubernetes Dashboard): **not** enabled — the GUI story for health and resources is its own optional console lab in this track
- Budget: **`medium`**, deliberately — four Pods on the namespace LimitRange defaults fill its limit side *exactly*, and `deployment-oversized.yaml` is sized to exceed it. The budget is the lesson.
- **vcluster:** `false` — the session namespace's own quota is the subject; a vcluster would hide it behind a separately-budgeted namespace.
- **Self-contained:** the learner applies `deployment-base.yaml` + `service.yaml` on page 01. No `session.objects` pre-deploy (the superseded lab pre-deployed the app with a **hardcoded** registry — that is what this re-author fixes) and no state from another lab.

## 3. Learning Objectives

- Scale a Deployment and reason about replica count against a namespace budget.
- Read a `ResourceQuota` to tell whether a rollout has room to land.
- Diagnose a quota rejection from cluster events, and fix it by right-sizing `requests`/`limits`.
- Explain what **readiness** protects versus what **liveness** protects, and configure both.
- Explain what brings a deleted Pod back.

## 4. Connection to the rest of the course

**Already known:** Deployments, `oc scale`, rollouts, reading `describe`/`events`.

**New here:** the budget as a hard constraint, admission-time rejection, requests vs limits as two different jobs, probes, and reconciliation watched live.

**Deliberately not here:** autoscaling (b05 — and it needs the `requests` this lab sets), PodDisruptionBudget and graceful shutdown (b09), StatefulSet sizing (b07).

## 5. Exercise Files

- `deployment-base.yaml` — one replica, **no** `resources`, no probes (so its Pods take the LimitRange defaults, which is what makes the quota arithmetic visible).
- `service.yaml` — a stable address, so readiness has an endpoint list to watch.
- `deployment-oversized.yaml` — 700m/700Mi per container: refused at admission.
- `deployment-probes.yaml` — the target state: 50m/64Mi requests, 100m/128Mi limits, readiness on `/`, liveness on `/healthz`.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — the three problems with a one-replica app, objectives, prerequisites, the `medium` budget called out up front.
- **`01-scale-and-the-budget/`** — apply the app, scale to 4, read the quota. **SVG** `quota-budget.svg`. Ends on "zero headroom on limits".
- **`02-hitting-the-limit.md`** — apply the oversized manifest, watch the rollout refuse to land, read the `FailedCreate` event left to right.
- **`03-right-sizing.md`** — requests vs limits, apply the right-sized manifest over the stuck rollout, confirm the budget now has headroom.
- **`04-liveness-and-readiness/`** — the two questions, read the configured probes, endpoints as the thing readiness controls, break readiness with `oc set probe`, see one address leave the Service, restore. **SVG** `probe-flow.svg`.
- **`05-self-healing.md`** — delete one Pod by name, watch the ReplicaSet replace it; desired-vs-actual in both directions.
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, with a 4-question knowledge check.

## 7. Examiner Coverage (13 checks, one per command)

`verify-app-deployed` · `verify-scaled` (arg: 4) · `verify-quota-present` · `verify-oversized-pending` · `verify-quota-event-visible` · `verify-right-sized` · `verify-quota-headroom` *(new)* · `verify-probes-configured` · `verify-endpoints-ready` · `verify-readiness-broken` · `verify-endpoints-reduced` *(new)* · `verify-readiness-restored` · `verify-pod-replaced`

The superseded lab reused `verify-scaled` and `verify-right-sized` twice each for different commands; each command now has its own assertion, and the two new checks assert the two effects the old lab only described in prose (budget headroom recovered, the unready Pod actually leaving the endpoints).

## 8. Terminal Working Directory

`~/exercises`, no `cd`. Upper pane (`execute-1`) for commands; lower pane (`session: 2`) for the two `--watch` observations, each wrapped in `timeout 60` so nothing is left running.

## 9. Design Notes

- **The quota arithmetic is load-bearing:** `deployment-base.yaml` must set **no** `resources`, or the Pods stop taking the LimitRange defaults and four replicas no longer fill the budget exactly.
- Probes are *read* before they are *broken* — the break is the demonstration, not the introduction.
- Liveness is explained but never fires: the honest thing to say is that readiness was the only probe in play, and why.
