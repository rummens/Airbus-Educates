---
title: Create an Instance
---

The CRD is on the cluster and the Operator is watching it. Now create a **Custom
Resource** — an instance of that type — and watch the Operator's reconciliation loop
turn it into a running database.

## Open the manifest

`sample-cr.yaml` is the smallest useful CloudNativePG `Cluster`: one instance, minimal
storage.

```editor:open-file
file: ~/exercises/sample-cr.yaml
```

Three fields matter, and they're all things **you** control — nothing here touches how
the Operator itself works:

- **`spec.instances`** — how many copies of PostgreSQL you want. `1` is enough to see
  reconciliation happen; a production database would use `3` for automatic failover, a
  day-2 decision that's entirely yours to make.
- **`spec.imageName`** — which PostgreSQL image the Operator runs your instances with,
  resolved from the {{< param product_short >}} Harbor registry — never a public one.
- **`spec.storage.size`** — how much disk this instance gets.

Notice what's *not* here: nothing about how the Operator watches this object, how it
elects a primary, or how it wires up the underlying Pods. That's the Operator's job, not
yours — you declare the outcome, it handles the mechanism.

## Apply it

The image reference uses `${DCS_REGISTRY}`, so apply it through `envsubst` — never a
plain `oc apply` on this file, or the literal, unresolved `${DCS_REGISTRY}` string would
be sent to the cluster:

```terminal:execute
command: envsubst < sample-cr.yaml | oc apply -f -
```

```examiner:execute-test
name: verify-cr-created
title: Verify the sample-db Cluster CR was created
timeout: 10
```

## Before: just created, not yet reconciled

Look at it immediately — the object exists, but the Operator hasn't had time to act on
it yet:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db
```

```examiner:execute-test
name: verify-cr-created
title: Verify the CR exists (before reconciliation)
timeout: 10
```

The `STATUS` column is blank or shows an early transitional message — the CR is
registered, but nothing has been provisioned for it yet. That gap between "exists" and
"actually running" is exactly what the reconciliation loop from page 01 closes.

## Watch the Operator provision it

In the **lower** terminal pane, watch for the Pod the Operator schedules to run this
instance:

```terminal:execute
command: watch oc get pods -l cnpg.io/cluster=sample-db
session: 2
```

{{< note >}}
Provisioning storage and starting PostgreSQL for the first time takes a minute or two —
this is not stuck, the Operator is working through its own reconciliation steps
(allocate storage, start the container, initialise the database, elect a primary). The
check below polls until it's done, so there's nothing to do but wait and watch the lower
pane.
{{< /note >}}

```examiner:execute-test
name: verify-pod-scheduled
title: Verify the operator has scheduled a Pod for sample-db
timeout: 10
retries: .INF
delay: 3
```

Once a Pod appears and settles into `Running`, stop the watch — it's served its purpose:

```terminal:interrupt
session: 2
```

## After: reconciled and healthy

Back in the upper pane, check the CR again:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify sample-db reports a healthy phase
timeout: 10
retries: .INF
delay: 3
```

This time `STATUS` reads **`Cluster in healthy state`** — the Operator finished
reconciling, and reality now matches what you declared. Read that same field directly
with [`-o jsonpath=`](https://kubernetes.io/docs/reference/kubectl/jsonpath/), which
extracts a single value from an object instead of printing the whole thing — useful any
time you want one fact, not a full `-o yaml` dump:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db -o jsonpath='{.status.phase}'
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify status.phase reads Cluster in healthy state
timeout: 10
```

Same field, two ways of looking at it — a table column, and a raw value. Either way,
that's the whole loop from page 01, played out for real: you declared a `Cluster`, the
Operator noticed, and it kept working until actual state matched desired state.
