---
title: The Compliance Workflow
---

You've now seen the pieces separately — classification, placement, the RACI split, and the
exception process. This page ties them into the single **loop** a tenant actually follows to
keep a workload compliant. No new commands here: it's the mental model to leave with.

## The tenant compliance loop

1. **Classify the data.** Decide the classification of the data your workload handles, using the
   scheme from page 1. This is a tenant duty — only you know what your workload processes.
2. **Tag the workload.** Record that classification on the workload — the
   `data.dcs/classification` annotation you saw on page 2 — so the intent travels with the spec.
3. **Place it in a permitted region.** Add the region `nodeSelector` (or affinity) that matches
   an allowed region for that classification. The scheduler and platform policy enforce it
   against the region labels the platform advertises.
4. **Request an exception if you can't comply.** When a control genuinely can't be met, raise a
   governed **Security Exception** as an
   **[ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests)** — reviewed,
   time-boxed, approved. Not a config toggle.
5. **Renew or close.** Exceptions expire. Renew while the need stands, close it when the
   workload can meet the control again — and the loop returns to steady state.

## Where each piece came from

- Steps 1 is the **classification matrix** (page 1) — the residency guarantee that keeps each
  classification in its region.
- Steps 2–3 are **placement expressed in the spec** (page 2) — annotation plus region
  `nodeSelector`.
- Steps 4–5 are the **RACI split and the exception process** (page 3) — the tenant requests,
  the platform reviews and approves.

## Why it works this way

{{< param product_short >}} is operated through a **service-management (ITSM)** workflow rather
than ad-hoc cluster admin: quota increases, image mirroring, and **security exceptions** are all
**Service Requests**, so every deviation from the baseline is *requested, reviewed, and
recorded*. Combined with the air-gapped, regional platform, that's what turns "we promise your
data stays in-region" into something auditable: classification says where data may live,
placement expresses it, RACI says who owns each step, and the exception process is the one
governed door for anything that doesn't fit.

{{< note >}}
The **ITSM request** workflow is the self-service channel for governed changes on
{{< param product_short >}} — see
[{{< param product_short >}} ITSM requests]({{< param dcs_docs_base_url >}}/support/itsm-requests).
In a lab we model the *outcome*; the real request goes through the ticketing system.
{{< /note >}}
