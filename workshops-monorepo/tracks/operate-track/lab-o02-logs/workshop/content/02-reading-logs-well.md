---
title: Reading Logs With Intent
---

`oc logs <pod>` prints everything a container has said since it started, which on a busy app
is unreadable. The flags are what make it useful.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/reading
```

## Target a workload, not a Pod name

You rarely know a Pod's generated name, and it changes. Use the Deployment:

```terminal:execute
command: oc logs deploy/hello-dcs --tail=20
```

```examiner:execute-test
name: verify-logs-readable
title: Verify you can read the app's logs through its Deployment
timeout: 60
retries: .INF
delay: 3
```

- **`deploy/hello-dcs`** lets `oc` pick a Pod from the Deployment for you.
- **`--tail=20`** returns the last 20 lines instead of everything.

{{< warning >}}
**⚠️ Watch out:** `deploy/…` reads **one** Pod, not all of them. With two replicas you see
only one Pod's lines, which the label selector below fixes.
{{< /warning >}}

## Read every replica

```terminal:execute
command: oc logs -l app=hello-dcs --tail=5 --prefix
```

```examiner:execute-test
name: verify-logs-all-replicas
title: Verify logs from more than one replica can be read at once
timeout: 60
retries: .INF
delay: 3
```

- **`-l app=hello-dcs`** reads every Pod matching the label.
- **`--prefix`** puts the Pod name in front of each line, which is the only way to tell two
  replicas apart.

## Bound it by time

```terminal:execute
command: oc logs -l app=hello-dcs --since=5m --tail=50 --prefix
```

```examiner:execute-test
name: verify-logs-since
title: Verify a time-bounded log read works
timeout: 60
retries: .INF
delay: 3
```

`--since=5m` limits the output to the last five minutes, which is what you need during an
incident.

## Follow it live

In the **lower** pane, watch the log as it happens. `timeout 30` ends it by itself:

```terminal:execute
command: timeout 30 oc logs -f deploy/hello-dcs --tail=5
session: 2
```

```section:begin
name: breakdown-follow-logs
prefix: Breakdown
title: What each part of the command does
```

- **`timeout 30`** — runs the command that follows and stops it after 30 seconds, so the pane is free again without you pressing Ctrl+C.
- **`oc logs -f deploy/hello-dcs`** — streams the log of one of the Deployment's Pods as new lines arrive.
- **`--tail=5`** — starts with only the last 5 existing lines.

```section:end
name: breakdown-follow-logs
```

In the **upper** pane, send ten requests, one per second:

```terminal:execute
command: |-
  url="http://hello-dcs.$(oc project -q).svc:8080"
  for i in $(seq 1 10); do curl -s -o /dev/null "$url"; sleep 1; done
  echo "done"
```

```section:begin
name: breakdown-send-slow-requests
prefix: Breakdown
title: What each part of the command does
```

- **`url="http://hello-dcs.$(oc project -q).svc:8080"`** — stores the Service's in-cluster address in the variable `url`; `$(oc project -q)` inserts your namespace name.
- **`for i in $(seq 1 10); do … done`** — `seq 1 10` prints the numbers 1 to 10, so the loop body runs 10 times.
- **`curl -s -o /dev/null "$url"`** — sends one request and throws the response away.
- **`sleep 1`** — waits one second between requests, so you can watch the lines arrive one by one in the lower pane.
- **`echo "done"`** — prints a confirmation when the loop is done.

```section:end
name: breakdown-send-slow-requests
```

New lines appear in the lower pane as the requests arrive. `-f` behaves like `tail -f`, and
it stops when the Pod does.
