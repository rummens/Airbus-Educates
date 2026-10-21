---
title: Diagnose It
---

Three commands show most of what you need to know about a failing workload. Use them in
order; each one narrows the problem. Read what the platform reports before you change
anything.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/diagnose
```

## 1. Describe the Pod — its status and events

`oc describe` prints a long report about the Pod that ends with an **Events** list: a
step-by-step record of what the platform tried and what failed. The output is long, so
`| tail -n 30` keeps only the **last 30 lines** — where the events are.

One detail matters here: a rolling update keeps the **old, healthy** Pod running while the
new one fails, so `-l app=hello-dcs` would describe both and the failure could scroll past.
The inner command picks the **newest** Pod — the broken one — and describes that:

```terminal:execute
command: oc describe $(oc get pod -l app=hello-dcs --sort-by=.metadata.creationTimestamp -o name | tail -1) | tail -n 30
```

```section:begin
name: breakdown-describe-newest-pod
prefix: Breakdown
title: What each part of the command does
```

- **`oc describe`** — prints the full report for the object named after it (here
  `pod/<name>`), ending with its Events.
- **`$( … )`** — runs the inner command first and puts its output, the name of the newest
  Pod, into the `describe` command.
- **`oc get pod -l app=hello-dcs`** — lists the Pods that carry the label `app=hello-dcs`.
- **`--sort-by=.metadata.creationTimestamp`** — sorts them by creation time, oldest first.
- **`-o name`** — prints each Pod only as `pod/<name>`, with no other columns.
- **`| tail -1`** — keeps the last line: the newest Pod.
- **`| tail -n 30`** — keeps only the last 30 lines of the report, where the Events are.

```section:end
name: breakdown-describe-newest-pod
```

Look for a line naming what's missing. Here you'll see the container can't be configured
because a **ConfigMap it references doesn't exist** — the name it's looking for is
`hello-dcs-conf`.

## 2. Cluster events — the same story, cluster-wide

This lists events for the whole namespace, with the **15 most recent** last, so the latest
problem is at the bottom:

```terminal:execute
command: oc get events --sort-by=.lastTimestamp | tail -n 15
```

```section:begin
name: breakdown-recent-events
prefix: Breakdown
title: What each part of the command does
```

- **`oc get events`** — lists the events recorded in your namespace.
- **`--sort-by=.lastTimestamp`** — sorts them by when each one last happened, oldest first.
- **`| tail -n 15`** — keeps the last 15 lines, so you see the most recent events.

```section:end
name: breakdown-recent-events
```

Events confirm it: a reference to `configmap "hello-dcs-conf" not found`.

```examiner:execute-test
name: verify-root-cause
title: Verify the root-cause signal is visible in the cluster
timeout: 10
retries: .INF
delay: 2
```

## 3. Logs — when the container at least started

```terminal:execute
command: oc logs -l app=hello-dcs --tail=20
```

You get **no log lines** — instead the server answers with something like:

```
Error from server (BadRequest): container "hello-dcs" in pod "hello-dcs-…" is waiting to start: CreateContainerConfigError
```

The command worked. This error message is the clue.

There are no logs *because the container never started*, and the message names the reason:
the container's **config** could not be built.

The failure is **before** the app runs, which means **configuration**, not code.

{{< note >}}
**📌 Note:** for a crash *after* startup you would add `--previous` to read the dead
container's logs. Here there is nothing to read.
{{< /note >}}

## The diagnosis

The manifest's `envFrom` points at `hello-dcs-conf`, but the real ConfigMap is
`hello-dcs-config`: the name is missing its last two letters. The next page fixes it and
confirms recovery.
