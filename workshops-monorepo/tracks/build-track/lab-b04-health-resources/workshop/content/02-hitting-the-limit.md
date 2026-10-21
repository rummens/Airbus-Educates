---
title: Hitting the Limit
---

Your namespace's limit side is fully spent: four Pods at the default limit fill the `medium`
budget exactly.

Now watch what happens when a change asks for **more per Pod** instead of taking the
defaults.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/quota-reject
```

## Apply the oversized version

`deployment-oversized.yaml` is the same app and the same four replicas, with explicit
`requests` and `limits` of **700m CPU / 700Mi memory** per container. That is well above the
default, and more than the namespace has left.

```editor:open-file
file: ~/exercises/deployment-oversized.yaml
```

```terminal:execute
command: envsubst < deployment-oversized.yaml | oc apply -f -
```

```section:begin
name: breakdown-apply-oversized
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment-oversized.yaml`** — reads the manifest and replaces `${DCS_REGISTRY}` with the registry address from your session.
- **`| oc apply -f -`** — the pipe hands the result to `oc apply`. The `-f -` means "read the manifest from the pipe" instead of from a file.

```section:end
name: breakdown-apply-oversized
```

{{< note >}}
**⏳ This takes a moment:** the changed Pod template starts a rolling update, so
{{< param product_short >}} tries to create bigger Pods alongside the running ones. The
check below waits for the outcome.
{{< /note >}}

```examiner:execute-test
name: verify-oversized-pending
title: Verify the oversized rollout cannot fully land
timeout: 20
retries: .INF
delay: 2
```

Look at the Pods:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Your original Pods are still `Running` and the rollout is not progressing. Nothing crashed:
the new Pods were **never scheduled at all**.

## Read why

Cluster [events](https://kubernetes.io/docs/concepts/overview/working-with-objects/#object-events)
record what the platform tried, and why it failed:

```terminal:execute
command: oc get events --sort-by=.lastTimestamp
```

```section:begin
name: breakdown-sorted-events
prefix: Breakdown
title: What each part of the command does
```

- **`oc get events`** — lists the recent events in your namespace.
- **`--sort-by=.lastTimestamp`** — sorts them by when they last happened, so the newest are at the bottom, next to your prompt.

```section:end
name: breakdown-sorted-events
```

Look for a `FailedCreate` event naming the ReplicaSet, with a message shaped like this:

```
Warning  FailedCreate  replicaset/hello-dcs-7f8b9c6d4  Error creating: pods "hello-dcs-7f8b9c6d4-x2k9p" is
forbidden: exceeded quota: <your-namespace>, requested: limits.cpu=700m,limits.memory=700Mi, used:
limits.cpu=2,limits.memory=2Gi, limited: limits.cpu=2,limits.memory=2Gi
```

Read it left to right:

1. it **requested** 700m / 700Mi for one more Pod;
2. the namespace was already at its **limited** ceiling of 2 CPU / 2Gi, from the last page;
3. so the create was **refused**, before any node was chosen and before any image was
   pulled.

```examiner:execute-test
name: verify-quota-event-visible
title: Verify the quota-exceeded event is visible in the cluster
timeout: 15
retries: .INF
delay: 2
```

{{< note >}}
**📌 Note:** your exact Pod names and figures will differ. The shape of the message is what
matters.
{{< /note >}}

That is the [**ResourceQuota**](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
working as intended: admission control refusing a request the namespace cannot back.

The fix is to size the Pods correctly. Asking for a bigger namespace is not the answer.
