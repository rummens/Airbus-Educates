---
title: Summary
---

Four shapes a Deployment cannot express, all of them ordinary once you have run them.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Ran** a Job to completion and read its output from the Pod it kept.
2. **Failed** a Job on purpose and watched it reach a verdict after `backoffLimit` retries,
   with both attempts preserved for inspection.
3. **Created** a CronJob, **triggered** it by hand with `--from=cronjob/…`, and **suspended**
   it without deleting anything.
4. **Ran** an init container to completion before the app started, and a **sidecar** alongside
   it — separated by one line, `restartPolicy: Always`.
5. **Read**, from the app container, a file written by a container that had already exited.

## Check Your Understanding

1. Why is a Deployment the wrong object for a database migration?

{{< note >}}
**❓ Answer:** a successful migration **exits 0**, and a Deployment's job is to restart a
container that exits — so it would run the migration again, forever. A Job expects the Pod to
end and records whether it succeeded.
{{< /note >}}

2. A Job's Pod fails. What decides whether it is retried, and what happens when the retries
   run out?

{{< note >}}
**❓ Answer:** `backoffLimit` decides how many **retries** (with a doubling delay). When they
run out the Job is marked `Failed` with a `BackoffLimitExceeded` event, and it stops — unlike
a crash-looping Deployment, which never reaches a verdict.
{{< /note >}}

3. What is the difference between an init container and a native sidecar?

{{< note >}}
**❓ Answer:** one line — `restartPolicy: Always`. Both are declared under `initContainers`, so
both are ordered relative to the app container; without that field the container must
**finish** before the app starts, with it the container **keeps running** beside the app (and
is stopped after it).
{{< /note >}}

4. Your CronJob was suspended for two days. What happens to the runs it missed when you
   resume it?

{{< note >}}
**❓ Answer:** nothing — they are gone. A schedule is not a queue; resuming only means the
**next** scheduled time will fire. Work that must happen eventually needs a queue, or a run
triggered by hand with `oc create job --from=cronjob/…`.
{{< /note >}}

## Next Steps

**Resilience & Scheduling** is the last lab in this track: PodDisruptionBudgets that survive a
node drain, graceful shutdown when the platform sends `SIGTERM`, and spreading replicas so one
node's failure is not your outage.
