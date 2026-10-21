---
title: A Job That Finishes
---

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/job
```

## Read it first

```editor:open-file
file: ~/exercises/job-migrate.yaml
```

Three fields are worth knowing before you run it:

- **`restartPolicy: Never`** makes a failed attempt a **new Pod**, so each attempt keeps its
  own logs. `OnFailure` restarts the container in place and overwrites them.
- **`backoffLimit: 2`** retries twice, then marks the Job `Failed`.
- **`ttlSecondsAfterFinished: 600`** deletes the finished Job after ten minutes, so completed
  Jobs do not accumulate.

## Run it

```terminal:execute
command: envsubst < job-migrate.yaml | oc apply -f - && oc wait --for=condition=complete job/db-migrate --timeout=120s
```

```section:begin
name: breakdown-run-job
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < job-migrate.yaml`** — reads the file and replaces each `${VAR}` placeholder (here the Harbor registry, `${DCS_REGISTRY}`) with the value from your session, so the registry host is never hard-coded.
- **`| oc apply -f -`** — the pipe passes that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc wait --for=condition=complete job/db-migrate --timeout=120s`** — blocks until the Job reports the `Complete` condition, or fails after 120 seconds.

```section:end
name: breakdown-run-job
```

`oc wait` blocks until the Job reports the `complete` condition, which is how to wait for
work whose duration you do not control.

```examiner:execute-test
name: verify-job-completed
title: Verify the db-migrate Job completed successfully
timeout: 60
retries: .INF
delay: 3
```

## What it left behind

```terminal:execute
command: oc get jobs && oc get pods -l job-name=db-migrate
```

```section:begin
name: breakdown-job-and-pod
prefix: Breakdown
title: What each part of the command does
```

- **`oc get jobs`** — lists the Jobs, with their `COMPLETIONS` column.
- **`&&`** — run the next command only if the first one succeeded.
- **`oc get pods -l job-name=db-migrate`** — lists the Pods with the label `job-name=db-migrate`, which the Job controller adds to every Pod it creates. You do not need to know the Pod's generated name.

```section:end
name: breakdown-job-and-pod
```

Two things to notice:

- the Job reports **`COMPLETIONS 1/1`**;
- its Pod is still listed, with status **`Completed`**. The Job keeps it so you can read its
  logs.

The Pod stays as a record of the run; a Deployment would have replaced it.

## Read the output

```terminal:execute
command: oc logs job/db-migrate
```

```examiner:execute-test
name: verify-job-logs
title: Verify the Job's output shows the migration finished
timeout: 30
retries: .INF
delay: 3
```

`oc logs job/<name>` reads the logs of the Job's Pod without you having to look up its
generated name.

{{< note >}}
**💡 Tip:** a Job can also run **several** Pods. `completions` says how many must succeed
and `parallelism` how many may run at once, which turns a Job into a small batch worker.
{{< /note >}}

Next, make one fail.
