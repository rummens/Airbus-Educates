# Requesting a Tenant & Namespace via ITSM

**So far your namespaces were created for you. This lab shows how to request one, and what each field on the request form means.**

DCS is multi-national, so there is no single ITSM portal. Each location (DIV, DE, ES, …) has
its own **myITSM**.

A **Tenant** must be requested in the portal of its own location — and it cannot be moved
afterwards.

This lab walks the whole path:

- find the **right portal**;
- the **New tenant** request — the fields, then billing and export control;
- the **New namespace for existing tenant** request;
- the **self-service vs request** line.

This lab is a **quick-start**, not a full reference. The namespace page recommends the
*basic* option and points to the docs for expert mode (operators, capacity tiers, the ten
quota fields).

> **📌 Note:** the form has many options because DCS onboarding is **automated**. ITSM is
> currently the input form for that pipeline. Provisioning is already automated; only the
> self-service frontend is still missing.

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
