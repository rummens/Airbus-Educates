---
title: Spreading Replicas
---

If all three replicas run on **one** node, a node failure takes the app down and a drain
restarts every replica.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/spread
```

## Where they run now

```terminal:execute
command: oc get pods -l app=hello-dcs -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,STATUS:.status.phase
```

Read the **NODE** column. The scheduler packs workloads by default, because it is
optimising for efficient use of the cluster rather than for your availability.

## Ask to be spread

```editor:open-file
file: ~/exercises/deployment-spread.yaml
```

Two mechanisms, both asking for the same thing:

- **`topologySpreadConstraints`** keeps the number of Pods per **topology domain** within
  `maxSkew` of each other. `topologyKey: kubernetes.io/hostname` means per node, and
  `topology.kubernetes.io/zone` would mean per failure domain.
- **`podAntiAffinity`** (preferred) is the older phrasing for the same idea: prefer not to
  place two of these together.

```terminal:execute
command: envsubst < deployment-spread.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
```

```examiner:execute-test
name: verify-spread-constraints
title: Verify the Pod template now asks to be spread across nodes
timeout: 60
retries: .INF
delay: 3
```

## Prefer or require

`whenUnsatisfiable` decides what happens when the spread is not possible:

- **`ScheduleAnyway`**, used here, is a **preference**. If the spread cannot be honoured the
  Pod still runs, just not where you hoped.
- **`DoNotSchedule`** is a **requirement**. The spread is guaranteed, and a Pod that cannot
  satisfy it stays **Pending**, indefinitely if the cluster has nowhere to put it.

```terminal:execute
command: oc get pods -l app=hello-dcs -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,STATUS:.status.phase
```

```examiner:execute-test
name: verify-all-replicas-scheduled
title: Verify every replica is running despite the spread request
timeout: 90
retries: .INF
delay: 3
```

{{< note >}}
**📌 If every Pod is on the same node**, a single-node training or test cluster has nowhere
to spread to. `ScheduleAnyway` is why they are all `Running` anyway. Swap in `DoNotSchedule`
on such a cluster and two of the three would sit `Pending`.
{{< /note >}}

## Choosing

- **`ScheduleAnyway`** for most apps: better placement when it is available, and never a Pod
  that cannot start.
- **`DoNotSchedule`** when being co-located is unacceptable, for example a quorum member whose
  peers must not share a failure domain, and you accept Pending as the alternative.

{{< warning >}}
**⚠️ Watch out:** spreading interacts with your **quota** and the cluster's free capacity. A
hard spread on a busy cluster produces a slow rollout with Pods stuck Pending, and the reason
is in a scheduler event. Check `oc describe pod` first.
{{< /warning >}}

A budget, spread replicas and an app that handles `SIGTERM` let the platform do its
maintenance without your users noticing. `hello-dcs` ignores `SIGTERM`, so each of its Pods
still waits out the full grace period and is then killed with `SIGKILL`.
