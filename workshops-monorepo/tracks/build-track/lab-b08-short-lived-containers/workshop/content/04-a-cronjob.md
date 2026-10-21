---
title: On a Schedule
---

A [**CronJob**](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) is a
**Job factory**. Each time the schedule fires it creates a Job, which creates a Pod.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/cronjob
```

## Create it

```editor:open-file
file: ~/exercises/cronjob-report.yaml
```

The schedule is `0 3 * * *`, 03:00 daily, so it will **not** fire while you are here. You
trigger it by hand instead, which is also how you would test a new CronJob before trusting it
overnight.

Three fields control overlapping runs, history and pausing:

- **`concurrencyPolicy: Forbid`** skips the next run if the previous one is still going. The
  alternatives are `Allow`, the default, which permits two runs at once, and `Replace`.
- **`successfulJobsHistoryLimit` / `failedJobsHistoryLimit`** decide how many finished Jobs
  are kept for inspection. The defaults are 3 and 1.
- **`suspend`** pauses the schedule without deleting anything.

```terminal:execute
command: envsubst < cronjob-report.yaml | oc apply -f - && oc get cronjob nightly-report
```

```examiner:execute-test
name: verify-cronjob-created
title: Verify the CronJob exists with its schedule and concurrency policy
timeout: 30
retries: .INF
delay: 3
```

`LAST SCHEDULE` reads `<none>`, because it has never fired.

## Trigger a run by hand

Do not wait until 03:00. Create a Job **from** the CronJob's template:

```terminal:execute
command: oc create job report-now --from=cronjob/nightly-report && oc wait --for=condition=complete job/report-now --timeout=120s
```

`--from=cronjob/<name>` copies the CronJob's `jobTemplate`, so you are testing the **real**
template rather than a copy you wrote by hand.

```examiner:execute-test
name: verify-manual-run-completed
title: Verify the manually triggered run completed
timeout: 60
retries: .INF
delay: 3
```

```terminal:execute
command: oc logs job/report-now
```

```examiner:execute-test
name: verify-report-output
title: Verify the report output came from the CronJob's template
timeout: 30
retries: .INF
delay: 3
```

## Pause it

A CronJob you no longer want firing does not have to be deleted:

```terminal:execute
command: oc patch cronjob nightly-report -p '{"spec":{"suspend":true}}' --type=merge && oc get cronjob nightly-report
```

```examiner:execute-test
name: verify-cronjob-suspended
title: Verify the CronJob is suspended
timeout: 30
retries: .INF
delay: 3
```

`SUSPEND` now reads `True`. The definition, its history and its schedule are all intact, and
it will not fire. Set it back to `false` to resume.

{{< warning >}}
**⚠️ Watch out:** a suspended CronJob does **not** catch up on missed runs when you resume
it. Missed runs are not stored anywhere, so if the work has to happen eventually, track it
some other way.
{{< /warning >}}

Next, the containers that share a Pod with your app.
