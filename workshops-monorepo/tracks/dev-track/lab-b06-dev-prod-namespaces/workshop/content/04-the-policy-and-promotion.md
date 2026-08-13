---
title: The Policy, and Promotion
---

You've now felt both differences the comparison table promised. This last page reads the
policy itself, then names the change model that follows from it: **promotion**.

## Read the policy

You've already applied `dcs-namespace-type-policy` and seen it act twice. List it, then
read it in full:

```terminal:execute
command: oc get clusterpolicy
```

You'll see `dcs-namespace-type-policy` listed — a single object doing both jobs you've
watched, because a `ClusterPolicy` can hold more than one rule.

```terminal:execute
command: oc describe clusterpolicy dcs-namespace-type-policy
```

```examiner:execute-test
name: verify-clusterpolicy-rules
title: Verify the ClusterPolicy carries both rules
timeout: 10
```

Walk the `describe` output against what you saw happen:

- **`route-requires-prod`** — `match` targets `route.openshift.io/v1/Route`, `exclude`
  carves out namespaces labelled `dcs.airbus/namespace-type: prod`, and `validate.deny`
  rejects everything left — i.e. every namespace that isn't PROD. This is what stopped
  your Route in `dev` and let it through in `prod`.
- **`prod-requires-resources`** — `match` targets `Pod`, scoped by `namespaceSelector` to
  `dcs.airbus/namespace-type: prod`, and `validate.pattern` requires a non-empty
  `resources.requests` and `resources.limits` on every container. This is what stopped
  your Deployment in `prod` and let it through in `dev`.

Both rules read the *same* one label off the namespace. Nothing about the workload or the
Route manifest ever changed between DEV and PROD — the namespace's own type is the entire
decision.

{{< note >}}
Want to see what other checks a real Kyverno policy can express? `oc explain` doesn't
cover custom resources like `ClusterPolicy` in useful depth — the
[Kyverno policy library](https://kyverno.io/policies/) is the better next stop, with
dozens of worked examples in the same shape as this one.
{{< /note >}}

## Promotion, not in-place edits

You saw the fix implied by page three's rejection — add a `resources` block — but on real
DCS you wouldn't apply that fix straight into `prod`. The DCS model is **promotion**: you
fix and re-verify the workload in **DEV**, then **re-deploy the same, now-vetted
manifest into PROD** as a fresh apply. You do not edit a running PROD workload in place.

That trade-off is the whole point of having two namespace types instead of one:

- **DEV** optimises for iteration speed — break things, fix them, repeat, cheaply.
- **PROD** optimises for confidence — nothing lands there that hasn't already been proven
  to meet its bar, and every landing is a new, auditable deploy rather than a live edit.

{{< note >}}
This workshop demonstrates the mechanism with one representative rule pair. Real DCS
PROD namespaces enforce a broader
[policy set]({{< param dcs_docs_base_url >}}/naas/dev-prod-lifecycle) than the two rules
here — the promotion model and the DEV/PROD split are the durable ideas to take away, not
this exact rule list.
{{< /note >}}

Next: a short recap, then on to **Scaling, Health & Resources** — making a workload
robust *within* whichever namespace's budget it lands in.
