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

The **UID** is the Pod's unique identity to the cluster. The Pod that comes back will have
a different UID, so it is a new Pod rather than the same one restarted.

## Watch, then delete

In the **lower** pane:

```terminal:execute
command: timeout 120 oc get pods -l app=hello-dcs --watch
session: 2
```

In the **upper** pane:

```terminal:execute
command: oc delete pod hello-dcs-0 && oc rollout status statefulset/hello-dcs --timeout=120s
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
