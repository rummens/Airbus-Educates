---
title: Where Logs Live
---

A container has no log file to configure. It writes to **stdout** and **stderr**, and the
platform takes it from there.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/where
```

![A container writes to stdout; the runtime writes that to a file on the node, which oc logs reads and which rotation eventually discards; a collector ships the same lines to the platform's log store, which outlives the Pod](log-path.svg)

## The path

1. Your process writes a line to **stdout**.
2. The **container runtime** on that node captures it and writes it to a file on the node.
3. **`oc logs`** reads that file, through the API.
4. A **collector** also reads it, and ships it to the platform's log store.

Two consequences follow, and they explain most log surprises:

- **`oc logs` is reading a file on a node.** That file is rotated when it gets big, and it
  disappears with the Pod.
- **Nothing parses your lines** on the way. Whatever structure your logs have is the structure
  you gave them.

{{< note >}}
**💡 Tip:** do not write logs to a file inside the container. Nothing collects it, it fills
the container's disk, and it is gone with the Pod. Write to standard output instead.
{{< /note >}}

## Deploy something that logs

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
```

```section:begin
name: breakdown-deploy-app
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with its value from your session, so the registry host is not hard-coded.
- **`| oc apply -f -`** — the pipe hands that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — runs the next command only if the one before it succeeded.
- **`oc rollout status deploy/hello-dcs --timeout=180s`** — waits until the Deployment's Pods are ready, or gives up after 180 seconds.

```section:end
name: breakdown-deploy-app
```

```examiner:execute-test
name: verify-app-ready
title: Verify the app is running with two replicas
timeout: 90
retries: .INF
delay: 3
```

## Generate some log lines

```terminal:execute
command: |-
  url="http://hello-dcs.$(oc project -q).svc:8080"
  oc apply -f service.yaml 2>/dev/null || true
  for i in $(seq 1 20); do curl -s -o /dev/null "$url" 2>/dev/null; done
  echo "sent 20 requests"
```

```section:begin
name: breakdown-send-requests
prefix: Breakdown
title: What each part of the command does
```

- **`url="http://hello-dcs.$(oc project -q).svc:8080"`** — stores the Service's in-cluster address in the variable `url`; `$(oc project -q)` inserts your namespace name.
- **`oc apply -f service.yaml 2>/dev/null || true`** — creates the Service; `2>/dev/null` hides any error message, and `|| true` lets the step carry on even if the apply fails.
- **`for i in $(seq 1 20); do … done`** — `seq 1 20` prints the numbers 1 to 20, so the loop body runs 20 times.
- **`curl -s -o /dev/null "$url" 2>/dev/null`** — sends one request and throws away the response and any error, so the loop keeps going if the app is not reachable yet.
- **`echo "sent 20 requests"`** — prints a confirmation when the loop is done.

```section:end
name: breakdown-send-requests
```

If that could not reach the app yet, it does not matter. The app logs its own startup
either way, which is enough for the next page.
