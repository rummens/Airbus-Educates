---
title: Right-Sizing
---

The oversized manifest failed because it asked for more per Pod than the budget had left.

The fix is a Pod that states what it **actually needs** — instead of taking the LimitRange
defaults, or guessing high to be safe.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/right-size
```

## Requests versus limits

Every container can set two numbers per resource in its
[`resources`](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
block, and they do different jobs:

- **`requests`** — what the Pod is **guaranteed**. The scheduler uses it to decide where the
  Pod fits, and the namespace quota counts it.
- **`limits`** — the **ceiling**. Cross it on memory and the container is killed
  (`OOMKilled`); cross it on CPU and the container is throttled, not killed.

Setting both, sized to what the app genuinely uses, is what lets four replicas of a small app
sit comfortably inside a budget instead of filling it exactly.

## Apply the right-sized version

```editor:open-file
file: ~/exercises/deployment-probes.yaml
```

This manifest sets **50m / 64Mi** requests and **100m / 128Mi** limits per container. It also
adds the two probes the next page is about — ignore those for now.

```terminal:execute
command: envsubst < deployment-probes.yaml | oc apply -f -
```

{{< note >}}
**💡 Tip:** this applies a known-good desired state **over** a stuck rollout. That is the
declarative recovery move — do not hand-patch the broken thing, apply the manifest you know
is right.
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
title: Verify the namespace budget now has headroom on limits
timeout: 15
retries: .INF
delay: 2
```

`limits.memory` should now read roughly `512Mi / 2Gi` instead of the `2Gi / 2Gi` you saw two
pages ago.

Same four replicas. Same app. A quarter of the budget, and real headroom for whatever you
deploy next.
