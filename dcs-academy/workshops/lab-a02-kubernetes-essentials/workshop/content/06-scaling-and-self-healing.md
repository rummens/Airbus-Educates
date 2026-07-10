---
title: Scaling and Self-Healing
---

Because a Deployment maintains *desired state*, two powerful behaviours come almost for
free: scaling, and self-healing.

## Scaling

To run more instances, change the desired replica count. Imperatively:

```terminal:execute
command: oc scale deployment/hello-dcs --replicas=3
```

Output:

```
deployment.apps/hello-dcs scaled
```

{{< note >}}
The new Pods take a moment to start — you may briefly see them `Pending` or
`ContainerCreating`. The check waits until all three are ready.
{{< /note >}}

```examiner:execute-test
name: verify-replicas
title: Verify three replicas are ready
args:
- hello-dcs
- "3"
timeout: 5
retries: .INF
delay: 2
```

Confirm three Pods:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

```examiner:execute-test
name: verify-pods-running
title: Verify three pods are running
args:
- hello-dcs
- "3"
timeout: 10
```

## Self-Healing

The ReplicaSet doesn't just create Pods once — it *continuously* keeps the count at the
desired number. If a Pod dies, it's replaced. Let's watch that happen live using the
split terminal.

In the **left** terminal, watch the Pods continuously:

```terminal:execute-1
command: |-
  watch oc get pods -l app=hello-dcs
```

Now, in the **right** terminal, delete one Pod:

```terminal:execute-2
command: |-
  oc delete $(oc get pod -l app=hello-dcs -o name | head -1)
```

Watch the left terminal: the deleted Pod goes `Terminating`, and almost immediately a
brand-new Pod appears to take its place — the ReplicaSet noticed the count dropped below 3
and fixed it. You never asked it to; that's the control loop working. This is why
Kubernetes is *resilient*: crashed instances are replaced automatically.

Stop the watch in the left terminal:

```terminal:interrupt-1
```

```examiner:execute-test
name: verify-pods-running
title: Verify self-healing restored three pods
args:
- hello-dcs
- "3"
timeout: 30
retries: .INF
delay: 2
```

## Configuration Drift

There's a catch. You scaled to 3 with an imperative command, but your `deployment.yaml`
still says `replicas: 1`. The cluster no longer matches your source of truth — that's
**configuration drift**. Re-applying the file brings reality back in line:

```terminal:execute
command: |-
  envsubst < deployment.yaml | oc apply -f -
```

```terminal:execute
command: oc get pods -l app=hello-dcs
```

You're back to 1 Pod. The lesson: for lasting changes, edit the file and `oc apply` —
imperative commands like `oc scale` are fine for a quick experiment but drift away from
your declared state.

```examiner:execute-test
name: verify-replicas
title: Verify the applied config restored one replica
args:
- hello-dcs
- "1"
timeout: 5
retries: .INF
delay: 2
```
