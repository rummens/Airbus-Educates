---
title: Diagnose It
---

Three lenses tell you almost everything about a misbehaving workload. Use them in order —
each narrows the problem. The rule of thumb: **read the console before you rebuild the
machine.**

## 1. Describe the Pod — its status and events

`oc describe` ends with an **Events** list: the play-by-play of what the platform tried
and what failed.

```terminal:execute
command: oc describe pod -l app=hello-dcs | tail -n 30
```

Look for a line naming what's missing. Here you'll see the container can't be configured
because a **ConfigMap it references doesn't exist** — the name it's looking for is
`hello-dcs-conf`.

## 2. Cluster events — the same story, cluster-wide

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
command: oc logs -l app=hello-dcs --tail=20 || echo "(no logs: the container never started — consistent with a config error before startup)"
```

For a crash *after* startup you'd add `--previous` to read the dead container's logs. Here
there are none, which is itself a clue: the failure is **before** the app runs, so it's
configuration, not code.

## The diagnosis

The manifest's `envFrom` points at `hello-dcs-conf`, but the real ConfigMap is
`hello-dcs-config`. One character off. Next page: fix it and confirm recovery.
