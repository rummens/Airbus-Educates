---
title: Survive a Restart
---

Now the test that matters. Delete replica 0 outright and see **what comes back**.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/restart
```

## Note what you are about to lose

```terminal:execute
command: oc get pod hello-dcs-0 -o custom-columns=NAME:.metadata.name,UID:.metadata.uid,IP:.status.podIP,NODE:.spec.nodeName
```

The **UID** is the Pod's unique identity to the cluster. The Pod that comes back will have a
different UID — it really is a new Pod, not the same one restarted.

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
`hello-dcs-0` again — same name, same ordinal, same DNS record.

## And the data?

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

`written by hello-dcs-0` — the marker from the last page, on a Pod that did not exist when it
was written.

Nothing restored it. The claim `data-hello-dcs-0` was never deleted; the new `hello-dcs-0`
simply got the same claim back, because the claim belongs to the **ordinal**, not to the Pod.

{{< note >}}
**📌 Note:** `oc get pvc` looks exactly the same as before. That is the point — the Pod churned,
the storage did not.
{{< /note >}}

## What this buys an app

A database replica can keep its data directory, its identity in the cluster, and its place in
the replication topology across a restart, a node drain or an upgrade.

Those are the guarantees you would otherwise have to fake with careful naming and hope.

Next: what happens when you scale down.
