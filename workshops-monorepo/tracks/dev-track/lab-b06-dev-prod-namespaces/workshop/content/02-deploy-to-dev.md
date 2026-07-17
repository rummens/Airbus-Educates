---
title: Deploy to DEV
---

Time to make the policy real. First you apply the `ClusterPolicy` that draws the
DEV/PROD line, then you deploy the same `hello-dcs` workload from earlier labs into the
DEV namespace and see what it does — and does not — check.

## Apply the policy

`kyverno-policy.yaml` is a [`ClusterPolicy`](https://kyverno.io/docs/policy-types/cluster-policy/overview/) —
cluster-scoped, so it applies to every namespace at once, not just one:

```editor:open-file
file: ~/exercises/kyverno-policy.yaml
```

Notice its two rules read the `dcs.airbus/namespace-type` label on the *target*
namespace, not anything on the workload itself:

- `route-requires-prod` — rejects a Route in any namespace that isn't `prod`.
- `prod-requires-resources` — rejects a container that omits CPU/memory requests and
  limits, but **only** in a namespace labelled `prod`.

```terminal:execute
command: oc apply -f kyverno-policy.yaml
```

{{< note >}}
**On real {{< param product_short >}} you would never run this command.** ClusterPolicies
are cluster-scoped, and — as B05 showed — tenants never create cluster-scoped objects. On
the live platform this policy is pre-applied by the platform team and PROD's enforcement is
simply *there*. You apply it here only because this practice session grants you cluster-admin
so you can watch the rule take effect end-to-end; the aim is to understand what PROD enforces,
not to author the policy yourself.
{{< /note >}}

```examiner:execute-test
name: verify-kyverno-policy-present
title: Verify the ClusterPolicy is present and scoped to PROD
timeout: 10
retries: .INF
delay: 2
```

## Deploy hello-dcs into DEV

`hello-dcs.yaml` is the same Deployment + Service shape you ran in **Deploy Your First
App** — deliberately with **no resources block**. It carries a `${DCS_REGISTRY}` image
reference, so — as in earlier labs — apply it with `envsubst`, never a plain `oc apply`,
or the registry variable is left as a literal string and the image pull fails:

```terminal:execute
command: |-
  envsubst < hello-dcs.yaml | oc apply -n dev -f -
```

The **`-n dev`** selects the namespace the command targets — every command from here on
names `dev` or `prod` explicitly, since you're working across two namespaces in this lab
rather than the one namespace most earlier labs gave you.

{{< note >}}
The image pull can take a few seconds. The check below waits for the Deployment to become
ready.
{{< /note >}}

```examiner:execute-test
name: verify-dev-workload-ready
title: Verify hello-dcs is ready in DEV
timeout: 10
retries: .INF
delay: 2
```

See it for yourself — DEV accepted the manifest exactly as written:

```terminal:execute
command: oc get deployment,pods -n dev -l app=hello-dcs
```

You should see the Deployment `1/1` READY and one Pod `Running` — no different from any
earlier lab. `prod-requires-resources` never fired, because this namespace isn't `prod`.

```examiner:execute-test
name: verify-dev-workload-ready
title: Confirm hello-dcs is running in DEV
timeout: 10
```

## Try to expose it

Everything up to here worked in DEV exactly as it would anywhere. Now try the one thing
DEV doesn't allow:

```terminal:execute
command: oc apply -n dev -f hello-dcs-route.yaml
```

{{< note >}}
**Hint:** read the error `oc apply` prints rather than re-running the command — it names
the rule that rejected it. DEV-type namespaces have no Route capability at all; this
isn't a quota or a typo to fix.
{{< /note >}}

```examiner:execute-test
name: verify-dev-route-blocked
title: Verify the Route was rejected in DEV
timeout: 10
retries: .INF
delay: 2
```

That's the first row of the comparison table made real: the identical Route manifest
that will succeed in PROD on the next page is refused here, at admission, before a Route
object is even created.
