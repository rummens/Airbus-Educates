---
title: Build One
---

A StatefulSet needs a **headless Service** first — that is what gives each Pod a DNS name.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/build
```

## The headless Service

```editor:open-file
file: ~/exercises/service-headless.yaml
```

`clusterIP: None`, exactly as in the **Services & Cluster Networking** lab. The StatefulSet
will point at it by name through `spec.serviceName`.

```terminal:execute
command: oc apply -f service-headless.yaml
```

```examiner:execute-test
name: verify-headless-service
title: Verify the headless Service exists with no cluster IP
timeout: 15
retries: .INF
delay: 2
```

## The StatefulSet

```editor:open-file
file: ~/exercises/statefulset.yaml
```

Three fields do the work that a Deployment has no equivalent for:

- **`serviceName: hello-dcs`** — where the per-Pod DNS names come from.
- **`volumeClaimTemplates`** — a claim **per replica**, not one shared volume.
- **`replicas: 2`** — created in order, `hello-dcs-0` before `hello-dcs-1`.

Watch the Pods appear in the **lower** pane before you apply it:

```terminal:execute
command: timeout 180 oc get pods -l app=hello-dcs --watch
session: 2
```

Now apply it in the **upper** pane:

```terminal:execute
command: envsubst < statefulset.yaml | oc apply -f - && oc rollout status statefulset/hello-dcs --timeout=180s
```

In the lower pane, notice what you do **not** see: both Pods starting at once.
`hello-dcs-0` reaches Ready first, and only then is `hello-dcs-1` created.

```examiner:execute-test
name: verify-statefulset-ready
title: Verify both StatefulSet replicas are ready, in ordinal order
timeout: 60
retries: .INF
delay: 3
```

{{< note >}}
**⏳ This takes a moment:** the ordering is why this is slower than a Deployment of two. Each
volume is provisioned and each Pod becomes Ready before the next one starts.
{{< /note >}}

## Look at the names

```terminal:execute
command: oc get pods -l app=hello-dcs -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
```

`hello-dcs-0` and `hello-dcs-1` — **ordinals**, not the random suffixes a Deployment's
ReplicaSet generates.

## One volume each

```terminal:execute
command: oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,CAPACITY:.status.capacity.storage,CLASS:.spec.storageClassName
```

Two claims, created from the one template:

- **`data-hello-dcs-0`** — replica 0's own disk.
- **`data-hello-dcs-1`** — replica 1's own disk.

The name is `<template>-<statefulset>-<ordinal>`, which is how each claim finds its way back
to the same replica.

```examiner:execute-test
name: verify-pvc-per-replica
title: Verify one bound PersistentVolumeClaim exists per replica
timeout: 30
retries: .INF
delay: 3
```

Next: prove the identity is real.
