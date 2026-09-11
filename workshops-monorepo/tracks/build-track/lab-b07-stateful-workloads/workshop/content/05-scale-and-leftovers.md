---
title: Scaling, and What It Leaves
---

Scaling a StatefulSet is not symmetric with scaling a Deployment, and the asymmetry is on
purpose.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/scaling
```

## Scale up: a new replica brings a new disk

```terminal:execute
command: oc scale statefulset/hello-dcs --replicas=3 && oc rollout status statefulset/hello-dcs --timeout=180s
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

`hello-dcs-2` appeared **after** the others were Ready, and `data-hello-dcs-2` was provisioned
from the same template. Scaling out a stateful app means provisioning storage, which is why
it is slower than scaling a stateless one.

{{< note >}}
**📌 Note:** the `oc get pvc` output is not label-filtered the way the Pods are — claims from a
`volumeClaimTemplate` carry the template's labels, not necessarily the app's. Drop the `-l` if
you want to see every claim in the namespace.
{{< /note >}}

## Scale down: the disk stays

```terminal:execute
command: oc scale statefulset/hello-dcs --replicas=2 && oc rollout status statefulset/hello-dcs --timeout=120s
```

The highest ordinal goes first — `hello-dcs-2` is the one removed.

```terminal:execute
command: oc get pods -l app=hello-dcs && oc get pvc
```

`hello-dcs-2` is gone. **`data-hello-dcs-2` is still there, still `Bound`.**

```examiner:execute-test
name: verify-pvc-kept-after-scaledown
title: Verify the removed replica's volume was kept, not deleted
timeout: 60
retries: .INF
delay: 3
```

That is deliberate, and it is the right default:

- scaling down is often **temporary**, and the data belongs to replica 2, not to the Pod that
  happened to be running;
- scale back to 3 and `hello-dcs-2` gets **its own data back**;
- deleting a volume is irreversible, so the platform will not do it as a side effect of a
  replica count.

{{< warning >}}
**⚠️ Watch out:** this is also how a storage quota fills up silently. A StatefulSet that has
been scaled up and down a few times leaves claims nobody is watching. They count against your
namespace's storage budget until somebody deletes them by hand.
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

Look for `requests.storage` and `persistentvolumeclaims`. Every claim from every scale-up —
including the one whose Pod is gone — is counted there.

Deleting a StatefulSet behaves the same way: `oc delete statefulset hello-dcs` removes the
Pods and leaves every claim. Cleaning up a stateful workload for real is **two** deletions,
and the second one is the one you have to mean.
