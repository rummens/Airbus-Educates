---
title: Self-Healing
---

Everything so far has been about **shaping** the desired state: replica count, resource
numbers, probes.

This page shows {{< param product_short >}} **enforcing** it. You delete a running Pod by
hand, with no rollout and no manifest change, and watch the platform put one back.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/self-healing
```

## Note the names

```terminal:execute
command: oc get pods -l app=hello-dcs
```

One of those names is about to disappear, and a **new** one will take its place.

## Watch it happen

In the **lower** pane:

```terminal:execute
command: timeout 60 oc get pods -l app=hello-dcs --watch
session: 2
```

```section:begin
name: breakdown-watch-pods
prefix: Breakdown
title: What each part of the command does
```

- **`timeout 60`** — stops the command after 60 seconds, so nothing is left running in the pane.
- **`oc get pods`** — lists Pods.
- **`-l app=hello-dcs`** — shows only Pods with the label `app=hello-dcs`.
- **`--watch`** — keeps the command running and prints a new line each time a Pod changes.

```section:end
name: breakdown-watch-pods
```

## Delete one Pod

In the **upper** pane, pick exactly one running Pod and delete it:

```terminal:execute
command: |-
  oc get pods -l app=hello-dcs -o name | head -n 1 > /tmp/deleted-pod.txt
  oc delete "$(cat /tmp/deleted-pod.txt)"
```

```section:begin
name: breakdown-delete-one-pod
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pods -l app=hello-dcs`** — lists the app's Pods.
- **`-o name`** — prints `pod/<name>` lines instead of the full table.
- **`| head -n 1`** — keeps one line, so exactly one Pod is targeted.
- **`> /tmp/deleted-pod.txt`** — saves that name, so the check can prove *that* Pod is gone.
- **`oc delete "$(cat /tmp/deleted-pod.txt)"`** — reads the saved name back and deletes that Pod.

```section:end
name: breakdown-delete-one-pod
```

```examiner:execute-test
name: verify-pod-replaced
title: Verify the deleted Pod is gone and a replacement reached Ready
timeout: 30
retries: .INF
delay: 2
```

## Look again

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Still four Pods, `4/4` READY, but one name differs from the list you noted.

**You did not create the new Pod.** The deleted Pod stays deleted.
The Deployment's **ReplicaSet** continuously compares the actual replica count against
`spec.replicas`, and the moment actual dropped to 3 it created a new Pod from the same
template.

{{< note >}}
**💡 Tip:** the same loop ran on the earlier pages, just triggered from the other side.
There, you changed the **desired** state and the platform rolled out to match it. Here,
something changed the **actual** state and the platform rolled forward to match desired.
Either direction, the ReplicaSet's only job is to make actual equal desired.
{{< /note >}}

## The same mechanism in production

Nothing here was special-cased for a lab. The same mechanism recovers from a node failure,
an evicted Pod, or a container that crashes on its own.

If a Deployment fits its budget and has probes, the platform can keep it running without
manual action.
