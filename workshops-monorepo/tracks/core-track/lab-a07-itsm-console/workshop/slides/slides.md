<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Requesting a Tenant & Namespace via ITSM

Every namespace you have used so far was simply there. This lab shows where it comes from — and how to get your own quickly.

**The short version:** find your national myITSM portal, request a **Tenant**, request a **Namespace** if you need a second one. DCS provisions the rest automatically.

Digital Container Service · DCS Academy

---

<!-- id: portals -->
## Find Your ITSM Portal

DCS is multi-national: **each location has its own myITSM portal** (DIV, DE, ES, …). There is no single central form.

- A Tenant is requested **per location**, in that location's own portal.
- You can only pick locations **inside your own domain**.
- Once created, a Tenant **cannot be moved**.
- The portal list lives on the docs page *ITSM requests → Service Requests*.
- Every request starts with one radio list — **New tenant — Do this first!** and **New namespace for existing tenant** are the two this lab covers.

![Pick your national myITSM portal, request a tenant, then request namespaces; DCS provisions them automatically](request-flow.svg)

---

<!-- id: tenant -->
## Request a Tenant — the Fields

Do this **once**. Tenant → Namespaces, the model from the **Terms — Namespaces & Tenancy** lab — the Tenant is who is accountable and what gets recharged.

- **Tenant owner** — the person responsible for security, sizing and finance; not necessarily you.
- **Tenant name** — lowercase, digits, `-` (Kubernetes naming convention).
- **Namespace members** — one e-mail address per line.
- **Siglum** — your department or project.
- **Purpose** — a sentence or two on what you'll use it for.
- **New namespace name** — optional; names the default namespace the Tenant comes with.
- **Preferred tenant location** — the cluster; the list differs per ITSM, and the choice is permanent.

Names get a **random suffix** for uniqueness — use the name you get back.

---

<!-- id: tenant-extras -->
## Request a Tenant — Billing & Export Control

The rest of the tenant form. For most first-time requests, under a minute.

- **Billing** (WBS project code, CC siglum, facts code, IWO) — only if recharging applies to you, i.e. medium and large requests. Otherwise leave it empty.
- **Export control / ITAR** — declare whether you plan to put EC or ITAR data in.
- DCS **can** host such data; if you answer yes, notify your **local Export Control team**. A notification duty, not a rejection.
- **Further details** — free text for anything the form doesn't cover, or any field you were unsure about.
- Then submit. Provisioning is **automated** — nobody builds your tenant by hand.

---

<!-- id: namespace -->
## Request a Namespace

Only needed from the **second** namespace onwards — your Tenant already came with one.

- **Three fields:** existing tenant name (with its suffix) · namespace members, one per line · new namespace name.
- ✅ **Pick "Basic standard namespace"** — pre-configured and standard-sized; you are then asked only for usage and features. Raise limits later with *Modify namespace*.
- **DevSpace** is a personal environment for one person; **customized (expert)** means setting every quota by hand.
- **Usage:** Development (fewer policies, no service exposure) or Production (stronger policies, exposure allowed — the reason the **Expose Your App** lab's Route needs PROD).
- **Features**, all optional: private Harbor registry · proxy access · EgressIP · custom robot account.

---

<!-- id: self-service -->
## Self-Service vs Requests

The rule: anything **inside your namespace** you do yourself; anything that changes your **entitlements or the shared platform** you request.

- **Self-service with `oc`:** deploy, scale, restart · ConfigMaps and Secrets · Service and Route (PROD namespace) · PVCs.
- **ITSM request:** new Tenant or Namespace · modify/delete · user management · quota increase · image mirroring · Harbor repos · S3 bucket · networking whitelist · security exception.
- The form is long because DCS onboarding is **automated** — ITSM is the input form for that pipeline until the self-service frontend exists.

---

<!-- id: close -->
## What's Next

You can now onboard yourself onto DCS end to end and tell requests from self-service.

- One portal **per location**; a Tenant cannot move.
- **Tenant first**, then namespaces; the Tenant brings one default namespace.
- **Basic** unless you already know your numbers.

The **Console track** does the same work in the OpenShift web console; the **Developer track** covers **RBAC, Tenancy & Namespaces** and **DEV vs PROD Namespaces & Policies**.
