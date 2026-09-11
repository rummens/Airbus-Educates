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

Look at where the three are declared. Two of them — `setup` and `heartbeat` — are both under
**`initContainers`**, and exactly one line separates them:

- **`setup`** has no `restartPolicy`. It is an ordinary **init container**: it runs to
  completion, and only then is the app container started.
- **`heartbeat`** has **`restartPolicy: Always`**. That makes it a **sidecar**: started before
  the app, and kept running beside it for the life of the Pod.

They share an `emptyDir` called `work` with the app container, which is how a helper hands
something to the app: same Pod, same volume.

## Apply it and watch the order

```terminal:execute
command: envsubst < deployment-with-helpers.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
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

Now ask the Pod what each container did:

```terminal:execute
command: |-
  pod=$(oc get pod -l app=hello-dcs -o name | head -1)
  echo "--- setup (init container) ---"
  oc logs $pod -c setup
  echo "--- heartbeat (sidecar) ---"
  oc logs $pod -c heartbeat --tail=3
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

## The proof they shared a Pod

The init container wrote a file into the shared volume. Read it **from the app container**:

```terminal:execute
command: |-
  pod=$(oc get pod -l app=hello-dcs -o name | head -1)
  oc exec $pod -c hello-dcs -- cat /work/setup.txt
  oc exec $pod -c hello-dcs -- tail -2 /work/heartbeat.log
```

```examiner:execute-test
name: verify-shared-volume-handoff
title: Verify the app container can read what the helpers wrote
timeout: 60
retries: .INF
delay: 3
```

The app sees a file written by a container that had already **exited** before it started, and
a log still being appended to by one running **next to** it.

```examiner:execute-test
name: verify-sidecar-still-running
title: Verify the sidecar is still running alongside the app
timeout: 60
retries: .INF
delay: 3
```

## When to reach for which

- **Init container** — the app cannot start correctly without this being done first.
  Migrations, fetching config, waiting for a dependency. If it fails, the app never starts,
  which is usually what you want.
- **Sidecar** — the app should not know or care that this is happening. Shipping logs,
  exposing metrics, terminating TLS.

{{< warning >}}
**⚠️ Watch out:** every container in the Pod draws its own `requests` and `limits` from the
namespace budget. Three containers in one Pod is three sets of numbers — a sidecar on fifty
replicas is fifty more containers to pay for.
{{< /warning >}}
