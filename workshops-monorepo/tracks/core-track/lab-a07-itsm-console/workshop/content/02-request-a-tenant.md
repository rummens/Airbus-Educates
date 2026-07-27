---
title: Request a Tenant
---

Select **"New tenant — Do this first!"**. This is the request you make **once**, and it is
the prerequisite for everything else — a namespace can only be created *inside* a Tenant.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/tenant
```

Recall the model from A06: **Tenant → Namespaces**, two levels, no "project" in between.
The Tenant is the accountable, recharged org unit; the namespaces are where your workloads
actually run.

## General options

| Field | What to put in it |
|---|---|
| **Tenant owner** | The Airbus e-mail address of the person **responsible** for this tenant — the one who gets asked about security incidents, sizing and finance. Not necessarily you. |
| **Tenant name** | The name of the Tenant. It has to follow the [Kubernetes naming convention](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/): lowercase letters, digits and `-`, no spaces, no underscores, no capitals. |
| **Namespace members** | E-mail addresses of the people who get access, **one per line**. They become users of the tenant's namespaces. |
| **Siglum** | The siglum of the department or project this tenant belongs to. |
| **Purpose of the new tenant** | One or two sentences on what you intend to do with it. |
| **New namespace name** | Optional. The Tenant's **default namespace** is created with it; give it a custom name here, or leave it blank and it inherits the Tenant name. |
| **Preferred tenant location** | The cluster your tenant will live on. The options differ per ITSM — Germany's list is not Spain's. |

{{< warning >}}
**Two things you cannot undo later.** A Tenant **cannot be moved** once its location is
chosen. And **names get a random suffix** appended by {{< param product_short >}} to keep
them unique across the platform — so the tenant you get back is `my-tenant-<suffix>`, not
exactly what you typed. Read the created name from the confirmation and use *that*
everywhere afterwards.
{{< /warning >}}

## Namespace options

The tenant request embeds the **same namespace section** as the standalone namespace
request, because it also creates that first default namespace. Every field there is
explained on the next page — including the shortcut that lets you skip almost all of them.

## Billing options

Only relevant **if recharging applies to you** — medium and large requests. If it does,
supply:

- **WBS project code**
- **CC siglum**
- **Facts code** (for information)
- **IWO** — needed when you are in a different legal entity, e.g. Airbus Romania.

If recharging does not apply, leave these empty.

## Export control / ITAR

You are asked to declare whether you plan to put **EC or ITAR data** into any namespace of
this tenant.

{{< warning >}}
{{< param product_short >}} **can** host such data — but you must contact your **local
Export Control team** to notify them first. This is a notification duty, not a blocker:
they want to double-check. Your local Export Control officer or the Export Control hub
page is the right starting point.
{{< /warning >}}

## Others

The last box is **"Further details"** — free text. Anything the form does not cover, any
question about a field you were unsure about, any deviation you want: write it here rather
than leaving a field wrong. Then submit.

{{< note >}}
**Full reference:** the
[how-to for requesting a Tenant]({{< param dcs_docs_base_url >}}/how-to/request-a-tenant)
in the {{< param product_short >}} docs walks the same form field by field with
screenshots.
{{< /note >}}
