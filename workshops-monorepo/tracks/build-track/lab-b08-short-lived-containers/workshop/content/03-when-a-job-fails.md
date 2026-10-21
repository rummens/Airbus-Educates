---
title: When a Job Fails
---

A Deployment whose container keeps exiting restarts it forever, which shows up as
`CrashLoopBackOff` and never resolves. A Job stops after its retries and reports **`Failed`**.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/fails
```

## Run one that cannot work

```editor:open-file
file: ~/exercises/job-failing.yaml
```

Same shape as before, except that the command writes an error and exits 1, and
`backoffLimit: 1` means **two attempts in total** before it gives up.

```terminal:execute
command: envsubst < job-failing.yaml | oc apply -f - && oc wait --for=condition=failed job/db-migrate-broken --timeout=180s
```

```section:begin
name: breakdown-run-failing-job
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < job-failing.yaml`** — reads the file and replaces each `${VAR}` placeholder (here the Harbor registry, `${DCS_REGISTRY}`) with the value from your session, so the registry host is never hard-coded.
- **`| oc apply -f -`** — the pipe passes that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc wait --for=condition=failed job/db-migrate-broken --timeout=180s`** — blocks until the Job reports the `Failed` condition, or gives up after 180 seconds.

```section:end
name: breakdown-run-failing-job
```

Here you wait for the **`failed`** condition. The Job is expected to fail, so that is the
outcome you are asserting.

```examiner:execute-test
name: verify-job-failed-after-retries
title: Verify the broken Job gave up after its retries
timeout: 120
retries: .INF
delay: 5
```

## Read what it tried

```terminal:execute
command: oc get pods -l job-name=db-migrate-broken
```

**Two Pods**, both `Error`. `restartPolicy: Never` makes each attempt a new Pod, so both
attempts survive for you to inspect and the first failure is not overwritten by the retry.

```terminal:execute
command: oc describe job db-migrate-broken | tail -20
```

```section:begin
name: breakdown-describe-tail
prefix: Breakdown
title: What each part of the command does
```

- **`oc describe job db-migrate-broken`** — prints the Job's settings, status and recent events.
- **`| tail -20`** — keeps only the last 20 lines, where the events are listed.

```section:end
name: breakdown-describe-tail
```

At the bottom, the `BackoffLimitExceeded` event records that the Job stopped, and why.

```examiner:execute-test
name: verify-failed-pods-kept
title: Verify both failed attempts were kept for inspection
timeout: 60
retries: .INF
delay: 3
```

## Read the failure reason

```terminal:execute
command: oc logs job/db-migrate-broken | tail -5
```

```section:begin
name: breakdown-logs-tail
prefix: Breakdown
title: What each part of the command does
```

- **`oc logs job/db-migrate-broken`** — prints the logs of one of the Job's Pods, without you looking up its name.
- **`| tail -5`** — keeps only the last five lines.

```section:end
name: breakdown-logs-tail
```

The log shows `cannot reach the database`, from the attempt that produced it.

A Job that stops is better than one that retries forever:

- somebody gets a clear failure instead of a Pod quietly restarting all night;
- the logs of every attempt are still there;
- the cluster stops spending capacity on work that cannot succeed.

```examiner:execute-test
name: verify-failure-reason-readable
title: Verify the failure reason is readable in the Job's logs
timeout: 30
retries: .INF
delay: 3
```

{{< warning >}}
**⚠️ Watch out:** `backoffLimit` counts **retries**, not total attempts, and the delay
between them doubles (10s, 20s, 40s…). A large limit on a slow-failing Job keeps it alive much
longer than you expect.
{{< /warning >}}

Next, put a Job on a schedule.
