---
title: Survive a Restart
---

Delete replica 0 outright, and read **what comes back**.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/restart
```

## Record the Pod's identity

```terminal:execute
command: oc get pod hello-dcs-0 -o custom-columns=NAME:.metadata.name,UID:.metadata.uid,IP:.status.podIP,NODE:.spec.nodeName
```

```section:begin
name: breakdown-pod-identity
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pod hello-dcs-0`** — shows only replica 0.
- **`-o custom-columns=`** — prints a table with the columns you name instead of the default ones. Each column is written `TITLE:field-path`, separated by commas.
- **`NAME:.metadata.name`** — the Pod's name.
- **`UID:.metadata.uid`** — the unique ID the cluster gave this Pod object.
- **`IP:.status.podIP`** — the Pod's current IP address.
- **`NODE:.spec.nodeName`** — the node it runs on.

```section:end
name: breakdown-pod-identity
```

The **UID** is the Pod's unique identity to the cluster. The Pod that comes back will have
a different UID, so it is a new Pod rather than the same one restarted.

## Watch, then delete

In the **lower** pane:

```terminal:execute
command: timeout 120 oc get pods -l app=hello-dcs --watch
session: 2
```

```section:begin
name: breakdown-watch-pods
prefix: Breakdown
title: What each part of the command does
```

- **`timeout 120`** — stops the command after 120 seconds, so the lower pane is free again without pressing Ctrl+C.
- **`oc get pods -l app=hello-dcs`** — lists only the Pods with the label `app=hello-dcs`.
- **`--watch`** — keeps running and prints a new line each time one of those Pods changes.

```section:end
name: breakdown-watch-pods
```

In the **upper** pane:

```terminal:execute
command: oc delete pod hello-dcs-0 && oc rollout status statefulset/hello-dcs --timeout=120s
```

```section:begin
name: breakdown-delete-replica
prefix: Breakdown
title: What each part of the command does
```

- **`oc delete pod hello-dcs-0`** — deletes replica 0; the StatefulSet creates a replacement.
- **`&&`** — run the next command only if the delete succeeded.
- **`oc rollout status statefulset/hello-dcs --timeout=120s`** — waits until the StatefulSet has all its replicas ready again, or gives up after 120 seconds.

```section:end
name: breakdown-delete-replica
```

```examiner:execute-test
name: verify-identity-after-restart
title: Verify the replacement Pod has the same name and a new UID
timeout: 60
retries: .INF
delay: 3
```

A Deployment would have created `hello-dcs-<newhash>-<newsuffix>`. Here the replacement is
`hello-dcs-0` again, with the same ordinal and the same DNS record.

## Check the data

```terminal:execute
command: oc exec hello-dcs-0 -- cat /opt/app-root/src/data/owner.txt
```

```examiner:execute-test
name: verify-data-after-restart
title: Verify the replacement Pod re-attached the same volume, with its data
timeout: 30
retries: .INF
delay: 3
```

`written by hello-dcs-0`, which is the marker from the last page, on a Pod that did not
exist when it was written.

No restore step ran. The claim `data-hello-dcs-0` was never deleted, and the new
`hello-dcs-0` got the same claim back, because the claim belongs to the **ordinal** rather
than to the Pod.

{{< note >}}
**📌 Note:** `oc get pvc` shows the same claims as before. The Pod was replaced, but the data
on the volume is still there.
{{< /note >}}

## What this buys an app

A database replica can keep its data directory, its identity in the cluster, and its place in
the replication topology across a restart, a node drain or an upgrade.

Without a StatefulSet you would have to build these guarantees yourself.

Next: what happens when you scale down.
