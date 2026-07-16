---
title: Tenants & Namespace Types
---

One more layer of vocabulary and you'll have the whole map. Namespaces don't float free —
they belong to a **Tenant**.

## Tenant → Namespaces

A [**Tenant**]({{< param dcs_docs_base_url >}}/concepts/tenancy-and-access) is the
org-level unit on {{< param product_short >}}: it's who's accountable, and it's what gets
billed (recharged). A Tenant **owns one or more Namespaces**. That's the entire model —
two levels:

```
Tenant  (org / accountability / recharging)
 └── Namespace   (DEV)
 └── Namespace   (PROD)
 └── Namespace   ...
```

{{< warning >}}
There is **no separate "project" layer**. On OpenShift, "project" is simply the word for
a namespace — the same thing you've been using — not a third level between Tenant and
Namespace. If you've seen a "Namespace → Project → Tenant" diagram elsewhere, it's wrong
for {{< param product_short >}}.
{{< /warning >}}

## DEV and PROD namespace types

Namespaces come in **types** — most importantly **DEV** and **PROD** — and they behave
differently: PROD is governed more strictly (policy enforcement, and it's where you're
allowed to expose apps), DEV is looser for fast iteration. That the types *exist* is the
point here; *how* the difference is enforced is a Developer-track topic (**B06**).

Look at the markers on your own namespace:

```terminal:execute
command: oc get namespace "$(oc project -q)" -o jsonpath='{.metadata.labels}'; echo
```

```examiner:execute-test
name: verify-namespace-labels
title: Verify your namespace labels are readable
timeout: 10
```

The labels are how the platform tracks which Tenant a namespace belongs to and what type
it is.

{{< note >}}
Don't confuse a **cluster** with a **namespace type**. From A01: Sandbox and PROD are
*clusters* — where the platform runs. DEV and PROD here are *namespace types* — how a
namespace is governed. Different things that reuse the word "PROD".
{{< /note >}}
