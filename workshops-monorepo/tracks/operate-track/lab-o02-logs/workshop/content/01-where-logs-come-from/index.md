---
title: Where Logs Actually Live
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

Two consequences follow, and they explain nearly every surprise people have with logs:

- **`oc logs` is reading a file on a node.** That file is rotated when it gets big, and it
  disappears with the Pod.
- **Nothing is parsing your lines** on the way. Whatever structure your logs have is the
  structure you gave them.

{{< note >}}
**💡 Tip:** do not write logs to a file inside the container. Nothing collects it, it fills
the container's disk, and it is gone with the Pod. Standard output is the interface.
{{< /note >}}

## Deploy something that logs

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
```

```examiner:execute-test
name: verify-app-ready
title: Verify the app is running with two replicas
timeout: 90
retries: .INF
delay: 3
```

## Give it something to say

```terminal:execute
command: |-
  url="http://hello-dcs.$(oc project -q).svc:8080"
  oc apply -f service.yaml 2>/dev/null || true
  for i in $(seq 1 20); do curl -s -o /dev/null "$url" 2>/dev/null; done
  echo "sent 20 requests"
```

If that could not reach the app yet, it does not matter — the app logs its own startup either
way, which is enough for the next page.
