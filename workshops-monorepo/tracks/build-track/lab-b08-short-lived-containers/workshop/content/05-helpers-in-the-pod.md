---
title: Helpers in the Same Pod
---

Jobs and CronJobs run **instead of** your app. The last two shapes run **with** it, inside the
same Pod, sharing its network and its volumes.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/helpers
```

## One Pod, three containers

```editor:open-file
file: ~/exercises/deployment-with-helpers.yaml
```

Look at where the three are declared. Two of them, `setup` and `heartbeat`, are both under
**`initContainers`**, and one line separates them:

- **`setup`** has no `restartPolicy`. It is an ordinary **init container**: it runs to
  completion, and only then is the app container started.
- **`heartbeat`** has **`restartPolicy: Always`**, which makes it a **sidecar**: started
  before the app, and kept running beside it for the life of the Pod.

They share an `emptyDir` called `work` with the app container, and a helper passes
files to the app through that shared volume.

## Apply it and watch the order

```terminal:execute
command: envsubst < deployment-with-helpers.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
```

```section:begin
name: breakdown-apply-helpers
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment-with-helpers.yaml`** — reads the file and replaces each `${VAR}` placeholder (here the Harbor registry, `${DCS_REGISTRY}`) with the value from your session, so the registry host is never hard-coded.
- **`| oc apply -f -`** — the pipe passes that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc rollout status deploy/hello-dcs --timeout=180s`** — waits until every replica is ready, or gives up after 180 seconds.

```section:end
name: breakdown-apply-helpers
```

```examiner:execute-test
name: verify-pod-with-helpers-ready
title: Verify the Pod is ready with its helper containers
timeout: 90
retries: .INF
delay: 3
```

## What ran, and in what order

```terminal:execute
command: oc get pods -l app=hello-dcs -o custom-columns=NAME:.metadata.name,READY:.status.containerStatuses[*].ready,INIT:.status.initContainerStatuses[*].name
```

```section:begin
name: breakdown-container-columns
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pods -l app=hello-dcs`** — lists only the Pods with the label `app=hello-dcs`.
- **`-o custom-columns=`** — prints a table with the columns you name instead of the default ones. Each column is written `TITLE:field-path`, separated by commas.
- **`NAME:.metadata.name`** — the Pod's name.
- **`READY:.status.containerStatuses[*].ready`** — `true` or `false` for each regular container; `[*]` means "every item in the list", printed comma-separated.
- **`INIT:.status.initContainerStatuses[*].name`** — the names of the containers declared under `initContainers`, here `setup` and `heartbeat`.

```section:end
name: breakdown-container-columns
```

Now ask the Pod what each container did:

```terminal:execute
command: |-
  pod=$(oc get pod -l app=hello-dcs -o name | head -1)
  echo "--- setup (init container) ---"
  oc logs $pod -c setup
  echo "--- heartbeat (sidecar) ---"
  oc logs $pod -c heartbeat --tail=3
```

```section:begin
name: breakdown-helper-logs
prefix: Breakdown
title: What each part of the command does
```

- **`pod=$(…)`** — runs the command inside `$(…)` and stores its output in the shell variable `pod`, so the next lines can use `$pod`.
- **`oc get pod -l app=hello-dcs -o name`** — lists the app's Pods as `pod/<name>`, a form other `oc` commands accept directly.
- **`| head -1`** — keeps only the first line, so `pod` holds one Pod.
- **`echo "--- … ---"`** — prints a header, so you can tell the two logs apart.
- **`oc logs $pod -c setup`** — prints the logs of the `setup` container; `-c` picks one container in a Pod that has several.
- **`oc logs $pod -c heartbeat --tail=3`** — prints only the last three lines of the sidecar's log.

```section:end
name: breakdown-helper-logs
```

```examiner:execute-test
name: verify-init-completed
title: Verify the init container ran to completion before the app
timeout: 60
retries: .INF
delay: 3
```

The init container's log ends at `setup done` and stops. The sidecar's keeps producing output,
because it is still running.

## Read the shared volume from the app

The init container wrote a file into the shared volume. Read it **from the app container**:

```terminal:execute
command: |-
  pod=$(oc get pod -l app=hello-dcs -o name | head -1)
  oc exec $pod -c hello-dcs -- cat /work/setup.txt
  oc exec $pod -c hello-dcs -- tail -2 /work/heartbeat.log
```

```section:begin
name: breakdown-read-shared-volume
prefix: Breakdown
title: What each part of the command does
```

- **`pod=$(…)`** — runs the command inside `$(…)` and stores its output in the shell variable `pod`, so the next lines can use `$pod`.
- **`oc get pod -l app=hello-dcs -o name`** — lists the app's Pods as `pod/<name>`, a form other `oc` commands accept directly.
- **`| head -1`** — keeps only the first line, so `pod` holds one Pod.
- **`oc exec $pod -c hello-dcs --`** — runs the command after `--` inside the app container, not in one of the helpers.
- **`cat /work/setup.txt`** — prints the file the init container wrote into the shared volume.
- **`tail -2 /work/heartbeat.log`** — prints the last two lines the sidecar has appended so far.

```section:end
name: breakdown-read-shared-volume
```

```examiner:execute-test
name: verify-shared-volume-handoff
title: Verify the app container can read what the helpers wrote
timeout: 60
retries: .INF
delay: 3
```

The app sees a file written by a container that had already **exited** before it started,
and a log still being appended to by one running **next to** it.

```examiner:execute-test
name: verify-sidecar-still-running
title: Verify the sidecar is still running alongside the app
timeout: 60
retries: .INF
delay: 3
```

## When to reach for which

- **Init container:** the app cannot start correctly unless this is done first. Migrations,
  fetching config, waiting for a dependency. If it fails the app never starts, which is
  usually what you want.
- **Sidecar:** the app does not need to know this is happening. Shipping logs, exposing
  metrics, terminating TLS.

{{< warning >}}
**⚠️ Watch out:** every container in the Pod takes its own `requests` and `limits` from the
namespace budget. A Pod with three containers needs three sets of requests and limits, and
a sidecar on fifty replicas adds fifty containers to your quota.
{{< /warning >}}
