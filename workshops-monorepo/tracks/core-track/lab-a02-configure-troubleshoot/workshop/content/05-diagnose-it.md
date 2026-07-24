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
`| tail -n 30` keeps only the **last 30 lines** — where the events are:

```terminal:execute
command: oc describe pod -l app=hello-dcs | tail -n 30
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

You'll likely see **no log lines at all** — and that absence is itself the clue: the
container never started, so the app never got to print anything. The failure is **before**
the app runs, which means configuration, not code. (For a crash *after* startup you'd add
`--previous` to read the dead container's logs; here there's nothing to read.)

## The diagnosis

The manifest's `envFrom` points at `hello-dcs-conf`, but the real ConfigMap is
`hello-dcs-config`. One character off. Next page: fix it and confirm recovery.
