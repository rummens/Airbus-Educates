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

The schedule is `0 3 * * *` — 03:00 daily, so it will **not** fire while you are here. That is
deliberate: you are about to trigger it by hand instead, which is also how you would test a
new CronJob before trusting it overnight.

Three fields decide how it behaves when reality gets messy:

- **`concurrencyPolicy: Forbid`** — if the previous run is still going when the next is due,
  **skip** it. The alternatives are `Allow` (the default — two runs at once) and `Replace`.
- **`successfulJobsHistoryLimit` / `failedJobsHistoryLimit`** — how many finished Jobs to keep
  so you can inspect them. Defaults are 3 and 1.
- **`suspend`** — pause the schedule without deleting anything.

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

`LAST SCHEDULE` reads `<none>` — it has never fired.

## Trigger a run by hand

Do not wait until 03:00. Create a Job **from** the CronJob's template:

```terminal:execute
command: oc create job report-now --from=cronjob/nightly-report && oc wait --for=condition=complete job/report-now --timeout=120s
```

`--from=cronjob/<name>` copies the CronJob's `jobTemplate`, so you are testing the **real**
template rather than a lookalike you wrote by hand.

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

`SUSPEND` now reads `True`. The definition, its history and its schedule are all intact — it
simply will not fire. Set it back to `false` to resume.

{{< warning >}}
**⚠️ Watch out:** a suspended CronJob does **not** catch up on missed runs when you resume it.
If the work must happen eventually, a schedule is not a queue.
{{< /warning >}}

Next: the containers that share a Pod with your app.
