---
title: Do It in PROD
---

Same workload, same Route manifest, same commands — only the namespace changes. Watch
both flip: the workload that DEV accepted unchanged now gets stopped, and the Route DEV
refused now succeeds.

## Deploy the identical workload into PROD

Not a single byte of `hello-dcs.yaml` changes — only the `-n` target does:

```terminal:execute
command: |-
  envsubst < hello-dcs.yaml | oc apply -n prod -f -
```

Read the output closely. The `Service` is created — it carries no container, so
`prod-requires-resources` has nothing to check. The `Deployment` is a different story:
Kyverno rejects it right there in the `oc apply` output, naming the
`dcs-namespace-type-policy` rule that blocked it and the missing `resources` block that
triggered it.

{{< note >}}
Kyverno auto-generates the equivalent rule for the Deployment (and ReplicaSet) that owns
a matched Pod. That's why the Deployment itself is rejected immediately here, rather than
being created and only failing later when its ReplicaSet tries to create a Pod.
{{< /note >}}

```examiner:execute-test
name: verify-prod-workload-blocked
title: Verify PROD rejected the resource-less workload
timeout: 10
retries: .INF
delay: 2
```

Confirm it for yourself — no ready replicas, in contrast to DEV's `1/1` on the previous
page:

```terminal:execute
command: oc get deployment,pods -n prod -l app=hello-dcs
```

You should see no `hello-dcs` Deployment listed at all (the create was rejected outright)
— compare that with the `1/1 READY` you saw for the exact same manifest in `dev`.

```examiner:execute-test
name: verify-prod-workload-blocked
title: Confirm PROD still has no ready hello-dcs Pods
timeout: 10
```

{{< note >}}
This lab stops at "PROD rejected it" so the enforcement is unmistakable. On real DCS,
the next step would be fixing the manifest — adding a `resources` block — and re-applying;
that's ordinary iteration, not a special recovery procedure.
{{< /note >}}

## Create the Route in PROD

The Route doesn't depend on the Deployment being ready — it only needs the `Service`,
which PROD already accepted. Apply the identical Route manifest DEV refused:

```terminal:execute
command: oc apply -n prod -f hello-dcs-route.yaml
```

```examiner:execute-test
name: verify-prod-route-created
title: Verify the Route was admitted in PROD
timeout: 10
retries: .INF
delay: 2
```

See the host DCS assigned:

```terminal:execute
command: oc get route hello-dcs -n prod -o jsonpath='{.spec.host}{"\n"}'
```

You should see a hostname printed — where the same command against `dev` would show
nothing, because no Route object was ever created there.

```examiner:execute-test
name: verify-prod-route-created
title: Confirm the Route host is set in PROD
timeout: 10
```

That's the full contrast from the comparison table on page one, seen live: the same
workload, the same Route, admitted or rejected purely on which namespace type it landed
in.
