---
title: Create an Instance
---

The CRD is on the cluster and the Operator is watching it. Now create a **Custom
Resource**, an instance of that type, and watch the Operator's reconciliation loop
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

Two fields matter, and both are things **you** control; neither changes how the Operator
itself works:

- **`spec.instances`** — how many copies of PostgreSQL you want. `1` is enough to see
  reconciliation happen; a production database would use `3` for automatic failover, a
  day-2 decision that is yours to make.
- **`spec.storage.size`** — how much disk this instance gets.

## Apply it

The manifest has no image, StatefulSet, PersistentVolumeClaim, Service, probes or failover
logic. You declare what you want, and the operator decides how to build it.

{{< note >}}
**📌 There is no `imageName` here on purpose.** On {{< param product_short >}} the platform
configures the operator with the operand image it is allowed to run, from the
{{< param product_short >}} registry. Which PostgreSQL build runs is decided by the
platform, because the platform owns the operator.
{{< /note >}}

{{< warning >}}
**⚠️ In this training session the database will not finish starting.** You will see the
operator create the volume claim, Services, secrets and Pods, and then the PostgreSQL
process fail with `Permission denied`.

The cause is the Academy's environment, not the operator: a training namespace runs under a
stricter security policy than a real tenant namespace, and never assigns the container a UID
to run as. On {{< param product_short >}} the same manifest produces a running database.

You can still see what you declared, what the operator built from it, and who owns which
part.
{{< /warning >}}

{{< note >}}
**📌 Why `-n $DB_NS`.** The database goes in a namespace next to your session's, not in the
session namespace itself. A training session runs under the workshop's own security policy,
and the operand the operator starts cannot execute there. A separate namespace also keeps
the operator's objects together, which is where a real tenant would put a database anyway.
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

Look at it immediately. The object exists, but the Operator has not had time to act on
it yet:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS
```

```examiner:execute-test
name: verify-cr-created
title: Verify the CR exists (before reconciliation)
timeout: 10
```

The `STATUS` column is blank or shows an early transitional message. The CR is
registered, but nothing has been provisioned for it yet. The reconciliation loop from page 01
closes the gap between "exists" and "running".

## Watch the Operator provision it

In the **lower** terminal pane, watch for the Pod the Operator schedules to run this
instance:

```terminal:execute
command: watch oc get pods -l cnpg.io/cluster=sample-db -n $DB_NS
session: 2
```

{{< note >}}
**📌 Note:** Provisioning storage and starting PostgreSQL for the first time takes a minute or two.
This is not stuck: the Operator is working through its reconciliation steps (allocate
storage, start the container, initialise the database, elect a primary). The check below
polls until a Pod is scheduled, so wait and watch the lower pane.
{{< /note >}}

```examiner:execute-test
name: verify-pod-scheduled
title: Verify the operator has scheduled a Pod for sample-db
timeout: 10
retries: .INF
delay: 3
```

Once a Pod appears, stop the watch:

```terminal:interrupt
session: 2
```

## After: what it built for you

Back in the upper pane, look at everything that now exists in that namespace:

```terminal:execute
command: oc get clusters.postgresql.cnpg.io,pods,pvc,svc,secret -n $DB_NS
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify the operator created the objects behind your three lines of spec
timeout: 150
retries: .INF
delay: 5
```

You wrote **three lines of spec**. The operator produced a volume claim, Services, secrets and
Pods, each one an object you would otherwise have had to write, name, size and wire together
yourself.

Read the CR's own status, which is how an operator reports back:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS -o jsonpath='{.status.phase}{"\n"}'
```

```section:begin
name: breakdown-cluster-phase
prefix: Breakdown
title: What each part of the command does
```

- **`oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS`** — reads your `Cluster`, using the full kind name so `oc` does not confuse it with another `Cluster` type.
- **`-o jsonpath='{.status.phase}{"\n"}'`** — prints only the phase the operator wrote into the resource's status, followed by a newline.

```section:end
name: breakdown-cluster-phase
```

```examiner:execute-test
name: verify-cr-status-reported
title: Verify the Cluster reports a status of its own
timeout: 60
retries: .INF
delay: 5
```

On a real tenant namespace the phase settles at `Cluster in healthy state`. Here it stops
short, for the reason in the warning above, but the loop from page 01 has still run: you
declared a `Cluster`, and the operator created the objects to match it.
