---
title: Self-Healing
---

Everything so far has been about **shaping** the desired state: replica count, resource
numbers, probes.

This page proves {{< param product_short >}} actually **enforces** it. You delete a running
Pod by hand — no rollout, no manifest — and watch the platform put one back.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/self-healing
```

## Note the names

```terminal:execute
command: oc get pods -l app=hello-dcs
```

One of those names is about to disappear for good, and a **new** one will take its place.

## Watch it happen

In the **lower** pane:

```terminal:execute
command: timeout 60 oc get pods -l app=hello-dcs --watch
session: 2
```

## Delete one Pod

In the **upper** pane, pick exactly one running Pod and delete it:

```terminal:execute
command: |-
  oc get pods -l app=hello-dcs -o name | head -n 1 > /tmp/deleted-pod.txt
  oc delete "$(cat /tmp/deleted-pod.txt)"
```

What that does, piece by piece:

- **`-o name`** — prints `pod/<name>` lines instead of the full table.
- **`head -n 1`** — keeps one line, so exactly one Pod is targeted.
- **`> /tmp/deleted-pod.txt`** — saves the name, so the check can prove *that* Pod is gone.

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

Still four Pods, `4/4` READY — but one name differs from the list you noted.

**You did not create that Pod.** The one you deleted is gone for good; nothing brought it
back. The Deployment's **ReplicaSet** continuously compares the actual replica count against
`spec.replicas`, and the moment actual dropped to 3 it created a new Pod from the same
template.

{{< note >}}
**💡 Tip:** the same loop ran on the earlier pages, just triggered from the other side.
There, you changed the **desired** state and the platform rolled out to match it. Here,
something changed the **actual** state and the platform rolled forward to match desired.
Either direction, the ReplicaSet's only job is to make actual equal desired.
{{< /note >}}

## Why this matters

Nothing here was special-cased for a lab. The same mechanism recovers from a node failure,
an evicted Pod, or a container that crashes on its own.

That is the practical payoff of this whole lab: a Deployment that fits its budget and proves
its own health is a Deployment the platform can keep alive without you.
