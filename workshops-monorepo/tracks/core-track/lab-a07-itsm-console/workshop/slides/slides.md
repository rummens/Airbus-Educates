<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Requesting a Tenant & Namespace via ITSM

Every namespace you have used so far was simply there. This lab shows where it comes from: you request it through ITSM, and this is what the form asks you.

**In this lab:** find your myITSM portal · request a Tenant · request a Namespace · understand every input · tell self-service from requests.

Digital Container Service · DCS Academy

---

<!-- id: portals -->
## Find Your ITSM Portal

DCS is multi-national: **each location has its own myITSM portal** (DIV, DE, ES, …). There is no single central form.

- A Tenant must be requested **for each location separately**, in that location's portal.
- You can only pick locations **inside your own domain**.
- Once created, a Tenant **cannot be moved**.
- The list of portals lives on the docs page *ITSM requests → Service Requests*.
- Every request starts with one radio list: **New tenant — Do this first!**, **New namespace for existing tenant**, modify/delete, user management, whitelist, and more.

![Pick your national myITSM portal, request a tenant, then request namespaces; DCS provisions them automatically](request-flow.svg)

---

<!-- id: tenant -->
## Request a Tenant

Do this **once**. Tenant → Namespaces, the model from A06 — the Tenant is who is accountable and what gets recharged.

- **Tenant owner** — the person responsible (security, sizing, finance); not necessarily you.
- **Tenant name** — Kubernetes naming convention: lowercase, digits, `-`.
- **Namespace members** — one e-mail address per line.
- **Siglum · purpose · preferred location** — the location list differs per ITSM, and the choice is permanent.
- **New namespace name** — optional; names the default namespace the Tenant comes with.
- **Billing** (WBS, CC siglum, facts code, IWO) only if recharging applies · **Export control / ITAR** must be declared, and your local EC team notified.
- Names get a **random suffix** for uniqueness — use the name you get back.

---

<!-- id: namespace -->
## Request a Namespace

For every namespace after the Tenant's default one. Three paths — pick the first that fits.

- **Basic standard namespace** — pre-configured and standard-sized; only usage and features asked. Raise limits later with *Modify namespace*.
- **DevSpace** — tied to one person, cannot be shared; choosing it ends the form.
- **Customized (expert)** — you specify everything: DEV/PROD usage, operators, capacity tier (16/32/48 CPU), and the quotas (CPU, memory, ephemeral and PVC storage, image storage, Harbor space).
- **Features** on any path: private Harbor registry · proxy access · EgressIP · custom robot account.
- Unsure about a field? **Keep the default** and ask in *Further details*.

---

<!-- id: self-service -->
## Self-Service vs Requests

The rule: anything **inside your namespace** you do yourself; anything that changes your **entitlements or the shared platform** you request.

- **Self-service with `oc`:** deploy, scale, restart · ConfigMaps and Secrets · Service and Route (PROD namespace) · PVCs.
- **ITSM request:** new Tenant or Namespace · modify/delete · user management · quota increase · image mirroring · Harbor repos · S3 bucket · networking whitelist · security exception.
- The forms are long because DCS onboarding is **automated** — ITSM is the input form for that pipeline until the self-service frontend exists.

---

<!-- id: close -->
## What's Next

You can now onboard yourself onto DCS end to end and tell requests from self-service.

- One portal **per location**; a Tenant cannot move.
- **Tenant first**, then namespaces; the Tenant brings one default namespace.
- **Basic** unless you know your numbers.

The **Console track** does the same work in the OpenShift web console; the **Developer track** covers RBAC (**B05**) and DEV vs PROD by policy (**B06**).
