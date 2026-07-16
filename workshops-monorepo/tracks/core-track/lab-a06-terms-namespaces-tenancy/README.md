# Terms — Namespaces & Tenancy

**The words you keep hearing — Namespace, Tenant, DEV/PROD — and namespace isolation shown for real, not just described.**

You've been deploying into a namespace since your first lab without a name for it. This
lab names it, then makes isolation concrete: you deploy the *same* app into two
namespaces at once and watch identical names coexist and actions stay contained. Then it
places the namespace in the DCS **Tenant → Namespaces** model and names the DEV/PROD
namespace types — the vocabulary the Developer track builds its deep model on.

- **Track:** Core / Fundamentals · Lab 6
- **Audience:** Beginner — comfortable deploying with `oc`
- **Duration:** ~30 min
- **Format:** Hands-on, guided — split terminal, two pre-provisioned peer namespaces
- **Prerequisites:** A02 (Deploy Your First App).

## By the end of this lab you'll be able to

- Define a Namespace and identify your active one.
- Deploy one app into two namespaces and explain the isolation you observe.
- List concrete reasons to run multiple namespaces.
- Explain the Tenant → Namespaces model (and why there's no "project" layer).
- Say that DEV and PROD namespace types exist and differ.

## What you'll do

Deploy the same `hello` Deployment into two namespaces from one manifest, prove the names
don't clash and a change in one doesn't touch the other, then map namespaces onto tenants
and namespace types. Vocabulary that finally has evidence behind it.
