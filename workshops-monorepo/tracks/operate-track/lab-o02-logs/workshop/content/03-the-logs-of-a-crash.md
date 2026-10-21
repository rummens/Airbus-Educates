---
title: The Logs of a Crash
---

One flag covers this situation: the container that failed has **already been replaced**, and
the new container's log does not contain the error.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/crash
```

## Deploy something that fails

```editor:open-file
file: ~/exercises/crashing.yaml
```

It logs a startup line, prints a fatal error to **stderr**, and exits non-zero. The
Deployment starts it again.

```terminal:execute
command: envsubst < crashing.yaml | oc apply -f - && sleep 20 && oc get pods -l app=flaky
```

```section:begin
name: breakdown-deploy-flaky
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < crashing.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with its value from your session, so the registry host is not hard-coded.
- **`| oc apply -f -`** — the pipe hands that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — runs the next command only if the one before it succeeded.
- **`sleep 20`** — waits 20 seconds, so the container has time to start, crash and be restarted.
- **`oc get pods -l app=flaky`** — lists the app's Pods, with their `STATUS` and `RESTARTS` columns.

```section:end
name: breakdown-deploy-flaky
```

```examiner:execute-test
name: verify-flaky-restarting
title: Verify the flaky app is crash-looping
timeout: 120
retries: .INF
delay: 5
```

`RESTARTS` climbs, and `STATUS` cycles through `Error` and `CrashLoopBackOff`.

## Read the current container

```terminal:execute
command: oc logs deploy/flaky --tail=10 || true
```

```section:begin
name: breakdown-read-current
prefix: Breakdown
title: What each part of the command does
```

- **`oc logs deploy/flaky --tail=10`** — prints the last 10 lines of the current container in one of the Deployment's Pods.
- **`|| true`** — between restarts there may be no running container to read, so this command can fail. `|| true` keeps the step from being marked as failed.

```section:end
name: breakdown-read-current
```

Depending on when you catch it, you get the new container's few lines, or an error, because
between restarts there is no running container to read.

## Read the one that died

```terminal:execute
command: |-
  pod=$(oc get pods -l app=flaky -o name | head -1)
  oc logs "$pod" --previous --tail=20
```

```section:begin
name: breakdown-read-previous
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pods -l app=flaky -o name`** — lists the app's Pods as `pod/<name>`, one per line.
- **`| head -1`** — keeps only the first one.
- **`pod=$(…)`** — stores that Pod name in the variable `pod`.
- **`oc logs "$pod" --previous --tail=20`** — prints the last 20 lines of that Pod's previous container, the one that crashed.

```section:end
name: breakdown-read-previous
```

```examiner:execute-test
name: verify-previous-logs
title: Verify the previous container's fatal error can be read
timeout: 120
retries: .INF
delay: 5
```

The output contains the fatal error:

```
FATAL: cannot reach the database at db.internal:5432
```

**`--previous`** reads the log of the **last terminated** container in that Pod. That log
usually holds the error, so run it first on a crash-looping Pod.

{{< note >}}
**💡 Tip:** stderr and stdout land in the same stream, so `oc logs` shows them together.
Writing errors to stderr is still worth doing, because the aggregated store keeps the
distinction and so do most log parsers.
{{< /note >}}

## Clean up the noise

```terminal:execute
command: oc delete deploy flaky
```

```examiner:execute-test
name: verify-flaky-gone
title: Verify the crashing workload was removed
timeout: 60
retries: .INF
delay: 3
```

## Where oc logs stops

You just deleted that Deployment. Try to read its logs now:

```terminal:execute
command: oc logs deploy/flaky --previous 2>&1 | tail -2 || true
```

```section:begin
name: breakdown-read-deleted
prefix: Breakdown
title: What each part of the command does
```

- **`oc logs deploy/flaky --previous`** — asks for the previous container's log of a Deployment you have already deleted.
- **`2>&1`** — sends the error message to the same output as normal text, so the pipe passes it on.
- **`| tail -2`** — shows only the last two lines.
- **`|| true`** — the read is expected to fail; this keeps the step from being marked as failed.

```section:end
name: breakdown-read-deleted
```

```examiner:execute-test
name: verify-logs-gone-with-pod
title: Verify the deleted workload's logs are unreachable
timeout: 60
retries: .INF
delay: 3
```

The command returns an error instead of logs: the Pod is gone, and its log file on the node
was deleted with it.

`oc logs` only reads containers that still exist. Anything that crashed last night on a
node that has since been drained is out of reach. The next page covers how the platform
keeps those lines.
