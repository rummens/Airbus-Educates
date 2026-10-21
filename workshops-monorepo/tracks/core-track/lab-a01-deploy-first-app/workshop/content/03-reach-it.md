---
title: Reach It
---

Your app is running, but nothing outside the cluster can talk to it yet.

For a quick local test, open a **tunnel** from your terminal straight to the Pod with
[`oc port-forward`](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/nodes/working-with-containers#nodes-containers-port-forwarding).
It needs no public address.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/reach
```

{{< note >}}
**📌 Note:** this is a *local* tunnel — only for you, only while the command runs. It is
not real exposure.

**Expose Your App** gives the app a proper external address (a **Route**).
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

```section:begin
name: breakdown-open-tunnel
prefix: Breakdown
title: What each part of the command does
```

- **`oc rollout status deploy/hello-dcs --timeout=60s`** — waits until the app is Ready,
  for at most 60 seconds, so the tunnel has a Pod to connect to.
- **`kill "$(cat /tmp/pf.pid 2>/dev/null)"`** — `$(…)` reads the process ID that an earlier
  run saved, and `kill` stops that old tunnel.
- **`2>/dev/null || true`** — hides the error when there is no old tunnel, and `|| true`
  lets the block carry on anyway.
- **`oc port-forward deploy/hello-dcs 8080:8080`** — opens the tunnel: port 8080 in your
  session forwards to port 8080 of a Pod in the Deployment.
- **`>/tmp/pf.log 2>&1`** — writes the tunnel's output and error messages to a log file,
  so they do not fill the pane.
- **`&`** — runs the tunnel in the background, so the pane stays free for other commands.
- **`echo $! > /tmp/pf.pid`** — `$!` is the process ID of the background tunnel; saving it
  lets the next run stop this tunnel.
- **`sleep 2 && echo "port-forward ready on localhost:8080"`** — waits two seconds for the
  tunnel to open, then (`&&`: only if the wait succeeded) prints a ready message.

```section:end
name: breakdown-open-tunnel
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

You should see your greeting in the plain-text response: `Hello from the DCS Academy`.

The app reads `GREETING` at request time, so what you set on the last page is what comes
back.

```examiner:execute-test
name: verify-greeting
title: Verify the app serves your greeting
timeout: 10
retries: 3
delay: 2
```
