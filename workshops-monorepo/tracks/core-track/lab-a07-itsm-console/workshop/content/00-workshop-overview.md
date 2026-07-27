---
title: "Requesting a Tenant & Namespace via ITSM"
---

Six labs in, you have deployed, configured, exposed and persisted — always inside a
namespace that was simply *there*. This lab, part of **{{< param product_name >}}**, shows
where that namespace comes from: you **request** it through ITSM, and this is what the
form asks you.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide).
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Find **your** myITSM portal — there is one per location (DIV, DE, ES, …), and a Tenant
  must be requested in the portal of its own location.
- Fill in a **New tenant** request: owner, name, members, siglum, location, billing and
  the export-control declaration.
- Fill in a **New namespace** request, and choose between **basic**, **DevSpace** and
  **customized (expert)** — including what every resource field means.
- Explain **why the form asks so much**: {{< param product_short >}} onboarding is
  automated, and ITSM is currently the input form for that automation.
- Tell which actions are **self-service with `oc`** and which need a request.

## Prerequisites

- **A06 — Terms: Namespaces & Tenancy.** This lab assumes the **Tenant → Namespaces**
  model and the **DEV/PROD** namespace types. It also explains the "you'll need a request
  for that" notes from A03 (a Route needs a PROD namespace) and A04 (S3 comes via a
  request).

## Your Environment

A browser-based session with an **editor** for the sorting worksheet. The ITSM portals
live outside the lab environment, so this lab is a guided walkthrough of the forms — no
cluster actions are required and nothing here changes your session.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Beginner
