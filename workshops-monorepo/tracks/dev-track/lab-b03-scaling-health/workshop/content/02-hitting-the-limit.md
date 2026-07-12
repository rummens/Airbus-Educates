---
title: Hitting the Limit
---

Time to hit the ceiling on purpose. `deployment-oversized.yaml` asks for **3 replicas, each
requesting 1 full CPU and 1Gi of memory** — 3000m CPU / 3Gi total, well over the medium
budget (2000m / 2Gi). Watch what the quota does.

## Ask for too much

```editor:open-file
file: ~/exercises/deployment-oversized.yaml
```

```terminal:execute
command: oc apply -f ~/exercises/deployment-oversized.yaml
```

Now look at the Pods:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Expected: some Pods `Running`, but at least one stuck in **`Pending`** — it can't be
scheduled because admitting it would blow the quota.

## Read the evidence

The Pod won't tell you why from `get`. The **events** will:

```terminal:execute
command: oc get events --sort-by=.lastTimestamp | tail -n 15
```

Look for a line like `exceeded quota: … requested: requests.cpu=…, used: …, limited: …`.
That's the quota admission webhook refusing the Pod. You can also read it per-object:

```terminal:execute
command: oc describe deployment hello-dcs
```

Confirm the constraint bit:

```examiner:execute-test
name: verify-oversized-pending
title: The oversized request is rejected by the quota
timeout: 8
retries: 4
delay: 3
```

{{< note >}}
This is the important lesson: the quota isn't a suggestion. Asking for more doesn't get you
more — it gets you a **Pending** Pod and a clear event. The fix is never "please raise my
quota" as a first move; it's to **request what the app actually needs**. That's next.
{{< /note >}}
