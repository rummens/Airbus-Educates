---
title: Why Split Into Namespaces?
---

You just saw isolation work. So why would a real tenant deliberately run more than one
namespace? Four common reasons — all of them things you *just watched happen*.

## Separate instances of one app

The most common one: **DEV / QA / PROD** copies of the same service, each in its own
namespace, each with the same object names, each on its own lifecycle. Exactly the
`hello`-in-two-places demo you ran — scaled up to a real delivery pipeline.

{{< note >}}
DEV and PROD aren't just naming conventions on {{< param product_short >}} — they're
namespace **types** with different rules. You'll see how they're enforced in the
Developer track (**B06**).
{{< /note >}}

## Team and blast-radius isolation

A mistake in one namespace — a bad rollout, a runaway workload, an accidental delete —
**can't reach another**. Scaling `app-a` to zero didn't touch `app-b`. Teams get a blast
radius they control.

## Independent quotas and RBAC

Each namespace gets its **own** resource budget and its **own** access rules. One team's
namespace can be generous and open; another's can be locked down and small — independently.
(The deep dive on access is Developer **B05**.)

## Naming freedom

The name clash you *didn't* get is the point. Two teams can both call their app `hello`,
`api`, or `db` without coordinating — because the namespace keeps the names apart.

## Check your understanding

You want DEV, QA and PROD copies of the same app — same names — all running at once.
What gives you that cleanly?

{{< note >}}
**Answer:** Put each copy in its **own namespace**. Identical names coexist without
clashing, and each instance has an independent lifecycle, quota, and access policy.
{{< /note >}}
