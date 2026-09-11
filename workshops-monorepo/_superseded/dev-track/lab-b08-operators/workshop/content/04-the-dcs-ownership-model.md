---
title: The DCS Ownership Model
---

You just created a working PostgreSQL database in a few minutes, without provisioning a
single Pod, Service, or Secret by hand. It's tempting to read that as "DCS runs my
database for me" — a managed database-as-a-service. That reading is wrong, and getting
it right is the single most important idea in this workshop.

## Operators, not aaS

{{< param product_short >}} offers platform services — like the CloudNativePG database
you just used — as [**Operators**]({{< param dcs_docs_base_url >}}/concepts/operators),
not as managed/aaS. The split is exact:

- **The platform owns the Operator**: installing it, upgrading it, and the CRD versions
  it brings. That's the part you saw was already done when you found the CRDs on
  page 02 — you never touched it, and on {{< param product_short >}} you never will.
- **You own the instance**: the `Cluster` CR you created, its sizing, its configuration,
  its data, its backups, upgrading it to a newer CR version when you choose to, and
  responding to its incidents. Everything downstream of the object you wrote on page 03
  is yours.

{{< note >}}
Contrast this with a managed database-as-a-service from a cloud provider, where the
*provider* owns day-2 operations — sizing, patching, backup verification, incident
response — for the instance itself, not just the software that runs it. On
{{< param product_short >}}, that line sits one level up: the platform's
responsibility stops at "the Operator works correctly and the CRD is current." Whether
your `sample-db` instance is backed up, sized correctly, and recovers from an incident is
on you, the same as it would be if you'd built the database yourself.
{{< /note >}}

## Why it's drawn there

This split exists because an Operator only encodes *generic* operational knowledge for
its kind of application — how to provision storage, elect a primary, apply a config
safely. It has no idea what data matters to you, how much traffic your instance should
expect, or what your recovery-time expectations are. Those are decisions only the owner
of a specific instance can make, so {{< param product_short >}} draws the line exactly
there: generic operational mechanics are the platform's job; instance-specific decisions
are the tenant's.

This is the same logic as the [Responsibility Matrix]({{< param dcs_docs_base_url >}}/governance/overview)
you'll meet elsewhere in {{< param product_short >}}'s governance model, applied
specifically to Operator-managed services: a shared responsibility split, drawn at a
different line than a public-cloud managed service, and worth knowing precisely — it's
the most common source of support-ticket confusion for teams new to {{< param product_short >}}.

## Recap: the boundary in the object you already ran

You don't need a new command to see the boundary — it's the same `oc get` from page 03,
read with this split in mind:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify sample-db is still healthy
timeout: 10
```

Everything that object's `STATUS` reports — healthy or not — is something you're
responsible for watching and acting on. The Operator that produces that status, and the
CRD that defines its shape, are the platform's to maintain. Same object, two owners, one
clean line between them.
