---
title: A Budget for Maintenance
---

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/pdb
```

## Deploy three replicas

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=180s
```

```examiner:execute-test
name: verify-app-ready
title: Verify hello-dcs is running with three ready replicas
timeout: 90
retries: .INF
delay: 3
```

## Declare the budget

```editor:open-file
file: ~/exercises/pdb.yaml
```

`minAvailable: 2` says: whatever you are doing, leave at least two of mine serving.

```terminal:execute
command: oc apply -f pdb.yaml
```

```examiner:execute-test
name: verify-pdb-created
title: Verify the PodDisruptionBudget exists and selects the app
timeout: 30
retries: .INF
delay: 3
```

## Ask it what the platform may do

A PDB's **status** is the useful part, and it is easy to miss:

```terminal:execute
command: oc get pdb hello-dcs -o custom-columns=NAME:.metadata.name,MIN:.spec.minAvailable,ALLOWED:.status.disruptionsAllowed,HEALTHY:.status.currentHealthy,DESIRED:.status.desiredHealthy,EXPECTED:.status.expectedPods
```

Read the columns together:

- **EXPECTED 3** is how many Pods the selector matches.
- **HEALTHY 3** is how many are currently ready.
- **DESIRED 2** is the floor you asked for.
- **ALLOWED 1** is **how many Pods the platform may take away right now**.

That last number is what the object is for. A drain of one node can evict one of your Pods,
then has to wait for a replacement to become ready before touching another.

```examiner:execute-test
name: verify-disruptions-allowed
title: Verify the budget currently allows one Pod to be disrupted
timeout: 60
retries: .INF
delay: 3
```

## Squeeze it to zero

Scale down to exactly the floor:

```terminal:execute
command: oc scale deploy/hello-dcs --replicas=2 && oc rollout status deploy/hello-dcs --timeout=120s
```

```terminal:execute
command: oc get pdb hello-dcs -o custom-columns=MIN:.spec.minAvailable,ALLOWED:.status.disruptionsAllowed,HEALTHY:.status.currentHealthy,EXPECTED:.status.expectedPods
```

**ALLOWED is now 0.** You have two Pods and you promised that two must stay, so the platform
may take **none** of them.

```examiner:execute-test
name: verify-disruptions-blocked
title: Verify the budget now allows no disruption at all
timeout: 60
retries: .INF
delay: 3
```

{{< warning >}}
**⚠️ Watch out:** this is not extra safety. A drain that cannot proceed **waits**, and a node
that cannot be drained does not get patched. A budget nobody can satisfy makes your app the
reason the cluster falls behind on maintenance, and somebody will eventually override it.
{{< /warning >}}

The fix is not a smaller budget. It is **more replicas than your floor**:

```terminal:execute
command: oc scale deploy/hello-dcs --replicas=3 && oc rollout status deploy/hello-dcs --timeout=120s
```

```examiner:execute-test
name: verify-headroom-restored
title: Verify scaling back up restores the platform's room to work
timeout: 90
retries: .INF
delay: 3
```

`minAvailable: 2` with **3** replicas works: it protects two, and leaves the platform one
Pod of room.

Next, what happens to the Pod it takes.
