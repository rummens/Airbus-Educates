---
title: Diagnose It
---

Three commands tell you almost everything about a misbehaving workload. Use them in order —
each one narrows the problem. The general rule: read what the platform is reporting before
you change anything.

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
command: oc describe pod $(oc get pod -l app=hello-dcs --sort-by=.metadata.creationTimestamp -o name | tail -1) | tail -n 30
```

Look for a line naming what's missing. Here you'll see the container can't be configured
because a **ConfigMap it references doesn't exist** — the name it's looking for is
`hello-dcs-conf`.

## 2. Cluster events — the same story, cluster-wide

This lists events for the whole namespace. `--sort-by=.lastTimestamp` orders them oldest to
newest, and `| tail -n 15` keeps the **15 most recent** so the latest problem is at the
bottom:

```terminal:execute
command: oc get events --sort-by=.lastTimestamp | tail -n 15
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

That is not a broken command: it is the clue. There are no logs *because the container
never started*, and the message names the reason — the container's **config** could not be
built. The failure is **before** the app runs, which means configuration, not code. (For a
crash *after* startup you'd add `--previous` to read the dead container's logs; here there
is nothing to read.)

## The diagnosis

The manifest's `envFrom` points at `hello-dcs-conf`, but the real ConfigMap is
`hello-dcs-config`. One character off. Next page: fix it and confirm recovery.
