---
title: Self-Service vs Requests
---

The general rule: **anything inside your namespace, you do yourself; anything that
changes your entitlements or the shared platform, you request.**

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/self-service
```

## You do it yourself (with `oc`)

- **Deploy / scale / restart** workloads (A01).
- **Configure** with ConfigMaps and Secrets (A02).
- **Expose** an app with a Service and, in a PROD namespace, a Route (A03).
- **Claim storage** with a PVC (A04).

These are self-service because they live *within* the rights and quota you already have.

## You request it (ITSM ticket)

- **Quota increase** — more CPU/memory/storage than your namespace budget.
- **Image mirroring** — pulling an external image into Harbor (A04 introduced the air-gap).
- **New repos / catalogs** in Harbor.
- **S3 bucket** — object storage (A04: not a PVC).
- **Security exception** — anything that departs from the default policy.

These touch entitlements, the shared registry, or governance — so they go through
**approval**. See the
[{{< param product_short >}} requests guide]({{< param dcs_docs_base_url >}}/getting-started/requests).

{{< note >}}
The ticketed items are exactly the "you'll need a request for that" notes from A03 and
A04. This lab explains what those requests are and where you make them.
{{< /note >}}
