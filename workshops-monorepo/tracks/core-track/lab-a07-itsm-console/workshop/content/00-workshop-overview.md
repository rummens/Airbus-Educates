---
title: "Requesting a Tenant & Namespace via ITSM"
---

In the earlier labs you deployed, configured, exposed and stored data for an app, always in
a namespace that was created for you. This lab, part of **{{< param product_name >}}**,
shows where that namespace comes from: you **request** it through ITSM.

{{< note >}}
**💡 The short version, in case you only read this page:** find your national myITSM portal →
request a **Tenant** (about seven fields) → request a **Namespace** if you need a second
one (three fields, then pick *basic*). {{< param product_short >}} provisions the rest
automatically. The pages below walk through those fields one by one.
{{< /note >}}

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help).
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Find **your** myITSM portal — there is one per location (DIV, DE, ES, …), and a Tenant
  must be requested in the portal of its own location.
- Fill in a **New tenant** request: the seven fields, plus billing and export control.
- Fill in a **New namespace** request and know why **basic** is the right default.
- Explain **why the form has so many options**: {{< param product_short >}} onboarding is
  automated, and ITSM is currently the input form for that automation.
- Tell which actions are **self-service with `oc`** and which need a request.

## Prerequisites

- **Terms — Namespaces & Tenancy.** This lab assumes the **Tenant → Namespaces**
  model and the **DEV/PROD** namespace types. It also explains the "you'll need a request
  for that" notes from the **Expose Your App** lab (a Route needs a PROD namespace) and the **Storage** lab (S3 comes via a
  request).

## Your Environment

A browser-based session with an **editor** for the sorting worksheet. The ITSM portals
live outside the lab environment, so this lab is a guided walkthrough of the forms — no
cluster actions are required and nothing here changes your session.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Beginner
