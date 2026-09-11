# Workshop Plan: lab-b08-short-lived-containers

## 1. Workshop Metadata

- **Name:** `lab-b08-short-lived-containers`
- **Title:** Short-Lived & Helper Containers
- **Description:** Jobs that run to completion, CronJobs that schedule them, and the two helper containers that share a Pod with your app — init containers that must finish first, and sidecars that run alongside.
- **Duration:** 25m
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `80`
- **Prerequisites (curricular only):** Core *Deploy Your First App*; helpful: **Health & Resources**
- **Status:** New lab, written 2026-09-11. Covers the author's three extra topics — Jobs/CronJobs, init containers and sidecars — in one lab, because they answer the same question.

## 2. Workshop Configuration

Terminal `split`, editor, slides, examiner. Budget `medium`. **vcluster `false`**. Self-contained: every object is created by the learner.

No new image: the Jobs, the CronJob and both helper containers all run `samples/hello-dcs:1.0` with a `command:` override. On an air-gapped platform an extra utility image would need mirroring, and nothing here needs one.

## 3. Learning Objectives

- Run work to completion with a **Job**, and read its result from the Pod it keeps.
- Explain `backoffLimit`, `restartPolicy` and `ttlSecondsAfterFinished`, and watch a failing Job reach a **verdict**.
- Schedule work with a **CronJob**, trigger a run by hand to test it, and suspend it.
- Use an **init container** for work that must finish before the app starts.
- Say what makes a container a **sidecar** — the same API plus `restartPolicy: Always`.

## 4. The organising idea

One question runs through the lab: **how long is this container supposed to run?** Forever (Deployment), until done (Job), until done on a schedule (CronJob), or beside the app (init container / sidecar). The four shapes are taught as four answers to that question rather than as four unrelated objects.

## 5. Exercise Files

- `job-migrate.yaml` — succeeds. `restartPolicy: Never`, `backoffLimit: 2`, `ttlSecondsAfterFinished: 600`.
- `job-failing.yaml` — fails on purpose with `backoffLimit: 1`, so it makes **two attempts** and stops.
- `cronjob-report.yaml` — `0 3 * * *` (deliberately never fires during the lab), `concurrencyPolicy: Forbid`, history limits.
- `deployment-with-helpers.yaml` — one Pod, three containers: `setup` (init), `heartbeat` (**`restartPolicy: Always`** → sidecar), and the app, sharing an `emptyDir`.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — everything so far was meant to run forever, and that is wrong for a lot of real work.
- **`01-how-long-should-it-live/`** — the four shapes, and the surprise that a native sidecar is declared as an init container. **SVG** `container-shapes.svg`. Explains *why* (init containers have guaranteed ordering: started before the app, stopped after it).
- **`02-a-job.md`** — read the three fields first, run it with `oc wait --for=condition=complete`, see the `Completed` Pod kept as the record, read its logs.
- **`03-when-a-job-fails.md`** — the contrast with `CrashLoopBackOff`: a Job reaches a verdict. Waits for `condition=failed`, shows **both** attempts preserved (`restartPolicy: Never`), reads `BackoffLimitExceeded` and the real error.
- **`04-a-cronjob.md`** — create it, trigger a run with `oc create job --from=cronjob/…` (testing the real template), suspend it. Warns that missed runs are not caught up.
- **`05-helpers-in-the-pod.md`** — apply the three-container Pod, read the init container's finished log next to the sidecar's still-growing one, then read from the **app** container a file the exited init container wrote.
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, 4-question knowledge check.

## 7. Examiner Coverage (13 checks)

`verify-job-completed` · `verify-job-logs` · `verify-job-failed-after-retries` · `verify-failed-pods-kept` · `verify-failure-reason-readable` · `verify-cronjob-created` · `verify-manual-run-completed` · `verify-report-output` · `verify-cronjob-suspended` · `verify-pod-with-helpers-ready` · `verify-init-completed` · `verify-sidecar-still-running` · `verify-shared-volume-handoff`

The three that carry the lab's real claims:

- **`verify-init-completed`** asserts `state.terminated.exitCode == 0` on the init container — it *finished*, which is the guarantee.
- **`verify-sidecar-still-running`** asserts `state.running` on `heartbeat` **and** a ready app container — running *together* is the point, and it is what `restartPolicy: Always` buys.
- **`verify-shared-volume-handoff`** reads both files **from the app container**, proving the shared volume and the two different lifetimes in one command.

Every check that waits on an eventual state polls internally (see the harness rule: `smoke_test.py` runs each grader once).

## 8. Design Notes

- The failing Job is not decoration. "A Job gives up and tells you" is the property that distinguishes it from a Deployment, and it is only convincing if the learner watches it happen.
- The CronJob's schedule is set to 03:00 **so that it cannot fire during the lab** — every observation is then deterministic, and triggering by hand is the technique worth teaching anyway.
- Native sidecars need Kubernetes **1.29+** (test cluster: 1.35). On an older cluster `heartbeat` would run as an ordinary init container and block the app from starting — worth checking before this lab ships to a different platform version.
- The link check caught two wrong upstream URLs here (`/controllers/cron-job/` and `/controllers/cronjob/` are both 404; the real one is `/controllers/cron-jobs/`).
