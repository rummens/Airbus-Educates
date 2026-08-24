# Terms — Namespaces & Tenancy

**The words you keep hearing — Namespace, Tenant, DEV/PROD — and namespace isolation shown for real, not just described.**

You have been deploying into a **namespace** since your first lab, without a name for it.

This lab names it, then makes **isolation** concrete: you deploy the *same* app into two
namespaces at once, and watch identical names coexist while actions stay contained.

Then it places the namespace in the DCS **Tenant → Namespaces** model and names the
**DEV**/**PROD** namespace types — the vocabulary the Developer track builds its deep model
on.

- **Track:** Core / Fundamentals
- **Audience:** Beginner — comfortable deploying with `oc`
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, two pre-provisioned peer namespaces
- **Prerequisites:** the **Deploy Your First App** lab.

## By the end of this lab you'll be able to

- Define a Namespace and identify your active one.
- Deploy one app into two namespaces and explain the isolation you observe.
- List concrete reasons to run multiple namespaces.
- Explain the Tenant → Namespaces model (and why there's no "project" layer).
- Say that DEV and PROD namespace types exist and differ.

## What you'll do

1. **Deploy** the same `hello` Deployment into two namespaces from one manifest.
2. **Prove** the names do not clash, and that a change in one does not touch the other.
3. **Map** namespaces onto tenants and namespace types.

Vocabulary that finally has evidence behind it.
