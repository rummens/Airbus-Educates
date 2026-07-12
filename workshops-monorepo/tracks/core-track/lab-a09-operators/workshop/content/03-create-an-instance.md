---
title: Create an Instance
---

Now the part you own: create a **Custom Resource** and watch the operator turn it into a
running application.

## Look at the CR

```editor:open-file
file: ~/exercises/sample-cr.yaml
```

It's small on purpose. Every field here is something *you*, the instance owner, decide:

- `instances: 1` — how many PostgreSQL servers.
- `imageName` — the operand image, pulled from {{< param product_short >}} Harbor.
- `storage.size` — how much persistent storage the database gets.
- `resources` — CPU/memory within your namespace quota.

You describe *what* you want; the operator handles *how* to build and maintain it.

## Apply it

```terminal:execute
command: oc apply -f sample-cr.yaml
```

```examiner:execute-test
name: verify-cr-created
title: The Cluster CR was created
args:
- cluster.postgresql.cnpg.io
- demo-db
timeout: 10
```

{{< note >}}
The operator now reconciles your CR — creating a PostgreSQL pod, a service, secrets, and
config. This takes a little time (image pull + database bootstrap). "Done" is when the
cluster reports a ready instance.
{{< /note >}}

## Watch it reconcile

```terminal:execute
command: oc get cluster.postgresql.cnpg.io demo-db
```

Then inspect the status the operator maintains:

```terminal:execute
command: oc describe cluster.postgresql.cnpg.io demo-db
```

Look at the status/conditions — the operator reports what it has done and the cluster's
health. When a ready instance appears, the reconcile succeeded:

```examiner:execute-test
name: verify-cr-ready
title: The operator reconciled the CR into a running database
args:
- demo-db
timeout: 300
retries: .INF
delay: 5
```

You applied a few lines of YAML and got a managed PostgreSQL — that's the operator earning
its keep. But "managed by the operator" is not the same as "managed by DCS" — that's the
next, crucial page.
