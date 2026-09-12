---
title: The Logs of a Crash
---

One flag exists for a single situation: the container that can tell you what went wrong is
**already gone**, replaced by a fresh one that knows nothing.

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

Depending on when you catch it, you get the new container's few lines, or an error, because
between restarts there is no running container to read.

## Read the one that died

```terminal:execute
command: |-
  pod=$(oc get pods -l app=flaky -o name | head -1)
  oc logs "$pod" --previous --tail=20
```

```examiner:execute-test
name: verify-previous-logs
title: Verify the previous container's fatal error can be read
timeout: 120
retries: .INF
delay: 5
```

There it is:

```
FATAL: cannot reach the database at db.internal:5432
```

**`--previous`** reads the log of the **last terminated** container in that Pod. That is
where a crash explains itself, and it is worth reaching for first.

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

```examiner:execute-test
name: verify-logs-gone-with-pod
title: Verify the deleted workload's logs are unreachable
timeout: 60
retries: .INF
delay: 3
```

Nothing. The Pod is gone, the node's file went with it, and `oc logs` has nowhere to look.

**`oc logs` can only tell you about containers that still exist.** Anything that crashed
last night on a node that has since been drained is out of reach.

That is what the next page is about.
