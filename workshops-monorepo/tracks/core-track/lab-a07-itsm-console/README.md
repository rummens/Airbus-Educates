# Requesting a Tenant & Namespace via ITSM

**Every namespace you have used so far was simply there. This lab shows where it comes from — and what the request form actually asks you.**

DCS is multi-national, so there is no single ITSM portal: each location (DIV, DE, ES, …)
has its own myITSM, and a Tenant must be requested in the portal of its own location — it
cannot be moved afterwards. This lab finds the right portal, walks the **New tenant**
request and the **New namespace for existing tenant** request field by field, explains the
basic / DevSpace / customized fork and every resource quota behind it, and closes with the
self-service vs request line.

The forms are long because DCS onboarding is **automated on the DCS side** — ITSM is
currently the input form for that pipeline; the missing piece is the self-service
frontend, not the provisioning.

- **Track:** Core / Fundamentals · Lab 7
- **Audience:** Beginner — you've done A06
- **Duration:** ~20 min
- **Format:** Guided walkthrough of the two request forms + sorting worksheet + knowledge check
- **Prerequisites:** A06 (Terms — Namespaces & Tenancy).

## By the end of this lab you'll be able to

- Find your own myITSM portal and explain why a Tenant is per location and non-movable.
- Fill in a New tenant request: owner, name, members, siglum, purpose, location, billing, export control.
- Fill in a New namespace request and choose between basic, DevSpace and customized (expert) — including what every quota field means.
- Explain why the form asks so much: the onboarding is automated and the fields feed it.
- Tell which actions are self-service with `oc` and which need a request.
