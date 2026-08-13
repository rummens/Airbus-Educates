---
title: Right-Sizing
---

The oversized manifest failed because it asked for more per Pod than the namespace budget
had left. The fix is not a bigger namespace — it's a Pod that states what it actually
needs, instead of relying on the LimitRange defaults or guessing too high.

## Requests vs limits

Every container can set two numbers per resource, in its
[`resources`](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
block:

- **`requests`** — what the Pod is *guaranteed*, and what the scheduler uses to decide
  which node (and, on {{< param product_short >}}, which slice of your namespace budget)
  it fits into.
- **`limits`** — the *ceiling* the container is capped at; on the memory side, exceeding it
  gets the container killed (`OOMKilled`); on the CPU side, it gets throttled, not killed.

Setting both explicitly, sized to what the app genuinely needs, is what let four replicas
of a tiny app fit comfortably instead of exactly maxing out — or blowing past — the budget.

## Apply the right-sized version

Open the manifest and take a look:

```editor:open-file
file: ~/exercises/deployment-probes.yaml
```

`deployment-probes.yaml` sets `50m`/`64Mi` requests and `100m`/`128Mi` limits per
container — far below the `medium` budget's defaults, let alone its ceiling. It also adds
the liveness and readiness probes you'll look at on the next page; ignore those for now.

```terminal:execute
command: envsubst < deployment-probes.yaml | oc apply -f -
```

{{< note >}}
This applies the known-good desired state over the stuck rollout from the last page — the
same declarative-recovery pattern from A02: don't hand-patch what's broken, apply the
manifest you know is correct. Give the rollout a few seconds to complete.
{{< /note >}}

```examiner:execute-test
name: verify-right-sized
title: Verify hello-dcs is fully ready with explicit, right-sized resources
timeout: 20
retries: .INF
delay: 2
```

Confirm it landed:

```terminal:execute
command: oc get deployment,pods -l app=hello-dcs
```

All four Pods should now read `Running` and `Ready` — the stuck Pod from page 02 is gone,
replaced by one from this new, right-sized template. Check the budget again:

```terminal:execute
command: oc describe quota
```

`limits.memory` should now read something like `512Mi / 2Gi` instead of the `2Gi / 2Gi` you
saw on page 01 — the same four replicas, comfortably inside the budget instead of exactly
filling it, with real headroom left for whatever you deploy next.

```examiner:execute-test
name: verify-right-sized
title: Verify hello-dcs is fully ready with explicit, right-sized resources
timeout: 10
```
