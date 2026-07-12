---
title: What Makes PROD Different
---

Now the other side. You'll create a **PROD** namespace, put its policy gate in place, and
try the same deploy that just succeeded in DEV.

## Create a PROD namespace

```editor:open-file
file: ~/exercises/prod-namespace.yaml
```

Same shape as the DEV one, but labelled `dcs.airbus/namespace-type: prod`. Apply it:

```terminal:execute
command: oc apply -f prod-namespace.yaml
```

```examiner:execute-test
name: verify-ns-type
title: PROD namespace exists with the prod type label
args:
- team-prod
- prod
timeout: 10
```

## Apply the PROD policy

On {{< param product_short >}}, PROD namespaces are guarded by
[Kyverno](https://kyverno.io/docs/) admission policies. Here is a representative one — it
requires every Deployment in a PROD-type namespace to carry a `data-classification` label,
and it applies **only** to namespaces labelled `namespace-type: prod`:

```editor:open-file
file: ~/exercises/kyverno-policy.yaml
```

```terminal:execute
command: oc apply -f kyverno-policy.yaml
```

```examiner:execute-test
name: verify-policy-present
title: The PROD Kyverno policy is installed
args:
- prod-require-data-classification
timeout: 15
retries: 5
delay: 2
```

{{< note >}}
This step requires **Kyverno** to be installed in the cluster. On real
{{< param product_short >}} it always is; the enforcement below depends on it.
{{< /note >}}

## Try the DEV manifest in PROD

Apply the *same* `hello-dcs.yaml` — the one with no `data-classification` label — but this
time into `team-prod`:

```terminal:execute
command: oc apply -n team-prod -f hello-dcs.yaml
```

This time it is **rejected**. You should see an admission error like:

```
Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
... PROD workloads must carry a 'data-classification' label. Promote a compliant manifest
from DEV — do not edit in place.
```

That rejection *is* the DEV-vs-PROD difference made concrete: identical manifest, allowed
in DEV, blocked in PROD. The Deployment never got created in PROD — confirm it's absent:

```examiner:execute-test
name: verify-prod-blocked
title: The non-compliant deploy was blocked from PROD
args:
- hello-dcs
- team-prod
timeout: 10
```

## Promotion, not editing

So how *does* something reach PROD? You **promote** it: take the manifest, make it
compliant (here, add the required label), review it, and apply the tested version — you
don't hand-edit what's already running in PROD. That's the promotion model
([DCS NaaS lifecycle]({{< param dcs_docs_base_url >}}/naas/dev-prod-lifecycle)): DEV is
where you change things; PROD receives vetted, policy-compliant results.
