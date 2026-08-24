---
title: Request a Tenant — Billing & Export Control
---

The rest of the tenant form. For most first-time requests both sections are answered in
under a minute.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/tenant-extras
```

## Namespace options — skip ahead

The tenant form embeds the **namespace section**, because it also creates that first
default namespace. Everything in it is on the next page — and the short answer there is
"pick the basic option".

## Billing

Only relevant **if recharging applies to you** — that is, for medium and large requests.
If it doesn't, leave all four fields empty:

- **WBS project code**
- **CC siglum**
- **Facts code** — for information only
- **IWO** — only if you are in a different legal entity, e.g. Airbus Romania

## Export control / ITAR

One declaration: do you plan to put **EC or ITAR data** into any namespace of this tenant?

{{< warning >}}
**⚠️ Watch out:** {{< param product_short >}} **can** host such data. But if you answer yes, you must notify
your **local Export Control team** — your Export Control officer, or the Export Control
hub page, is the place to start. They just want to know; this is a notification duty, not
a rejection.
{{< /warning >}}

## Further details, then submit

The last box is free text. Use it for anything the form doesn't cover: a field you were
unsure about, a different namespace owner than the members you listed, a special need.

Then submit — and {{< param product_short >}} takes over. Provisioning is **automated**,
so you are not waiting on someone to build your tenant by hand.
