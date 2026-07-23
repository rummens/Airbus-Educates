---
title: Self-Healing
---

Everything so far — scaling, right-sizing, probes — has been about *shaping* the desired
state you want. This page proves {{< param product_short >}} actually **enforces** it:
delete a running Pod outright, by hand, with no rollout involved, and watch the platform
put it back without you asking twice.

## Before: four ready Pods

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Note the Pod names in the `NAME` column — one of them is about to disappear for good, and
a **new** one will take its place.

## Watch it happen (lower terminal)

```terminal:execute
command: watch oc get pods -o wide -l app=hello-dcs
session: 2
```

## Delete one Pod (upper terminal)

Back in the upper pane, pick exactly one running Pod and delete it:

```terminal:execute
command: |-
  oc get pods -l app=hello-dcs -o name | head -n 1 > /tmp/deleted-pod.txt
  oc delete "$(cat /tmp/deleted-pod.txt)"
```

`-o name` prints just `pod/<name>` — one per line — instead of the full table; `head -n 1`
keeps only the first line, so exactly one Pod is targeted and its name is saved for the
check below.

```examiner:execute-test
name: verify-pod-replaced
title: Verify the deleted Pod is gone and a replacement has reached Ready
timeout: 15
retries: .INF
delay: 2
```

Look again:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Still four Pods, `4/4` READY — but one of the names is different from the list you noted
above. **You didn't create that Pod.** The one you deleted is gone for good; nothing brought
it back. Instead, the [**Deployment**](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)'s
underlying **ReplicaSet** continuously compares the actual replica count against the
desired count from `spec.replicas`. The moment actual (3) dropped below desired (4), it
created a brand-new Pod from the exact same template to close the gap — the same
reconciliation loop from Core A05, now watched live instead of taken on faith.

{{< note >}}
This is the same reconciliation you drove by hand on page 03 (re-applying a manifest) and
page 04 (fixing a probe) — only the trigger differs. There, you changed the *desired*
state and the platform rolled out to match it. Here, something changed the *actual* state
(you deleted a Pod) and the platform rolled forward to match desired again. Either
direction, the ReplicaSet's only job is to make actual equal desired.
{{< /note >}}

## Why this matters

Nothing you did was special-cased for this lab — the exact same mechanism is what
recovers from a node failure, an evicted Pod, or a container that crashes on its own. You
don't get paged to manually recreate a Pod on {{< param product_short >}}; the platform
already did it before you finished reading the alert. That's the practical payoff of
everything this workshop covered: a Deployment that fits its budget and proves its own
health is a Deployment the platform can actually keep alive without you.
