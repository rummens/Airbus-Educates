---
title: Why Split Into Namespaces?
---

Tenants run more than one namespace for four common reasons, each one something you saw
in the demo.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/why-split
```

## Separate instances of one app

The most common reason: **DEV / QA / PROD** copies of the same service, each in its own
namespace with the same object names and its own lifecycle. This is the same as
the `hello`-in-two-namespaces demo you ran, applied to a real delivery pipeline.

{{< note >}}
**📌 Note:** on {{< param product_short >}}, DEV and PROD are namespace **types** with
different rules. The **DEV vs PROD Namespaces** lab (Operate & Observe track) shows how
they are enforced.
{{< /note >}}

## Team and blast-radius isolation

A mistake in one namespace — a bad rollout, a workload consuming too much, an accidental
delete — **cannot reach another**. Scaling `app-a` to zero did not touch `app-b`.

## Independent quotas and RBAC

Each namespace gets its **own** resource budget and its **own** access rules. One team's
namespace can have a large quota and wide access while another's is small and locked down.
(The **RBAC & Tenancy** lab in the Operate & Observe track covers access in full.)

## Naming freedom

Because namespaces keep names apart, two teams can both call their app `hello`, `api` or
`db` without coordinating.

## Check your understanding

You want DEV, QA and PROD copies of the same app — same names — all running at once.
What gives you that cleanly?

{{< note >}}
**❓ Answer:** Put each copy in its **own namespace**. Identical names coexist without
clashing, and each instance has an independent lifecycle, quota, and access policy.
{{< /note >}}
