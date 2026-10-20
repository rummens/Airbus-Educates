---
title: Put It Under Load
---

Now make the app work for its living. The workshop image ships a small load tool, `ab`
(ApacheBench) — one process, many requests in flight, connections reused. That is enough to
push a 100m CPU request past its 50% target.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/load
```

## Watch first

In the **lower** pane, watch the HPA and the Pods together. `timeout 240` stops the watch by
itself, so nothing is left running:

```terminal:execute
command: timeout 240 sh -c 'while true; do date +%T; oc get hpa hello-dcs --no-headers; oc get pods -l app=hello-dcs --no-headers | wc -l | sed "s/^/pods: /"; echo; sleep 10; done'
session: 2
```

## Drive the load

In the **upper** pane, run a two-minute burst of traffic with `ab`:

```terminal:execute
command: ab -t 120 -c 16 "http://hello-dcs.$(oc project -q).svc:8080/"
session: 1
```

What that does:

- **`ab`** — sends plain HTTP GET requests in a steady stream and prints a summary when it
  stops.
- **`-t 120`** — run for two minutes, then stop by itself. Nothing is left running.
- **`-c 16`** — sixteen requests in flight at once, over reused connections.
- **the URL** — the Service address in this namespace; `ab` resolves the name once, at
  start.

Why a load tool instead of eight `curl` loops: every `curl` is a new process and a fresh
DNS lookup, and that per-request overhead can keep your terminal container busier than the
app it is attacking. One `ab` process with reused connections puts the work where it
belongs — on the app.

While `ab` runs, its progress lines show the request rate. In the lower pane you should
see TARGETS climb well past `50%`, then the Pod count rise — 2, then 3, then more.

{{< note >}}
**⏳ This takes a moment:** the HPA samples metrics every 15 seconds and scales out at most
once per interval. Expect the first extra Pod after roughly half a minute of load.
{{< /note >}}

```examiner:execute-test
name: verify-hpa-scaled-up
title: Verify the HPA scaled the Deployment above its minimum
timeout: 150
retries: .INF
delay: 5
```

## What just happened

Nobody ran `oc scale`. The HPA wrote a new replica count onto the Deployment, and everything
after that was the ordinary Deployment behaviour from the earlier labs: a new ReplicaSet
Pod, a readiness probe, a Service endpoint.

```terminal:execute
command: oc describe hpa hello-dcs
```

Read the **Events** at the bottom: each scale decision is recorded with the metric that
triggered it, like `New size: 3; reason: cpu resource utilization (percentage of request) above target`.

```examiner:execute-test
name: verify-hpa-scale-event
title: Verify the HPA recorded a scaling event with its reason
timeout: 150
retries: .INF
delay: 3
```

That event trail is the first thing to read when an HPA does something surprising.
