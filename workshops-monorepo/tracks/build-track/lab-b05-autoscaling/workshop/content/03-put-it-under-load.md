---
title: Put It Under Load
---

Next, put the app under load. The workshop image includes `ab` (ApacheBench), a load tool
that sends many requests at once from one process over reused connections. That is enough to
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

```section:begin
name: breakdown-watch-hpa
prefix: Breakdown
title: What each part of the command does
```

- **`timeout 240`** — stops everything after four minutes.
- **`sh -c '…'`** — runs the quoted loop in its own small shell, so `timeout` can stop all of it at once.
- **`while true; do` … `done`** — repeats the commands in between until `timeout` stops it.
- **`date +%T`** — prints the time, so you can see when each change happened.
- **`oc get hpa hello-dcs --no-headers`** — one line with the current and target CPU and the replica numbers, without the column titles.
- **`oc get pods -l app=hello-dcs --no-headers | wc -l`** — counts the app's Pods: one line per Pod, and `wc -l` counts the lines.
- **`| sed "s/^/pods: /"`** — puts `pods: ` in front of that count.
- **`echo`** — prints a blank line between samples.
- **`sleep 10`** — waits ten seconds before the next sample.

```section:end
name: breakdown-watch-hpa
```

## Drive the load

In the **upper** pane, run a two-minute burst of traffic with `ab`:

```terminal:execute
command: ab -t 120 -c 16 "http://hello-dcs.$(oc project -q).svc:8080/"
session: 1
```

```section:begin
name: breakdown-load-test
prefix: Breakdown
title: What each part of the command does
```

- **`ab`** — sends plain HTTP GET requests in a steady stream and prints a summary when it stops.
- **`-t 120`** — runs for two minutes, then stops by itself, so nothing is left running.
- **`-c 16`** — keeps sixteen requests in flight at once, over reused connections.
- **`"http://hello-dcs.$(oc project -q).svc:8080/"`** — the Service address in this namespace. `$(oc project -q)` is replaced by your namespace name, and `ab` resolves the name once, at start.

```section:end
name: breakdown-load-test
```

Why a load tool instead of eight `curl` loops: every `curl` is a new process and a fresh
DNS lookup, and that per-request overhead can keep your terminal container busier than the
app it is testing. One `ab` process with reused connections keeps the load on the app, not
on your terminal.

While `ab` runs, its progress lines show the request rate. In the lower pane you should
see TARGETS climb well past `50%`, then the Pod count rise: 2, then 3, then more.

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
