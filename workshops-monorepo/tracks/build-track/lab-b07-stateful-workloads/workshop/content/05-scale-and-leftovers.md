---
title: Scaling, and What It Leaves
---

Scaling a StatefulSet up and down are not symmetric operations, and the difference is
deliberate.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/scaling
```

## Scale up: a new replica brings a new disk

```terminal:execute
command: oc scale statefulset/hello-dcs --replicas=3 && oc rollout status statefulset/hello-dcs --timeout=180s
```

```section:begin
name: breakdown-scale-up
prefix: Breakdown
title: What each part of the command does
```

- **`oc scale statefulset/hello-dcs --replicas=3`** — sets the desired number of replicas to 3.
- **`&&`** — run the next command only if the scale request was accepted.
- **`oc rollout status statefulset/hello-dcs --timeout=180s`** — waits until every replica is ready, or gives up after 180 seconds.

```section:end
name: breakdown-scale-up
```

```examiner:execute-test
name: verify-scaled-up-with-pvc
title: Verify the new replica came with its own new volume
timeout: 90
retries: .INF
delay: 3
```

```terminal:execute
command: oc get pods,pvc -l app=hello-dcs
```

`hello-dcs-2` appeared **after** the others were Ready, and `data-hello-dcs-2` was
provisioned from the same template. Scaling out a stateful app means provisioning storage,
which is why it is slower than scaling a stateless one.

{{< note >}}
**📌 Note:** the `oc get pvc` output is not label-filtered the way the Pods are, because
claims from a `volumeClaimTemplate` carry the template's labels rather than the app's. Drop
the `-l` to see every claim in the namespace.
{{< /note >}}

## Scale down: the disk stays

```terminal:execute
command: oc scale statefulset/hello-dcs --replicas=2 && oc rollout status statefulset/hello-dcs --timeout=120s
```

```section:begin
name: breakdown-scale-down
prefix: Breakdown
title: What each part of the command does
```

- **`oc scale statefulset/hello-dcs --replicas=2`** — sets the desired number of replicas to 2.
- **`&&`** — run the next command only if the scale request was accepted.
- **`oc rollout status statefulset/hello-dcs --timeout=120s`** — waits until every replica is ready, or gives up after 120 seconds.

```section:end
name: breakdown-scale-down
```

The highest ordinal goes first, so `hello-dcs-2` is the one removed.

```terminal:execute
command: oc get pods -l app=hello-dcs && oc get pvc
```

```section:begin
name: breakdown-pods-and-claims
prefix: Breakdown
title: What each part of the command does
```

- **`oc get pods -l app=hello-dcs`** — lists the app's Pods.
- **`&&`** — run the next command only if the first one succeeded.
- **`oc get pvc`** — lists every claim in the namespace, with no label filter.

```section:end
name: breakdown-pods-and-claims
```

`hello-dcs-2` is gone. **`data-hello-dcs-2` is still there, still `Bound`.**

```examiner:execute-test
name: verify-pvc-kept-after-scaledown
title: Verify the removed replica's volume was kept, not deleted
timeout: 60
retries: .INF
delay: 3
```

That is deliberate:

- scaling down is often **temporary**, and the data belongs to replica 2 rather than to the
  Pod that happened to be running;
- scale back to 3 and `hello-dcs-2` gets **its own data back**;
- deleting a volume is irreversible, so the platform will not do it as a side effect of a
  replica count.

{{< warning >}}
**⚠️ Watch out:** this is also how a storage quota fills up without anyone noticing. A
StatefulSet that has been scaled up and down a few times leaves claims behind, and they count
against your namespace's storage budget until somebody deletes them.
{{< /warning >}}

## Check the storage side of the budget

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-storage-quota-read
title: Verify the namespace quota reports storage usage
timeout: 30
retries: .INF
delay: 3
```

Look for `requests.storage` and `persistentvolumeclaims`. Every claim from every scale-up is
counted there, including the one whose Pod is gone.

Deleting a StatefulSet behaves the same way: `oc delete statefulset hello-dcs` removes the
Pods and leaves every claim. To remove a stateful workload completely you delete
**twice**: the StatefulSet, then its claims. Deleting the claims destroys the data.
