# Module A — Core / Fundamentals (Core)

The shared core every learner completes before any track. **Reworked (2026-07-16)** around two principles:

1. **Quick win first** — get a learner's own app running on DCS as fast as possible, then layer concepts onto that working app.
2. **Theory folded into labs** — concepts are explained inline, in the step that needs them (with an examiner check + a knowledge check per workshop), not as separate concept-only pages or standalone theory workshops.

Depth that used to live in Core — the Harbor deep-dive, tenancy/RBAC internals, the DEV/PROD policy model, operators — **moves to the Developer track (Module B)**. Core keeps only the vocabulary and the hands-on happy path. Sequential — each workshop builds on the last.

> **Restructure note.** This breakdown is the new *target* design. The current built-and-tested workshops (`workshops-monorepo/tracks/core-track/lab-a01…a09`) still reflect the old 9-workshop Foundations. The mapping from old → new and the refactor/rename work is tracked in [tasks.md](tasks.md#module-a--core--fundamentals-restructure).

## Workshop Structure Conventions

Each entry lists: **Covers ideas** (topic numbers from `course-topics.md`), **Type**, **Prerequisites**, **Learning objectives**, **Narrative arc**, **Code exercises**, **Key code examples**, and **Source** (which built workshop(s) the content is drawn from). Workshop names: `lab-a0N-name`. All follow the house standards (intro page, `oc`, hybrid doc links, param trio, air-gapped images, examiner + knowledge check).

---

### Workshop A01: What is DCS?

**Directory name:** `lab-a01-what-is-dcs`
**Detailed plan:** [workshop-plans/lab-a01-what-is-dcs.md](workshop-plans/lab-a01-what-is-dcs.md)
**Covers ideas:** 1
**Type:** Core
**Prerequisites:** None
**Source:** old A01, **trimmed** — the OpenShift console tour moves out to A08.
**Learning objectives:** Explain what DCS is and where it fits (on-prem, air-gapped, multi-national, OpenShift-based); describe containers and images at a high level; state **why Kubernetes over plain Docker** for running apps; navigate the workshop session (terminal, editor, `oc`).
**Narrative arc:** DCS mission + who it's for → benefits (air-gapped, sovereign, managed) → containers/images primer → **why K8s, not just Docker** (scheduling, self-healing, scaling, declarative) → quick tour of the session so the learner is ready to deploy in A02.
**Code exercises:** First `oc` commands (`oc whoami`, `oc get project`); observe the pre-provisioned namespace. Mostly orientation.
**Key code examples:** Basic `oc` inspection. Links: DCS mission/benefits → `{{< param dcs_docs_base_url >}}`; containers/K8s → upstream. ~15m — deliberately light; the console tour is now its own lab (A08).

### Workshop A02: Deploy Your First App *(the quick win)*

**Directory name:** `lab-a02-deploy-first-app`
**Detailed plan:** [workshop-plans/lab-a02-deploy-first-app.md](workshop-plans/lab-a02-deploy-first-app.md)
**Covers ideas:** 2, 7
**Type:** Core
**Prerequisites:** A01
**Source:** merge of old A02 (Kubernetes Essentials) + old B01 (Deploy First App). **Hybrid style.**
**Learning objectives:** Deploy an existing image to a namespace; customise it with environment variables; reach it locally; change config and roll out an update; read the YAML behind what you created.
**Narrative arc:** "Let's get something running." → `oc create deployment` from a Harbor image → customise with `oc set env` → reach it with a local `curl` (session proxy / port-forward) → change an env var and watch the rollout → **then reveal the generated YAML** (Deployment → ReplicaSet → Pod ownership, labels/selectors) to bridge imperative → declarative.
**Code exercises:** `oc create deployment` (image from `{{< param dcs_registry >}}`); `oc set env`; `oc get`/`describe`; local `curl`; edit env → observe rollout; `oc get deploy -o yaml` to reveal the manifest. Examiner checks each step.
**Key code examples:** Imperative `oc create/set env/expose`; the revealed Deployment YAML. Constructs (Deployment/ReplicaSet/Pod) → upstream; DCS registry framing → `dcs_docs_base_url`.

### Workshop A03: Configure & Troubleshoot Your App

**Directory name:** `lab-a03-configure-troubleshoot`
**Detailed plan:** [workshop-plans/lab-a03-configure-troubleshoot.md](workshop-plans/lab-a03-configure-troubleshoot.md)
**Covers ideas:** 8, 10
**Type:** Core
**Prerequisites:** A02
**Source:** folds old B02 (Config & Secrets) + old B04 (Debugging & Logs).
**Learning objectives:** Externalise config via a ConfigMap; inject a Secret safely; roll out a config change; diagnose a failing workload from logs, events, and `describe`, and fix it.
**Narrative arc:** Env vars don't scale → move config to a ConfigMap, add a Secret → roll out → **then it breaks** (pre-seeded fault) → inspect `oc logs`/`describe`/`get events` → identify → fix → verify. "Observe and diagnose" style.
**Code exercises:** Create ConfigMap/Secret, wire via env/volume, trigger rollout; then repair a deliberately broken manifest using logs/events/describe. Examiner confirms both the config change and the recovery.
**Key code examples:** ConfigMap/Secret wiring; a broken manifest the learner fixes. Constructs → upstream.

### Workshop A04: Expose Your App

**Directory name:** `lab-a04-expose-app`
**Detailed plan:** [workshop-plans/lab-a04-expose-app.md](workshop-plans/lab-a04-expose-app.md)
**Covers ideas:** 6
**Type:** Core
**Prerequisites:** A02
**Source:** old A06 (Networking), reframed to "expose properly".
**Learning objectives:** Understand Service → Route → external load balancer; expose an app with a **real Route** on DCS-managed DNS (reachable outside the session), and also surface it **inside the session as a new dashboard tab**; know that a **Route requires a PROD-type namespace** (the "why" is the Developer track's DEV/PROD lab).
**Narrative arc:** A Pod isn't reachable → add a Service → **expose it for real** with a Route into a pre-provisioned PROD-type namespace (DCS DNS, external LB) → open it in a browser outside the session **and** as a new in-session dashboard tab → note "Routes need a PROD-type namespace — you'll see why in the Developer track."
**Code exercises:** Create a Service; create a Route (`host` on DCS DNS) in a PROD-type namespace; reach the app externally; add the app URL as a **session dashboard tab**; examiner checks the Route resolves and responds.
**Key code examples:** Service + Route YAML; session dashboard-tab config pointing at the Route. Route/Service → upstream; DCS DNS/LB + PROD-namespace requirement → `{{< param dcs_docs_base_url >}}/concepts/networking`.
**Config note:** Needs a **PROD-type namespace** provisioned for the Route. Educates' default session role excludes routes — grant routes via a Role+RoleBinding in `session.objects` (as fixed in the old A06). Add the Route URL as a dashboard tab.

### Workshop A05: Storage

**Directory name:** `lab-a05-storage`
**Detailed plan:** [workshop-plans/lab-a05-storage.md](workshop-plans/lab-a05-storage.md)
**Covers ideas:** 6b
**Type:** Core
**Prerequisites:** A02
**Source:** old A07 (Storage) + old B05 (Stateful Storage).
**Learning objectives:** Request storage with a PVC; distinguish DCS **File vs Block** storage classes; prove data persists across a restart; know classification drives SC choice and S3 comes via ITSM.
**Narrative arc:** The app loses data on restart → request a PVC (SC name via variable) → mount it → write data → restart → confirm persistence → understand File vs Block and S3-via-ticket.
**Code exercises:** Apply a PVC (`{{< param dcs_sc_file >}}`), mount, write, restart, confirm; challenge with a Block PVC. Examiner confirms persistence.
**Key code examples:** PVC + volume mount using variable SC names. PV/SC → upstream; DCS storage → `{{< param dcs_docs_base_url >}}/concepts/storage`.
**Config note:** Params `dcs_sc_file`, `dcs_sc_block`.

### Workshop A06: Terms — Namespaces & Tenancy

**Directory name:** `lab-a06-terms-namespaces-tenancy`
**Detailed plan:** [workshop-plans/lab-a06-terms-namespaces-tenancy.md](workshop-plans/lab-a06-terms-namespaces-tenancy.md)
**Covers ideas:** 3 (light), 5 (light)
**Type:** Core
**Prerequisites:** A02
**Source:** the *vocabulary* layer of old A03 (Namespace model) + old A05 (Access & Tenancy). **Deep model → Developer track (B05/B06).**
**Learning objectives:** Define the key DCS terms a learner will keep hearing — **Namespace** (what it is and why it exists / what makes one active), **Tenant** (Tenant → Namespaces, no separate "project" layer), and the existence of **DEV vs PROD** namespace types; read their own namespace context.
**Narrative arc:** "You've been working in a namespace — what is it?" → namespace as the unit of isolation/consumption (NaaS) → Tenant → Namespaces model → DEV/PROD types exist (details deferred to the Developer track) → find your own place (`oc project`, `oc get`).
**Code exercises:** Inspect current namespace/context; list what's in it; identify the tenant. Vocabulary + observe — no deep RBAC/policy here.
**Key code examples:** `oc project`, `oc get`, context inspection. DCS-specific: `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access` (overview only).

### Workshop A07: The ITSM Console — Self-Service on DCS

**Directory name:** `lab-a07-itsm-console`
**Detailed plan:** [workshop-plans/lab-a07-itsm-console.md](workshop-plans/lab-a07-itsm-console.md)
**Covers ideas:** 5 (self-service flow)
**Type:** Core
**Prerequisites:** A01
**Source:** new — the ITSM-request material previously scattered as blurbs across old A04/A05/A07.
**Learning objectives:** Know that DCS self-service runs through **ITSM requests** and where to find it; identify which actions require a ticket (quota increases, image mirroring, new repos/catalogs, S3, security exceptions) vs which are self-service via `oc`.
**Narrative arc:** "You can't just click everything — some things are requests." → tour the ITSM console → walk one representative request (e.g. a quota increase or an image-mirror request) → know the request → approval → provisioning loop.
**Code exercises:** Guided tour of the ITSM console (screenshot-driven / embedded tab if feasible); map a short list of tasks to "self-service" vs "raise a ticket".
**Key code examples:** None (console tour). DCS-specific: `{{< param dcs_docs_base_url >}}/getting-started/requests`.
**Config note:** ITSM console likely not reachable in an air-gapped session — deliver as an annotated, screenshot-driven tour (spike embeddability).

### Workshop A08: The OpenShift Console — A Guided Tour

**Directory name:** `lab-a08-openshift-console`
**Detailed plan:** [workshop-plans/lab-a08-openshift-console.md](workshop-plans/lab-a08-openshift-console.md)
**Covers ideas:** 2 (console parity)
**Type:** Core
**Prerequisites:** A02
**Source:** the console tour split out of old A01.
**Learning objectives:** Navigate the OpenShift web console and map its views to the `oc` commands already learned (workloads, networking, storage, config); know when the console is the faster tool.
**Narrative arc:** "Everything you did with `oc` has a UI." → tour perspectives, Workloads, Networking (the Route from A04), Storage (the PVC from A05), ConfigMaps/Secrets → `oc` ↔ console parity → when to reach for which.
**Code exercises:** Console tour with `oc` parity call-outs against the app the learner already deployed (A02) and exposed (A04).
**Key code examples:** `oc` ↔ console mapping. Console/perspectives → upstream. *(Console-embedding constraints: see [educates-openshift-console-limitation]; deliver per that finding.)*

## Notes

- **A01–A05 are the happy path**: what is DCS → deploy → configure/fix → expose → persist. This is the "quick win, theory folded in" spine. Keep them hands-on and tight.
- **A06–A08 are orientation**: vocabulary (A06) and the two console tours (A07 ITSM, A08 OpenShift), placed last as "now you know the landscape / next steps."
- Deep DCS concepts (Harbor internals, RBAC internals, DEV/PROD policy enforcement, operators) are **no longer in Core** — they are Developer-track workshops (Module B). Core teaches the terms; the Developer track teaches the mechanisms.
- Foundations remains the prerequisite for all tracks.

## Old → New mapping (for the refactor)

| Old Core workshop | New home |
|---|---|
| A01 What is DCS? | **A01** (trim console tour → A08) |
| A02 Kubernetes Essentials | **A02** (merge with old B01, hybrid style) |
| A03 Namespace model (vcluster) | **A06** vocabulary (light) + **B06** DEV/PROD policies (deep) |
| A04 Working with Harbor | **B04** Harbor & scanning |
| A05 Access & Tenancy | **A06** vocabulary (light) + **B05** RBAC/Tenancy (deep) |
| A06 Networking | **A04** Expose your app |
| A07 Storage | **A05** Storage |
| A08 RBAC Deep Dive | **B05** RBAC, Tenancy & Namespaces |
| A09 Operators | **B08** Operators |
| old B01 Deploy First App | folded into **A02** |
| old B02 Config & Secrets | folded into **A03** |
| old B04 Debugging & Logs | folded into **A03** |
| old B05 Stateful Storage | folded into **A05** |
