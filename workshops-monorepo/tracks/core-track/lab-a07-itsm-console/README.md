# Requesting a Tenant & Namespace via ITSM

**Every namespace you have used so far was simply there. This lab shows where it comes from — and what the request form actually asks you.**

DCS is multi-national, so there is no single ITSM portal. Each location (DIV, DE, ES, …) has
its own **myITSM**.

A **Tenant** must be requested in the portal of its own location — and it cannot be moved
afterwards.

This lab walks the whole path:

- find the **right portal**;
- the **New tenant** request — the fields, then billing and export control;
- the **New namespace for existing tenant** request;
- the **self-service vs request** line.

Deliberately a **quick-start**, not a reference. The namespace page steers to the *basic*
option and leaves expert mode — operators, capacity tiers, the ten quota fields — as a
pointer to the docs.

> **📌 Note:** the form has many options because DCS onboarding is **automated**. ITSM is
> currently the input form for that pipeline; the missing piece is the self-service
> frontend, not the provisioning.

- **Track:** Core / Fundamentals
- **Audience:** Beginner — you've done the **Terms — Namespaces & Tenancy** lab
- **Duration:** ~20 min
- **Format:** Quick-start walkthrough of the two request forms + sorting worksheet + knowledge check
- **Prerequisites:** the **Terms — Namespaces & Tenancy** lab.

## By the end of this lab you'll be able to

- Find your own myITSM portal and explain why a Tenant is per location and non-movable.
- Fill in a New tenant request: the seven fields, plus billing and export control.
- Fill in a New namespace request and know why basic is the right default.
- Explain why the form has so many options: the onboarding is automated and the fields feed it.
- Tell which actions are self-service with `oc` and which need a request.
