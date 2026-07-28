---
title: Self-Service vs Requests
---

You now know how to get a Tenant and a Namespace. This page draws the general line, so you
know when to reach for `oc` and when to open ITSM.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/self-service
```

The rule: **anything inside your namespace, you do yourself; anything that changes your
entitlements or the shared platform, you request.**

## You do it yourself (with `oc`)

- **Deploy / scale / restart** workloads (A01).
- **Configure** with ConfigMaps and Secrets (A02).
- **Expose** an app with a Service and, in a PROD namespace, a Route (A03).
- **Claim storage** with a PVC (A04).

Self-service, because these live *within* the rights and quota you already have.

## You request it (ITSM)

- **A new Tenant** or a **new Namespace** — this lab.
- **Modify or delete** a tenant or namespace, and **user management**.
- **Quota increase** — more CPU/memory/storage than your namespace budget (a *Modify
  namespace* request).
- **Image mirroring** — pulling an external image into Harbor (A04's air-gap).
- **New repos / catalogs** in Harbor, and an **S3 bucket** (A04: not a PVC).
- **Networking whitelist** and **security exceptions**.

These change entitlements, the shared registry, or governance — so they go through the
request pipeline.

## Sort them yourself

Open the worksheet and decide, for each task, which side it falls on:

```editor:open-file
file: ~/exercises/self-service-vs-ticket.md
```

Decide each one before you reveal the answers.

{{< note >}}
**Self-service via `oc`:** scale a Deployment · create a ConfigMap · expose an app with a
Route (in a PROD namespace) · create a PVC.

**Raise an ITSM request:** request a new Tenant · request a second Namespace · increase
your namespace quota · mirror an external image to Harbor · request an S3 bucket · add a
new Harbor catalog/repo · request a security exception.
{{< /note >}}

## Quick check

You need 2 more CPU cores than your namespace allows for a load test. `oc` or ITSM?

{{< note >}}
**Answer:** **ITSM** — a quota increase changes your entitlement, so it goes through a
*Modify namespace* request. Deploying the load test itself, once you have the quota, is
self-service.
{{< /note >}}
