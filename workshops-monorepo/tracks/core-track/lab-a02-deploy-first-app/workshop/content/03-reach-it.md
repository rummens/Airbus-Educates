---
title: Reach It
---

Your app is running, but nothing outside the cluster can talk to it yet. For a quick
local test you can open a **tunnel** from your terminal straight to the Pod with
[`oc port-forward`](https://docs.openshift.com/container-platform/latest/nodes/containers/nodes-containers-port-forwarding.html) —
no public address required.

{{< note >}}
This is a *local* tunnel, just for you, just while the command runs — not real exposure.
Giving the app a proper external address (a **Route**) is the whole point of **A04**.
{{< /note >}}

## Open the tunnel (lower terminal)

Run this in the **lower** terminal pane. It waits for the app to be ready, then starts the
tunnel in the background so the pane stays usable:

```terminal:execute
command: |-
  oc rollout status deploy/hello-dcs --timeout=60s
  kill "$(cat /tmp/pf.pid 2>/dev/null)" 2>/dev/null || true
  oc port-forward deploy/hello-dcs 8080:8080 >/tmp/pf.log 2>&1 &
  echo $! > /tmp/pf.pid
  sleep 2 && echo "port-forward ready on localhost:8080"
session: 2
```

```examiner:execute-test
name: verify-portforward
title: Verify the tunnel reaches the app (HTTP 200)
timeout: 10
retries: .INF
delay: 2
```

## Call it (upper terminal)

Now `curl` the app in the **upper** pane:

```terminal:execute
command: curl -s localhost:8080
```

You should see your greeting — **`Hello from the DCS Academy`** — in the plain-text
response. The app reads `GREETING` at request time, so what you set on the last page is
what comes back.

```examiner:execute-test
name: verify-greeting
title: Verify the app serves your greeting
timeout: 10
```
