<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Short-Lived & Helper Containers

Not every container should run forever. A migration has to finish, a report runs nightly, a setup step must complete first, a log shipper lives alongside.

**In this lab:** Jobs · a Job that fails · CronJobs · init containers and sidecars.

Digital Container Service · DCS Academy

---

<!-- id: shapes -->
## How long should it live?

One question picks the object. A Deployment's whole job is to restart a container that stopped — which is exactly wrong for work that is *supposed* to stop.

- **Deployment** — forever. Exits are failures.
- **Job** — until done. Exit 0 is success, and the Pod is kept so you can read it.
- **CronJob** — a Job factory on a schedule.
- **init container / sidecar** — in the same Pod as the app, before it or beside it.

![Four shapes: Deployment, Job, CronJob, and the two helper containers inside one Pod](container-shapes.svg)

---

<!-- id: job -->
## A Job that finishes

```
envsubst < job-migrate.yaml | oc apply -f -
oc wait --for=condition=complete job/db-migrate --timeout=120s
oc logs job/db-migrate
```

- `restartPolicy: Never` — each attempt is a new Pod, so each attempt keeps its logs.
- `backoffLimit` — how many retries before the Job is marked Failed.
- `ttlSecondsAfterFinished` — the finished Job deletes itself, so they do not pile up.
- The Pod stays `Completed` — it is the record of the work, not litter.
- `completions` + `parallelism` turn a Job into a small batch worker.

---

<!-- id: fails -->
## When a Job fails

A crash-looping Deployment never reaches a verdict. A Job does.

```
oc wait --for=condition=failed job/db-migrate-broken --timeout=180s
oc get pods -l job-name=db-migrate-broken   # two Pods, both Error
oc describe job db-migrate-broken           # BackoffLimitExceeded
```

- Both attempts survive, so the first failure is not overwritten by the retry.
- The log says `cannot reach the database` — the actual reason.
- Giving up means somebody gets a clear failure instead of a Pod restarting all night.
- `backoffLimit` counts **retries**, and the delay between them doubles.

---

<!-- id: cronjob -->
## On a schedule

A CronJob creates a Job each time it fires. Test it by hand rather than waiting for 03:00.

```
oc create job report-now --from=cronjob/nightly-report
oc patch cronjob nightly-report -p '{"spec":{"suspend":true}}' --type=merge
```

- `--from=cronjob/…` copies the real `jobTemplate`, so you test what will actually run.
- `concurrencyPolicy: Forbid` — skip a run if the last one is still going.
- History limits keep finished Jobs around to inspect.
- `suspend` pauses without deleting — but **missed runs are not caught up**.

---

<!-- id: helpers -->
## Helpers in the same Pod

Both are declared under `initContainers`. One line separates them.

```
initContainers:
- name: setup                    # runs to completion, app waits
- name: heartbeat
  restartPolicy: Always          # sidecar: keeps running beside the app
```

- **Init** — the app cannot start correctly without this first. Fails → the app never starts.
- **Sidecar** — the app neither knows nor cares. Logs, metrics, proxying.
- Declared as init containers because that gives **ordering**: started before the app, stopped after it.
- They share a volume with the app: the app reads a file from a container that already exited.
- Every container draws its own requests and limits from the namespace budget.

---

<!-- id: next -->
## What's next

You can now run work that ends, schedule it, and put helpers beside your app.

**Next lab — Resilience & Scheduling:** PodDisruptionBudgets that survive a node drain, graceful shutdown when the platform sends SIGTERM, and spreading replicas so one node's failure is not your outage.

Digital Container Service · DCS Academy
