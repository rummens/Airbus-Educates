---
title: The DCS Ownership Model
---

You just declared a PostgreSQL database without creating a Pod, Service or Secret by hand.
This is not a managed database-as-a-service, and the difference matters when something
breaks.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/ownership
```

## Operators, not managed services

{{< param product_short >}} offers platform services, like the CloudNativePG database
you just used, as [**Operators**]({{< param dcs_docs_base_url >}}/concepts/operators),
not as managed services. The split is:

- **The platform owns the Operator**: installing it, upgrading it, and the CRD versions it
  brings. That was already done when you found the CRDs on page 02.
- **You own the instance**: the `Cluster` CR you created, its sizing, its configuration,
  its data, its backups, upgrading it to a newer CR version when you choose to, and
  responding to its incidents. Everything downstream of the object you wrote on page 03
  is yours.

{{< note >}}
**📌 Note:** with a managed database-as-a-service from a cloud provider, the *provider* owns
day-2 operations for the instance itself: sizing, patching, backup verification and incident
response. On {{< param product_short >}} that line sits one level up. The platform's
responsibility stops at the Operator working correctly and the CRD being current. Whether
your `sample-db` instance is backed up, sized correctly and recovers from an incident is
yours.
{{< /note >}}

## Why it is drawn there

An Operator encodes *generic* operational knowledge for its kind of application: how to
provision storage, elect a primary, apply a config change safely. It does not know what data
matters to you, how much traffic to expect, or what your recovery-time expectations are.

Those are decisions only the owner of a specific instance can make, so the line is drawn
there: generic operational mechanics are the platform's, instance-specific decisions are the
tenant's.

This is the [Responsibility Matrix]({{< param dcs_docs_base_url >}}/governance/overview)
from {{< param product_short >}}'s governance model, applied to Operator-managed services. It
is drawn at a different line than a public-cloud managed service, and it is a common source of
support-ticket confusion for teams new to the platform.

## Recap: the boundary in the object you already ran

The boundary is visible in the same `oc get` from page 03, read with this split in
mind:

```terminal:execute
command: oc get cluster.postgresql.cnpg.io sample-db -n $DB_NS
```

```examiner:execute-test
name: verify-cr-healthy
title: Verify the operator still manages sample-db
timeout: 10
```

Everything that object's `STATUS` reports is yours to watch and act on. The Operator that
produces the status, and the CRD that defines its shape, are the platform's to maintain.
