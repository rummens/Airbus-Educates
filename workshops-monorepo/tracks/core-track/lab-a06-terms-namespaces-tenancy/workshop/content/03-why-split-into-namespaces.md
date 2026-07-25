---
title: Why Split Into Namespaces?
---

You just saw isolation work. So why would a real tenant run more than one namespace? Here
are four common reasons, each one something you saw in the demo.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/why-split
```

## Separate instances of one app

The most common reason: **DEV / QA / PROD** copies of the same service, each in its own
namespace, each with the same object names, each on its own lifecycle. This is the same as
the `hello`-in-two-namespaces demo you ran, applied to a real delivery pipeline.

{{< note >}}
DEV and PROD aren't just naming conventions on {{< param product_short >}} — they're
namespace **types** with different rules. You'll see how they're enforced in the
Developer track (**B06**).
{{< /note >}}

## Team and blast-radius isolation

A mistake in one namespace — a bad rollout, a workload consuming too much, an accidental
delete — **cannot reach another**. Scaling `app-a` to zero did not touch `app-b`. Each
team's mistakes stay within their own namespace.

## Independent quotas and RBAC

Each namespace gets its **own** resource budget and its **own** access rules. One team's
namespace can be generous and open; another's can be locked down and small — independently.
(The deep dive on access is Developer **B05**.)

## Naming freedom

The absence of a name clash is the point. Two teams can both call their app `hello`,
`api`, or `db` without coordinating — because the namespace keeps the names apart.

## Check your understanding

You want DEV, QA and PROD copies of the same app — same names — all running at once.
What gives you that cleanly?

{{< note >}}
**Answer:** Put each copy in its **own namespace**. Identical names coexist without
clashing, and each instance has an independent lifecycle, quota, and access policy.
{{< /note >}}
