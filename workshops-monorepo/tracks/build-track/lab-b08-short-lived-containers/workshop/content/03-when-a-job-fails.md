---
title: When a Job Fails
---

A Deployment whose container keeps exiting will keep restarting it forever —
`CrashLoopBackOff`, and no verdict.

A Job reaches a **verdict**. That is the difference worth seeing.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/fails
```

## Run one that cannot work

```editor:open-file
file: ~/exercises/job-failing.yaml
```

Same shape as before, except the command writes an error and exits 1 — and `backoffLimit: 1`,
so it makes **two attempts in total** before giving up.

```terminal:execute
command: envsubst < job-failing.yaml | oc apply -f - && oc wait --for=condition=failed job/db-migrate-broken --timeout=180s
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

**Two Pods**, both `Error`. Because `restartPolicy: Never` makes each attempt a new Pod, both
attempts survive for you to inspect — the first failure is not overwritten by the retry.

```terminal:execute
command: oc describe job db-migrate-broken | tail -20
```

At the bottom, the `BackoffLimitExceeded` event: the Job is telling you it stopped, and why.

```examiner:execute-test
name: verify-failed-pods-kept
title: Verify both failed attempts were kept for inspection
timeout: 60
retries: .INF
delay: 3
```

## Why this matters

```terminal:execute
command: oc logs job/db-migrate-broken | tail -5
```

`cannot reach the database` — the actual reason, from the attempt that produced it.

A Job that gives up is **better** than one that retries forever:

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
**⚠️ Watch out:** `backoffLimit` counts **retries**, not total attempts, and the delay between
them doubles (10s, 20s, 40s…). A large limit on a slow-failing Job can keep it alive far
longer than you expect.
{{< /warning >}}

Next: put a Job on a schedule.
