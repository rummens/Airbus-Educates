---
title: Build One
---

A StatefulSet needs a **headless Service** first, because that is what gives each Pod a DNS
name.

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

- **`serviceName: hello-dcs`** is where the per-Pod DNS names come from.
- **`volumeClaimTemplates`** creates a claim **per replica**, not one shared volume.
- **`replicas: 2`** are created in order, `hello-dcs-0` before `hello-dcs-1`.

Watch the Pods appear in the **lower** pane before you apply it:

```terminal:execute
command: timeout 180 oc get pods -l app=hello-dcs --watch
session: 2
```

```section:begin
name: breakdown-watch-pods
prefix: Breakdown
title: What each part of the command does
```

- **`timeout 180`** — stops the command after 180 seconds, so the lower pane is free again without pressing Ctrl+C.
- **`oc get pods -l app=hello-dcs`** — lists only the Pods with the label `app=hello-dcs`.
- **`--watch`** — keeps running and prints a new line each time one of those Pods changes.

```section:end
name: breakdown-watch-pods
```

Now apply it in the **upper** pane:

```terminal:execute
command: envsubst < statefulset.yaml | oc apply -f - && oc rollout status statefulset/hello-dcs --timeout=180s
```

```section:begin
name: breakdown-apply-statefulset
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < statefulset.yaml`** — reads the file and replaces each `${VAR}` placeholder (here the Harbor registry, `${DCS_REGISTRY}`) with the value from your session, so the registry host is never hard-coded.
- **`| oc apply -f -`** — the pipe passes that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc rollout status statefulset/hello-dcs --timeout=180s`** — waits until both replicas are ready, one after the other, or gives up after 180 seconds.

```section:end
name: breakdown-apply-statefulset
```

In the lower pane, the two Pods do **not** start together.
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

```section:begin
name: breakdown-pod-names
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pods -l app=hello-dcs`** — lists only the Pods with the label `app=hello-dcs`.
- **`-o custom-columns=`** — prints a table with the columns you name instead of the default ones. Each column is written `TITLE:field-path`, separated by commas.
- **`NAME:.metadata.name`** — the Pod's name.
- **`STATUS:.status.phase`** — the Pod's phase, such as `Running`.
- **`NODE:.spec.nodeName`** — the node the Pod was scheduled on.

```section:end
name: breakdown-pod-names
```

`hello-dcs-0` and `hello-dcs-1`. They are **ordinals**, not the random suffixes a
Deployment's ReplicaSet generates.

## One volume each

```terminal:execute
command: oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,CAPACITY:.status.capacity.storage,CLASS:.spec.storageClassName
```

```section:begin
name: breakdown-claim-columns
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pvc`** — lists the PersistentVolumeClaims in your namespace.
- **`-o custom-columns=`** — prints a table with the columns you name instead of the default ones. Each column is written `TITLE:field-path`, separated by commas.
- **`NAME:.metadata.name`** — the claim's name.
- **`STATUS:.status.phase`** — whether the claim is `Bound` to a volume.
- **`CAPACITY:.status.capacity.storage`** — the size of the volume that was provisioned.
- **`CLASS:.spec.storageClassName`** — the storage class that provided it.

```section:end
name: breakdown-claim-columns
```

Two claims, created from the one template:

- **`data-hello-dcs-0`** is replica 0's own disk.
- **`data-hello-dcs-1`** is replica 1's own disk.

The name is `<template>-<statefulset>-<ordinal>`, which is how each claim finds its way back
to the same replica.

```examiner:execute-test
name: verify-pvc-per-replica
title: Verify one bound PersistentVolumeClaim exists per replica
timeout: 30
retries: .INF
delay: 3
```

Next, check that the identity is real.
