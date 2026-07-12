# Workshop Plan: lab-b04-debugging-logs

## 1. Workshop Metadata

- **Name:** `lab-b04-debugging-logs`
- **Title:** Debugging & Logs
- **Description:** Diagnose a broken workload the way you would on DCS — read logs, events and `describe`, find the root cause of a pre-seeded fault, fix it, and confirm recovery.
- **Duration:** 35m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B01 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (edit the broken manifest to fix it)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (read the Pod's events/status visually)
- Examiner: `enabled: true`
- Budget: `medium`
- **vcluster decision:** `false` — native session namespace.
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs — deployed **broken** on purpose (see below).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Read a workload's state with `oc get`, `oc describe`, `oc get events` and `oc logs`.
- Map common failure signatures (CrashLoopBackOff, ImagePullBackOff, Pending, readiness-failing) to their causes.
- Apply a fix and verify recovery.
- Build a repeatable "observe → hypothesise → fix → verify" debugging loop.

## 4. Connection to Previous Workshop

**Already known** (B01–B03): deploy/expose/scale the app, probes, quota, `oc logs`/`oc describe` in passing.

**New here:** using those tools *together as a diagnostic method*; recognising failure signatures; reading events over time.

**Do NOT re-teach:** each command in isolation — the skill here is the *loop*, not the syntax.

## 5. Exercise Files to Create

- `exercises/broken-deployment.yaml` — hello-dcs Deployment with **one seeded fault** (pick a clear, deterministic one — e.g. a wrong image tag → ImagePullBackOff, or a bad readiness path → never Ready). One fault so the lab is deterministic; the fix is a single edit.
- `exercises/README.md` — placeholder with a one-line "this app is deployed broken; your job is to fix it."
- (Session pre-applies the broken Deployment via `session.objects` so the learner lands on a failing app.)

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; set the scene: "your app is down; a colleague pushed a change." Objectives; open the console on the failing Pod.
- **`01-what-is-broken.md`** — observe first: `oc get pods` shows the bad state; name the signature (e.g. `ImagePullBackOff`). No fixing yet. Examiner: the app is currently **not** ready (confirms the starting fault).
- **`02-read-the-signals.md`** — the three lenses: `oc describe pod` (events + reasons), `oc get events --sort-by=.lastTimestamp`, `oc logs` (and `--previous` for crashes). Walk the learner to the root cause line. Examiner: none (investigation page).
- **`03-form-a-hypothesis.md`** — connect the signature to the cause (bad tag → image not in Harbor; bad probe path → readiness fails); state the fix. VM-world analogy (very light): "same as reading the boot console before rebuilding the VM." Examiner: none.
- **`04-fix-and-verify.md`** — edit `broken-deployment.yaml` to correct the fault (`editor:replace-matching-text`), `oc apply`, `oc rollout status`, confirm Ready and serving. Examiner: app Running, Ready, responds 200.
- **`99-workshop-summary.md`** — recap the observe→hypothesise→fix→verify loop and the common signatures table. Bridge: apps that hold data fail differently → optional **B05 Stateful Workloads**, or jump to Module E (Observability) for fleet-wide logs/metrics. Check Your Understanding (4–5 Q).

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes.
- Patterns: `oc get pods`, `oc describe pod <p>`, `oc get events --sort-by=.lastTimestamp`, `oc logs <p> [--previous]`, `oc apply -f broken-deployment.yaml`, `oc rollout status`.

## 8. Design Notes

- Covers **course-topics idea 10** (debugging & logs). "Observe and diagnose" style, per the module map.
- **One deterministic fault** keeps the examiner reliable; the fix is a single, checkable edit. Provide a second optional fault variant in the plan's appendix for re-runs, but ship one by default.
- Reinforces air-gapped reality: an ImagePullBackOff variant teaches "the tag isn't mirrored to Harbor" — a real DCS failure mode (ties to A04, C15).
- No new objects to learn — this workshop is about *method*, using tools the learner already met.
