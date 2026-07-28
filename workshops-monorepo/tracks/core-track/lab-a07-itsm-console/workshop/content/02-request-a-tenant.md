---
title: Request a Tenant — the Fields
---

Select **"New tenant — Do this first!"**. You make this request **once**; it is the
prerequisite for everything else, because a namespace can only exist inside a Tenant.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/tenant
```

Recall A06: **Tenant → Namespaces**. The Tenant is the accountable, recharged org unit;
the namespaces are where your workloads run.

## Seven fields, and you're through

| Field | What to put in it |
|---|---|
| **Tenant owner** | E-mail of the person **responsible** for the tenant — who gets asked about security incidents, sizing and finance. Not necessarily you. |
| **Tenant name** | Lowercase letters, digits and `-` — the [Kubernetes naming convention](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/). |
| **Namespace members** | Who gets access. One e-mail address **per line**. |
| **Siglum** | The siglum of your department or project. |
| **Purpose** | One or two sentences on what you'll use it for. |
| **New namespace name** | Optional — names the **default namespace** the Tenant is created with. Blank means it inherits the Tenant name. |
| **Preferred tenant location** | The cluster your tenant lives on. The list differs per ITSM. |

That's the whole first half of the form.

## Two things you can't undo

{{< warning >}}
**Location is permanent.** A Tenant cannot be moved once created — pick the location you
actually work in.

**Names get a suffix.** {{< param product_short >}} appends a random suffix to keep names
unique platform-wide, so you get `my-tenant-<suffix>` back, not exactly what you typed.
Use the name from the confirmation everywhere afterwards.
{{< /warning >}}

{{< note >}}
**Unsure about a field?** Don't stall. Leave it at its default and write your question in
**"Further details"** at the end of the form — that box is read.
{{< /note >}}

The second half of the form is billing and export control, and for most people it is two
quick answers. That's the next page.
