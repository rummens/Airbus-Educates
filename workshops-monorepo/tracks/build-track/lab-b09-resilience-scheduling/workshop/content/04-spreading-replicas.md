---
title: Spreading Replicas
---

Three replicas on **one** node is not three replicas. It is one node's failure away from an
outage, and one drain away from a full restart.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/spread
```

## Where are they now?

```terminal:execute
command: oc get pods -l app=hello-dcs -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,STATUS:.status.phase
```

Read the **NODE** column. The scheduler packs workloads by default: it is trying to use the
cluster efficiently, not to protect you.

## Ask to be spread

```editor:open-file
file: ~/exercises/deployment-spread.yaml
```

Two mechanisms, both asking for the same thing:

- **`topologySpreadConstraints`** — keep the number of Pods per **topology domain** within
  `maxSkew` of each other. `topologyKey: kubernetes.io/hostname` means per node;
  `topology.kubernetes.io/zone` would mean per failure domain.
- **`podAntiAffinity`** (preferred) — the older phrasing: *prefer not to place two of these
  together*.

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

## Prefer, or require?

The single most important field here is `whenUnsatisfiable`:

- **`ScheduleAnyway`** (used here) — a **preference**. If the spread cannot be honoured, the
  Pod still runs, just not where you hoped.
- **`DoNotSchedule`** — a **requirement**. The spread is guaranteed, and a Pod that cannot
  satisfy it stays **Pending** — forever, if the cluster has nowhere to put it.

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
**📌 If every Pod is on the same node** — a single-node training or test cluster has nowhere
to spread to. `ScheduleAnyway` is exactly why they are all `Running` regardless. Swap in
`DoNotSchedule` on such a cluster and two of the three would sit `Pending` forever, which is
the trade-off made visible.
{{< /note >}}

## Choosing

- **`ScheduleAnyway`** for most apps: better placement when it is available, never a Pod that
  cannot start.
- **`DoNotSchedule`** when being co-located is genuinely unacceptable — a quorum member whose
  peers must not share a failure domain — and you accept Pending as the alternative.

{{< warning >}}
**⚠️ Watch out:** spreading interacts with your **quota** and the cluster's free capacity. A
hard spread on a busy cluster is a slow, mysterious rollout: Pods stay Pending with a scheduler
event nobody reads. Check `oc describe pod` before blaming the platform.
{{< /warning >}}

Together with the budget and a clean shutdown, that is the set: the platform can do its
maintenance, and your users do not find out.
