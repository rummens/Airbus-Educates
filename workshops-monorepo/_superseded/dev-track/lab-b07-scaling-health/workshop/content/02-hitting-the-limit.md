---
title: Hitting the Limit
---

Your namespace's limits are fully spent — four Pods, each at the default limit, exactly
fill the `medium` budget. Now watch what happens when a change asks for **more** per Pod
instead of relying on the defaults.

## Apply the oversized version

`deployment-oversized.yaml` is the same app, same four replicas, but with explicit
`resources.requests`/`resources.limits` of `700m` CPU and `700Mi` memory per container —
well above the default, and more than your namespace has left on the limit side. Take a
look, then apply it:

```editor:open-file
file: ~/exercises/deployment-oversized.yaml
```

```terminal:execute
command: envsubst < deployment-oversized.yaml | oc apply -f -
```

{{< note >}}
This changes the Deployment's Pod template, so {{< param product_short >}} starts a
rolling update — it tries to create new, bigger Pods alongside the existing ones. Give it a
few seconds; the check below waits for the outcome.
{{< /note >}}

```examiner:execute-test
name: verify-oversized-pending
title: Verify the oversized rollout cannot fully land
timeout: 15
retries: .INF
delay: 2
```

Look at the Pods:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Your four original Pods are still `Running` — but you should also see one or more new Pods
stuck `Pending`, or the rollout simply refusing to progress. Nothing crashed; the new
Pods were never even scheduled.

## Read why

Cluster [events](https://kubernetes.io/docs/concepts/overview/working-with-objects/#object-events)
record what the platform tried and why it failed:

```terminal:execute
command: oc get events --sort-by=.lastTimestamp
```

Look for a `FailedCreate` event naming the ReplicaSet, with a message like:

```
Warning  FailedCreate  replicaset/hello-dcs-7f8b9c6d4  Error creating: pods "hello-dcs-7f8b9c6d4-x2k9p" is
forbidden: exceeded quota: <your-namespace>, requested: limits.cpu=700m,limits.memory=700Mi, used:
limits.cpu=2,limits.memory=2Gi, limited: limits.cpu=2,limits.memory=2Gi
```

(Your exact Pod/ReplicaSet names and the `used`/`limited` figures will differ slightly —
the shape of the message is what matters.) Read it left to right: it **requested** 700m/700Mi
for one more Pod, was already at its **limited** ceiling (2 CPU / 2Gi from page 01), so the
create was refused outright — the Pod was never even scheduled, let alone started.

```examiner:execute-test
name: verify-quota-event-visible
title: Verify the quota-exceeded event is visible in the cluster
timeout: 10
retries: .INF
delay: 2
```

This is the [**ResourceQuota**](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
doing exactly its job: admission control rejecting a request the namespace's budget can't
back, before it ever costs the cluster anything. The fix isn't a bigger namespace — it's a
better-sized Pod. Next page.
