---
title: Create an Instance
---

The CRD is on the cluster and the Operator is watching it. Now create a **Custom
Resource** — an instance of that type — and watch the Operator's reconciliation loop
turn it into a running database.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/instance
```

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

Notice what the manifest does **not** contain: no image, no StatefulSet, no
PersistentVolumeClaim, no Service, no probes, no failover logic.

You declare **what** you want. The operator decides **how**.

{{< note >}}
**📌 There is no `imageName` here on purpose.** On {{< param product_short >}} the platform
configures the operator with the operand image it is allowed to run, from the
{{< param product_short >}} registry. Which PostgreSQL build runs is not the tenant's
decision — that is "the platform owns the operator", in one field.
{{< /note >}}

{{< warning >}}
**⚠️ In this training session the database will not finish starting.** You will see the
operator create everything — volume claim, Services, secrets, Pods — and then the PostgreSQL
process fail with `Permission denied`.

That is the Academy's own environment, not the operator: a training namespace runs under a
stricter security policy than a real tenant namespace, and never assigns the container a UID
to run as. On {{< param product_short >}} the same four lines produce a running database.

Everything this lab is about — what you declared, what the operator built from it, and who
owns which half — is visible regardless.
{{< /warning >}}

{{< note >}}
**📌 Why `-n $DB_NS`.** The database goes in a namespace next to your session's, not in the
session namespace itself. A training session runs under the workshop's own security policy,
and the operand the operator starts cannot execute there. It also keeps the operator's objects together in one place, which is where a real tenant
would put a database anyway.
{{< /note >}}

```terminal:execute
command: oc apply -f sample-cr.yaml -n $DB_NS
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
command: oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS
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
**📌 Note:** Provisioning storage and starting PostgreSQL for the first time takes a minute or two —
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

## After: what it built for you

Back in the upper pane, look at everything that now exists in that namespace:

```terminal:execute
command: oc get cluster,pods,pvc,svc,secret -n $DB_NS
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify the operator created the objects behind your four lines
timeout: 150
retries: .INF
delay: 5
```

You wrote **four lines of spec**. The operator produced a volume claim, Services, secrets and
Pods — each one an object you would otherwise have had to write, name, size and wire together
yourself.

Read the CR's own status, which is how an operator reports back:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS -o jsonpath='{.status.phase}{"\n"}'
```

```examiner:execute-test
name: verify-cr-status-reported
title: Verify the Cluster reports a status of its own
timeout: 60
retries: .INF
delay: 5
```

On a real tenant namespace that settles at `Cluster in healthy state`. Here it stops short,
for the environment reason above — but the loop from page 01 has already played out in full:
you declared a `Cluster`, the operator noticed, and it went to work making reality match.

Same field, two ways of looking at it — a table column, and a raw value. Either way,
that's the whole loop from page 01, played out for real: you declared a `Cluster`, the
Operator noticed, and it kept working until actual state matched desired state.
