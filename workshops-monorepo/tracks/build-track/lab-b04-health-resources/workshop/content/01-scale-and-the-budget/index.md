---
title: Scale and the Budget
---

Scaling a [**Deployment**](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
means asking {{< param product_short >}} to keep several identical copies running instead of
one.

Each copy draws on the same **namespace budget**, and that budget is finite.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/budget
```

## Deploy the starting point

`deployment-base.yaml` is `hello-dcs` as it usually arrives: **one replica**, no probes, and
**no `resources` block** at all.

```editor:open-file
file: ~/exercises/deployment-base.yaml
```

Apply it, together with a Service so later pages have an endpoint list to watch.
`envsubst` fills in `${DCS_REGISTRY}` before `oc` sees the manifest:

```terminal:execute
command: envsubst < deployment-base.yaml | oc apply -f - && oc apply -f service.yaml && oc rollout status deploy/hello-dcs --timeout=120s
```

```section:begin
name: breakdown-deploy-and-wait
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment-base.yaml`** — reads the manifest and replaces `${DCS_REGISTRY}` with the registry address from your session.
- **`| oc apply -f -`** — the pipe hands the result to `oc apply`. The `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&& oc apply -f service.yaml`** — if that succeeded, creates the Service from its file. It has no `${DCS_REGISTRY}` in it, so it needs no `envsubst`.
- **`&& oc rollout status deploy/hello-dcs`** — if that succeeded too, waits until the Deployment's Pods are ready.
- **`--timeout=120s`** — gives up after two minutes instead of waiting forever.

```section:end
name: breakdown-deploy-and-wait
```

```examiner:execute-test
name: verify-app-deployed
title: Verify hello-dcs is running with one replica and a Service
timeout: 15
retries: .INF
delay: 2
```

{{< note >}}
**📌 The colours on that button.** A check is **amber** while it waits or runs, **green**
when the state it describes is true, **red** when it is not.
{{< /note >}}

## Scale it up

`--replicas` sets the desired copy count the Deployment must maintain:

```terminal:execute
command: oc scale deploy/hello-dcs --replicas=4
```

```examiner:execute-test
name: verify-scaled
title: Verify hello-dcs is scaled to 4 ready replicas
args:
- "4"
timeout: 20
retries: .INF
delay: 2
```

Look at what you now have:

```terminal:execute
command: oc get deployment,pods -l app=hello-dcs
```

Four Pods, `4/4` READY. {{< param product_short >}} created three more copies from the same
template, and each is scheduled and health-tracked on its own.

## What that costs

None of these Pods states its own resource needs, so each one takes your namespace's
[**LimitRange**](https://kubernetes.io/docs/concepts/policy/limit-range/) defaults for a
`medium` budget:

- a **request** of 128Mi memory / 50m CPU, which is what the Pod is guaranteed and what the
  scheduler counts;
- a **limit** of 512Mi memory / 500m CPU, which is the ceiling it may not cross.

Four Pods at that default limit is **exactly** the whole `medium` budget:

![Four Pods filling the namespace's medium budget exactly, while their requests use only a quarter of it](quota-budget.svg)

Read your namespace's [**ResourceQuota**]({{< param dcs_docs_base_url >}}/concepts/quotas)
to see the numbers:

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-quota-present
title: Verify a ResourceQuota is present in your namespace
timeout: 10
retries: 3
delay: 2
```

The table shows **Used** against **Hard** per resource. Two things to notice:

- **`limits.memory` and `limits.cpu`** now read Used = Hard. The limit side is fully spent.
- **`requests.memory` and `requests.cpu`** are nowhere near full, because the default
  *request* is much smaller than the default *limit*.

Nothing is broken: Used equals Hard, not more. But there is **no headroom left on limits**.
The next page asks for more than that on purpose.
