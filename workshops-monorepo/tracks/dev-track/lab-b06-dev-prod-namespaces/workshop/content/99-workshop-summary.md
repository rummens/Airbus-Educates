---
title: Summary
---

You now know why your Route needed a PROD namespace back in the Core track — and you've
seen the mechanism that enforces it, not just the rule.

## What You Did

- **Created** a DEV and a PROD namespace, each carrying its own `dcs.airbus/namespace-type` label.
- **Applied** a Kyverno `ClusterPolicy` that reads that label to decide what it enforces.
- **Deployed** the identical `hello-dcs` workload into both — accepted unchanged in DEV, **rejected** in PROD for missing resource requests/limits.
- **Applied** the identical Route manifest into both — **rejected** in DEV, admitted with a host in PROD.
- **Read** the policy itself and named **promotion** — fix and re-verify in DEV, re-deploy into PROD, never edit PROD in place.

## Check Your Understanding

1. Which namespace type can host a Route — DEV or PROD?

{{< note >}}
**Answer:** PROD. A DEV-type namespace cannot expose a Route at all — this workshop's
`route-requires-prod` Kyverno rule is what enforces it.
{{< /note >}}

2. What concretely makes PROD "stricter" than DEV?

{{< note >}}
**Answer:** [Kyverno](https://kyverno.io/docs/) admission policies scoped to
namespaces labelled `dcs.airbus/namespace-type: prod` — in this workshop, a rule
requiring every container to declare CPU/memory requests and limits. DEV namespaces
aren't matched by that rule at all.
{{< /note >}}

3. You fixed a workload PROD rejected. What do you do with the fix?

{{< note >}}
**Answer:** **Promote** it — verify the fix in DEV, then re-deploy the same, now-vetted
manifest into PROD as a fresh apply. You don't edit the running PROD workload in place.
{{< /note >}}

## Next Steps

Now that a workload can actually land in PROD, the next question is whether it *stays*
up under load and within its namespace's budget. **B07 — Scaling, Health & Resources**
picks up right there. The policy mindset from this lab returns later too — **B08
(Operators)** and the Security track both build on "PROD enforces more than DEV does."
