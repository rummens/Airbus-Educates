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

- **`restartPolicy: Never`** — a failed attempt becomes a **new Pod**, so each attempt keeps
  its own logs. `OnFailure` restarts the container in place and overwrites them.
- **`backoffLimit: 2`** — retry twice, then mark the Job `Failed`.
- **`ttlSecondsAfterFinished: 600`** — the finished Job deletes itself after ten minutes, so
  completed Jobs do not accumulate.

## Run it

```terminal:execute
command: envsubst < job-migrate.yaml | oc apply -f - && oc wait --for=condition=complete job/db-migrate --timeout=120s
```

`oc wait` blocks until the Job reports the `complete` condition — which is the honest way to
wait for work whose duration you do not control.

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

Two things to notice:

- the Job reports **`COMPLETIONS 1/1`**;
- its Pod is still listed, with status **`Completed`** — not running, not restarted, kept so
  you can read it.

That Pod is the record of the work. A Deployment would have replaced it.

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

`oc logs job/<name>` reads the logs of the Job's Pod without you having to find its generated
name first.

{{< note >}}
**💡 Tip:** a Job can also run **several** Pods — `completions` says how many must succeed and
`parallelism` how many may run at once. Together they turn a Job into a small batch worker.
{{< /note >}}

Next: make one fail.
