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

In the **upper** pane, send ten requests, one per second:

```terminal:execute
command: |-
  url="http://hello-dcs.$(oc project -q).svc:8080"
  for i in $(seq 1 10); do curl -s -o /dev/null "$url"; sleep 1; done
  echo "done"
```

New lines appear in the lower pane as the requests arrive. `-f` behaves like `tail -f`, and
it stops when the Pod does.
