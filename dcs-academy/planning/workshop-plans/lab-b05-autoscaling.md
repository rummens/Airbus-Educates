# Workshop Plan: lab-b05-autoscaling

## 1. Workshop Metadata

- **Name:** `lab-b05-autoscaling`
- **Title:** Autoscaling
- **Description:** Let a HorizontalPodAutoscaler own the replica count — read live CPU metrics against your requests, drive the app under load and watch it scale out, then understand scale-in, the quota ceiling and where VPA fits.
- **Duration:** 20m (tune to the observed median after the first live runs)
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `50`
- **Prerequisites (curricular only):** **Health & Resources** (b04) — the HPA measures against the `requests` set there
- **Status:** New lab, written 2026-09-11. No predecessor in the superseded track.

## 2. Workshop Configuration

- Terminal `split`, editor, slides, examiner — all enabled
- Budget `medium`; **vcluster `false`** (the HPA reads the session namespace's own Pod metrics; a vcluster puts the workload where the cluster metrics pipeline does not serve it)
- Self-contained: the learner applies `deployment.yaml`, `service.yaml` and `hpa.yaml`. No `session.objects`, no state from another lab.
- **No extra load-generator image.** Load is eight parallel `curl` loops from the session terminal — air-gapped-clean, no registry question, nothing left running (the loops are time-bounded and the watch is wrapped in `timeout`).

## 3. Learning Objectives

- Explain how an HPA turns CPU metrics **plus your CPU requests** into a replica count.
- Create an HPA with `autoscaling/v2` and read its status, conditions and events.
- Drive an app under load and watch it scale out.
- Explain why scale-in waits out a stabilisation window.
- Set `maxReplicas` from the namespace budget rather than from imagination.
- Say what VPA does differently, and why you never point both at the same resource.

## 4. Connection to the rest of the course

**Builds on b04:** requests are the denominator of every HPA utilisation figure, and the quota is the ceiling the HPA cannot beat. Both facts were established hands-on in b04; this lab spends them.

**Deliberately not here:** cluster autoscaling (a platform concern, not a tenant one), custom/external metrics (needs an adapter and a metric worth teaching), KEDA.

## 5. Exercise Files

- `deployment.yaml` — `replicas: 1` as a starting point only, `requests.cpu: 100m`, probes, `limits.cpu: 200m`.
- `service.yaml` — the address load is driven at, and what new replicas join.
- `hpa.yaml` — `autoscaling/v2`, min 1, max 6, CPU at 50% average utilisation.

`maxReplicas: 6` is chosen from the budget: 6 × 200m = 1.2 CPU inside a `medium` namespace's 2 CPU limit ceiling, so a full scale-out can never be refused. The lab asserts that arithmetic rather than asserting it.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — framing, objectives, the b04 prerequisite stated as a hard dependency.
- **`01-how-hpa-works/`** — the loop (metrics → controller → replica count → Pods), requests as the denominator with worked numbers, what an HPA does *not* do. **SVG** `hpa-loop.svg`.
- **`02-create-the-hpa.md`** — apply app + Service, apply the HPA, read `oc get hpa` (TARGETS) and `oc describe hpa` (conditions/events). Names the `oc autoscale` one-liner equivalent.
- **`03-put-it-under-load.md`** — watch in the lower pane, eight parallel curl loops in the upper, watch TARGETS climb and Pods appear, read the `SuccessfulRescale` event and its reason.
- **`04-scale-in-and-ceilings.md`** — the 5-minute stabilisation window and *why* the asymmetry exists; read `.spec.behavior`; then the budget as the real ceiling, with the `maxReplicas: 20` counter-example and `ScalingLimited`.
- **`05-vertical-autoscaling.md`** — VPA: what it changes, recommendation-first, never both autoscalers on one resource, and the DCS operator ownership split. **Concept page, no commands** (and therefore no examiner check — nothing is asserted because nothing is done).
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, 4-question knowledge check.

## 7. Examiner Coverage (8 checks)

`verify-app-with-requests` · `verify-hpa-created` · `verify-hpa-has-metrics` · `verify-hpa-scaled-up` · `verify-hpa-scale-event` · `verify-hpa-still-reading` · `verify-hpa-behavior-read` · `verify-quota-fits-max`

## 8. Environment dependency — the Metrics API

**Four of the eight checks need the cluster's Metrics API** (per-Pod CPU): `verify-hpa-has-metrics`, `verify-hpa-scaled-up`, `verify-hpa-scale-event`, `verify-hpa-still-reading`.

CRC ships with **cluster monitoring disabled**, so `oc adm top` fails and every HPA utilisation figure is permanently `<unknown>`; an HPA there never leaves `minReplicas` no matter the load. Those four are **excluded in the smoke plan with that reason**, so the gate stays honest rather than silently passing.

On a cluster with user-workload monitoring (real DCS, or CRC with monitoring enabled) the exclusions should be removed and all eight should pass. **This is the same dependency the whole Operate & Observe track has** — o01 (Metrics) and o02 (Logs) cannot be smoke-tested at all until the test cluster serves metrics and logs.

## 9. Design Notes

- Load is generated from the terminal on purpose: a load-generator image would need mirroring, and the point of the page is the HPA's reaction, not the tool.
- The scale-**in** page deliberately does *not* wait out the five minutes — it reads `.spec.behavior` and explains the default instead. Burning a third of the lab's runtime on a timer teaches nothing.
- `verify-quota-fits-max` asserts the lab's own arithmetic, so a later edit that raises `maxReplicas` or the per-Pod limit past the budget fails the gate instead of teaching a broken example.
