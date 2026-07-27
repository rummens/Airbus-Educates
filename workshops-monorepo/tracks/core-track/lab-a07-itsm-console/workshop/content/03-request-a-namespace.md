---
title: Request a Namespace
---

Select **"New namespace for existing tenant"**. This is the request you repeat — every
time your Tenant needs another namespace beyond the default one it was created with.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/namespace
```

## General options

| Field | What to put in it |
|---|---|
| **Existing tenant name** | The Tenant this namespace joins — including the random suffix {{< param product_short >}} appended when the Tenant was created. |
| **Namespace members** | E-mail addresses, **one per line**. They become users of this namespace. |
| **New namespace name** | Follow the [Kubernetes naming convention](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/) — lowercase, digits, `-`. |

{{< note >}}
Namespace names also get a **random suffix** appended for uniqueness, exactly like tenant
names. Want somebody other than the listed members to own the namespace? Say so in
**"Further details"** — ownership is not a field on the form.
{{< /note >}}

## Then pick one of three paths

This is the fork that decides how much of the rest of the form you have to fill in:

- **Basic standard namespace** — a pre-configured, standard-sized namespace. You are only
  asked for the namespace **usage** and any **features**. Resource needs can be raised
  later with a *Modify namespace* request. **Start here** unless you know you need
  otherwise.
- **DevSpace** — a development environment tied to **one person**; it cannot be shared.
  Choosing it ends the form. There is a separate how-to for DevSpaces.
- **Customized namespace (expert mode)** — you specify every technical and resource
  parameter yourself. Everything below the Features section applies only to this path.

{{< note >}}
**Basic is not a downgrade.** It is the same platform with sensible defaults, and a later
*Modify namespace* request raises the limits. Pick expert mode when you already know the
numbers, not to keep your options open.
{{< /note >}}

## Features (all paths)

Optional add-ons, each a checkbox:

- **Create container private registry for this namespace** — gives you your own private
  registry (a Harbor project) for this namespace.
- **Proxy access** — lets the namespace reach your local proxy to pull external
  resources, e.g. artefacts consumed by a BuildConfig.
- **EgressIP** — lets the namespace reach external resources through a **dedicated IP
  address**.
- **Custom robot account** — a machine account for automated CI/CD. Describe the
  privileges it needs in **"Further details"**.

{{< warning >}}
"Harbor **project**" is Harbor's own word for a registry namespace. It is **not** a layer
in the {{< param product_short >}} tenancy model — that is still just **Tenant →
Namespaces**, as A06 said.
{{< /warning >}}

If you chose **basic**, you are done here. The rest is expert mode.

## Expert mode: namespace usage — DEV or PROD

The DEV/PROD distinction from A06, now as a form field:

- **Development** — fewer policies, higher tolerance for insecure images, but **no service
  exposure**.
- **Production** — stronger policies, lower tolerance for insecure images, but **allows
  service exposure**.

The form marks both options as **requiring an ARD** — the architecture/design record for
the application that will run there. This field is the mechanism behind the note in A03:
a Route needs a PROD namespace. Details:
[DEV and PROD namespaces]({{< param dcs_docs_base_url >}}/concepts/dev-and-prod-namespace).

## Expert mode: operators

Optionally enable **operators** for the namespace. The available list grows over time, so
read the current one in the form rather than memorising it.

## Expert mode: capacity tiers

Pre-defined sizes, if you would rather not hand-tune every number:

- **16 CPU – 64 GB RAM**
- **32 CPU – 128 GB RAM**
- **48 CPU – 256 GB RAM**

Standard ResourceQuotas are applied to all operator and DevSpace requests anyway.

## Expert mode: resources

The individual quota values. **If you are unsure, keep the defaults** — that is the
documented advice, not a shortcut.

| Field | What it controls | Range |
|---|---|---|
| **CPU limits** | Absolute maximum CPU all containers in the namespace may consume together — stops one namespace starving others on the cluster. | 10 – 20000 millicores |
| **CPU requests** | CPU pre-reserved for the namespace; determines how many Pods the scheduler can fit in. | 10 – 2000 millicores |
| **Memory limits** | Upper boundary of RAM. Once the containers' sum would exceed it, the namespace cannot scale further. | 10 – 81920 MB |
| **Memory requests** | Guaranteed minimum RAM reserved — the baseline that keeps workloads stable. | 10 – 8192 MB |
| **Requests ephemeral storage** | Local, temporary node disk (logs, caches) all Pods may claim. | 1 – 20 GB |
| **Total storage requests** | Cumulative capacity of all PVCs in the namespace — the overall footprint cap on external storage. | 1 – 500 GB |
| **OpenShift image storage** | Disk used by the namespace's ImageStreams in the integrated OpenShift registry. | 1 – 20 GB |
| **Individual PVC storage max** | Blocks any *single* volume request above this size ("no single disk larger than 100Gi"). | 1 – 500 GB |
| **Individual PVC storage min** | Forces every volume request to a baseline size, so storage is not fragmented into tiny chunks. | 1 – 250 GB |
| **Image repository max space** | Cap on the total size of images pushed to the namespace's Harbor registry, to prevent bloat. | 10 – 100 GB |

{{< note >}}
**Limits vs requests** — the same pair you will meet on every Pod. A **request** is
reserved for you and drives scheduling; a **limit** is the ceiling you may not cross.
Requests are what you are guaranteed, limits are what you are allowed.
{{< /note >}}

## Others

Same as the tenant request: **"Further details"** takes any question or extra wish. The
docs explicitly ask for feedback on whether this level of freedom helps or just
overwhelms — say so there.

{{< note >}}
**Full reference:** the
[how-to for requesting a container Namespace]({{< param dcs_docs_base_url >}}/how-to/request-a-container-namespace)
in the {{< param product_short >}} docs.
{{< /note >}}
