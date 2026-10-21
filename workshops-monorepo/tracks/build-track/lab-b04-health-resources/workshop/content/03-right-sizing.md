---
title: Right-Sizing
---

The oversized manifest failed because it asked for more per Pod than the budget had left.

The fix is a Pod that states what it **needs**, instead of taking the LimitRange
defaults or guessing high to be safe.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/right-size
```

## Requests versus limits

Every container can set two numbers per resource in its
[`resources`](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
block, and they do different jobs:

- **`requests`** is what the Pod is **guaranteed**. The scheduler uses it to decide where the
  Pod fits, and the namespace quota counts it.
- **`limits`** is the **ceiling**. Cross it on memory and the container is killed
  (`OOMKilled`); cross it on CPU and the container is throttled instead.

If you set both to what the app uses, four replicas of a small app fit inside the budget
with room to spare.

## Apply the right-sized version

```editor:open-file
file: ~/exercises/deployment-probes.yaml
```

This manifest sets **50m / 64Mi** requests and **100m / 128Mi** limits per container. It
also adds the two probes the next page is about, which you can ignore for now.

```terminal:execute
command: envsubst < deployment-probes.yaml | oc apply -f -
```

{{< note >}}
**💡 Tip:** this applies a known-good desired state **over** a stuck rollout. When a rollout
is stuck, apply the manifest you know is right rather than patching the broken object.
{{< /note >}}

```examiner:execute-test
name: verify-right-sized
title: Verify hello-dcs is fully ready with explicit, right-sized resources
timeout: 30
retries: .INF
delay: 2
```

## Check the budget again

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-quota-headroom
title: Verify the right-sized replicas claim only a fraction of the budget
timeout: 20
retries: .INF
delay: 3
```

`limits.memory` should now read roughly `512Mi / 2Gi` instead of the `2Gi / 2Gi` you saw two
pages ago: four replicas at 128Mi each instead of four at the 512Mi default.

{{< note >}}
**⏳ This takes a moment:** quota accounting lags Pod **termination**. For a few seconds after
the rollout, the retiring Pods are still counted and `Used` still shows the old figure. Run
`oc describe quota` again if you catch it mid-way.
{{< /note >}}

The same four replicas now use a quarter of the budget, which leaves room for other
workloads.
