---
title: Request a Namespace
---

Select **"New namespace for existing tenant"**. You repeat this one every time your Tenant
needs another namespace — a separate DEV and PROD, another team, another app.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/namespace
```

{{< note >}}
**📌 Your Tenant already came with one namespace.** You only need this request from the
*second* namespace onwards.
{{< /note >}}

## Three fields

| Field | What to put in it |
|---|---|
| **Existing tenant name** | The Tenant this namespace joins — including the random suffix it was given. |
| **Namespace members** | Who gets access. One e-mail address **per line**. |
| **New namespace name** | Lowercase, digits, `-` (same [Kubernetes naming convention](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)). It also gets a random suffix. |

## Then pick "Basic standard namespace"

The form offers three options. To get started, pick the first one:

- ✅ **Basic standard namespace** — pre-configured, standard-sized. You are asked only for
  the **usage** and any **features** below, and nothing else. Need more resources later? A
  *Modify namespace* request raises them.
- **DevSpace** — a personal development environment, tied to **one person** and not
  shareable. Own how-to in the docs.
- **Customized (expert mode)** — you set every quota and technical parameter by hand.

{{< note >}}
**📌 Basic runs on the same platform** with sensible defaults, and you can raise its limits
with a request. Choose expert mode only when you already know the exact quota numbers you
need.
{{< /note >}}

## Usage — DEV or PROD

The distinction from the **Terms — Namespaces & Tenancy** lab, now as one radio button:

- **Development** — fewer policies, more tolerance for insecure images, **no service
  exposure**.
- **Production** — stronger policies, less tolerance for insecure images, **service
  exposure allowed**.

That is the rule behind the **Expose Your App** lab: a Route needs a PROD namespace. More:
[DEV and PROD namespaces]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/dev-and-prod-namespace).

## Features — optional checkboxes

Leave them all off if you don't know you need them; they can be added later.

- **Private container registry** — your own Harbor project for this namespace.
- **Proxy access** — reach your local proxy to pull external artefacts.
- **EgressIP** — reach external resources from a dedicated IP address.
- **Custom robot account** — a machine account for CI/CD; describe the privileges it needs
  in "Further details".

{{< warning >}}
**⚠️ Watch out:** "Harbor **project**" is Harbor's own word for a registry namespace. It is **not** a layer
in the {{< param product_short >}} tenancy model — that is still **Tenant →
Namespaces**, as the **Terms — Namespaces & Tenancy** lab said.
{{< /warning >}}

## The whole request, start to finish

Fill in the three fields, choose the usage, tick any features you need, and submit.
{{< param product_short >}} provisions the namespace automatically.

{{< note >}}
**📌 Going further later.** Expert mode adds operators, capacity tiers (16 / 32 / 48 CPU) and
about ten individual quota fields (CPU, memory, ephemeral and PVC storage, image storage,
Harbor space). Each has a documented default — and the documented advice is to **keep the
defaults** unless you know better. The full field list is in the
[how-to for requesting a container Namespace]({{< param dcs_docs_base_url >}}/services/namespace_aas/quick-starts/request-namespace).
{{< /note >}}
