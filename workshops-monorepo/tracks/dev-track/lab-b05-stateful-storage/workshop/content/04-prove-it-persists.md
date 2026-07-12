---
title: Prove It Persists
---

This is the payoff. Same experiment as page 1 — delete the pod — but this time the data
lives on a PersistentVolume, not inside the container.

## Watch, then restart

Use the **lower** terminal to watch pods and the PVC live while you act in the upper one:

```terminal:execute-2
command: watch -n1 'oc get pods,pvc -l app=hello-dcs'
```

Now, in the upper terminal, delete the running pod. The Deployment will immediately create a
replacement:

```terminal:execute-1
command: oc delete pod -l app=hello-dcs
```

In the lower terminal watch the old pod terminate and a fresh one appear — while the **PVC
stays `Bound` the whole time**. The volume never went anywhere; only the pod was replaced.

```examiner:execute-test
name: verify-pods-running
title: A fresh pod is running after the restart
args:
- hello-dcs
- "1"
timeout: 120
retries: .INF
delay: 3
```

## Read the data back

The new pod is a brand-new container with an empty root filesystem — but it mounted the
**same** PVC at `/data`. Read the marker:

```terminal:execute-1
command: oc exec deployment/hello-dcs -- cat /data/marker
```

```
persisted-by-dcs
```

```examiner:execute-test
name: verify-marker
title: The data survived the pod restart
args:
- hello-dcs
- /data/marker
- persisted-by-dcs
timeout: 15
retries: 5
delay: 3
```

Still there. That's the whole point of persistent storage: the data lives in the
PersistentVolume, not the pod, so it outlives any single container. Stop the watch in the
lower terminal with `Ctrl+C` when you're ready.

## One honest caveat: RWO vs replicas

Your PVC is **ReadWriteOnce** — a single node mounts it read-write at a time. That's fine for
one pod. But if you scale this Deployment to several replicas, they won't all cleanly share
that one volume: pods landing on other nodes can't mount it, and even co-located pods writing
to the same files would corrupt each other's data. A raw PVC does **not** turn a stateless app
into a safely-scaled stateful one.

Real stateful systems — databases, message queues — solve this with an **operator** that gives
each replica its **own** volume and coordinates them (replication, failover, backups). On
{{< param product_short >}} that's the pattern you'll meet in Module F with **CloudNativePG**
for PostgreSQL. So: reach for a PVC to persist one app's data; reach for an operator when you
need stateful data *and* scale.
