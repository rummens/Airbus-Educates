# Module A — Foundations (Core)

The shared core every learner completes before any track. It brings learners with no container background to a working baseline, then establishes the four DCS-specific concepts (namespace types, Harbor, tenancy, networking) the whole academy relies on. Sequential — each workshop builds on the last.

## Workshop Structure Conventions

Each entry lists: **Covers ideas** (topic numbers from `course-topics.md`), **Type**, **Prerequisites**, **Learning objectives**, **Narrative arc**, **Code exercises**, **Key code examples**. Workshop names: `lab-a0N-name`. All follow the house standards (intro page, `oc`, hybrid doc links, param trio, air-gapped images, examiner + knowledge check).

---

### Workshop A01: What is DCS?

**Directory name:** `lab-a01-what-is-dcs`
**Detailed plan:** [workshop-plans/lab-a01-what-is-dcs.md](workshop-plans/lab-a01-what-is-dcs.md)
**Covers ideas:** 1
**Type:** Core
**Prerequisites:** None
**Learning objectives:** Explain what DCS is and where it fits; describe containers and images at a high level; navigate the workshop environment and the OpenShift web console.
**Narrative arc:** Orientation → what DCS is (on-prem, air-gapped, OpenShift-based) → containers/images primer → tour of the session (terminal, editor, `oc`) → **guided tour of the OpenShift web console** (the academy's single console tour).
**Code exercises:** Run first `oc` commands (`oc whoami`, `oc get project`); observe the pre-provisioned project; tour the console (perspectives, workloads, networking, storage) with `oc` parity.
**Key code examples:** Basic `oc` inspection commands. Mostly conceptual + observe. *(Duration now 30m to fit the console tour.)*

### Workshop A02: Kubernetes Essentials on DCS

**Directory name:** `lab-a02-kubernetes-essentials`
**Detailed plan:** [workshop-plans/lab-a02-kubernetes-essentials.md](workshop-plans/lab-a02-kubernetes-essentials.md)
**Covers ideas:** 2
**Type:** Core
**Prerequisites:** A01
**Learning objectives:** Create and inspect a Deployment, Service; read config/secrets; use `oc` to observe resources.
**Narrative arc:** Deploy a simple workload → expose it with a Service → inspect Pods/Deployments → introduce config via ConfigMap/Secret.
**Code exercises:** Apply a Deployment + Service (image from Harbor); scale it; inspect with `oc get`/`oc describe`.
**Key code examples:** Deployment + Service YAML using `{{< param dcs_registry >}}` image. Upstream links for each construct.

### Workshop A03: Namespaces & the Prod/Dev Model

**Directory name:** `lab-a03-namespace-model`
**Detailed plan:** [workshop-plans/lab-a03-namespace-model.md](workshop-plans/lab-a03-namespace-model.md)
**Covers ideas:** 3
**Type:** Core
**Prerequisites:** A02
**Learning objectives:** Distinguish DCS dev vs prod namespace types; describe promotion; deploy into each type.
**Narrative arc:** Concept of namespace types → see a dev and a prod namespace side by side (**vcluster**) → deploy to dev → understand what promotion to prod means.
**Code exercises:** Deploy to a dev namespace, inspect the differences in a prod-type namespace (vcluster).
**Key code examples:** Same workload across two namespace types. DCS-specific concept linked to `{{< param dcs_docs_base_url >}}/concepts/namespace-types` with inline blurb.
**Config note:** Enable vcluster for this workshop.

### Workshop A04: Working with Harbor

**Directory name:** `lab-a04-harbor-registry`
**Detailed plan:** [workshop-plans/lab-a04-harbor-registry.md](workshop-plans/lab-a04-harbor-registry.md)
**Covers ideas:** 4
**Type:** Core
**Prerequisites:** A02
**Learning objectives:** Pull images from DCS Harbor catalogs; browse the Harbor UI; understand projects and scan gates. (Pull-only — pushing is conceptual.)
**Narrative arc:** Why a single registry (air-gapped) → inspect/pull an image with `skopeo` → browse it in the Harbor UI → see the scan result → (concept) how pushing/mirroring works via a dedicated project + ITSM.
**Code exercises:** `skopeo inspect`/pull against Harbor (`{{< param dcs_registry >}}`, read-only robot account); view scan status; browse the Harbor UI tab.
**Key code examples:** `skopeo` pull/inspect; a Deployment referencing a Harbor image. DCS-specific: `/concepts/registry`.
**Config note:** Runs on `dcs-workshop-base` with **`skopeo`** added (no docker/podman — no double-virtualization). Harbor UI embedded as a dashboard tab (feasibility to validate).

### Workshop A05: Access & Tenancy

**Directory name:** `lab-a05-access-tenancy`
**Detailed plan:** [workshop-plans/lab-a05-access-tenancy.md](workshop-plans/lab-a05-access-tenancy.md)
**Covers ideas:** 5
**Type:** Core
**Prerequisites:** A01
**Learning objectives:** Describe how teams onboard to DCS; understand the **Tenant → Namespaces** model (no separate "project" layer — a project *is* a namespace in OpenShift wording); read RBAC basics; understand quotas and SSO login.
**Narrative arc:** Tenant model (Tenant → Namespaces) → who can do what (RBAC basics + isolation proof) → quotas in your namespace → self-service (ITSM) request flow.
**Code exercises:** Inspect your RBAC (`oc auth can-i`, `oc get rolebinding`); view quota (`oc describe quota`).
**Key code examples:** RBAC + ResourceQuota inspection. DCS-specific: `/concepts/tenancy-and-access`; RBAC construct → upstream. *(Deeper RBAC — Roles/ClusterRoles/bindings — is its own lab, A08.)*

### Workshop A06: Networking & Exposing Apps

**Directory name:** `lab-a06-networking`
**Detailed plan:** [workshop-plans/lab-a06-networking.md](workshop-plans/lab-a06-networking.md)
**Covers ideas:** 6
**Type:** Core
**Prerequisites:** A02
**Learning objectives:** Expose an app via a Route (requires a **PROD-type namespace**) with DCS DNS naming; understand Network Policies (observe-only) and egress restrictions.
**Narrative arc:** Deploy an app → expose it (session proxy for browser, Route in a provisioned PROD-type namespace) → reach it → observe a NetworkPolicy + a blocked egress call (air-gapped).
**Code exercises:** Create a Route into a PROD-type namespace (`host: app-{{< param session_hostname >}}`); reach the app; inspect a pre-provisioned NetworkPolicy; attempt/observe a blocked egress call.
**Key code examples:** Route YAML; session ingress/dashboard. DCS-specific: `/concepts/networking`; Route construct → upstream. *(NetworkPolicy is observe-only — tenant self-create is on the roadmap.)*

### Workshop A07: Storage on DCS

**Directory name:** `lab-a07-storage`
**Detailed plan:** [workshop-plans/lab-a07-storage.md](workshop-plans/lab-a07-storage.md)
**Covers ideas:** 6b (storage — see course-topics.md)
**Type:** Core
**Prerequisites:** A02
**Learning objectives:** Request storage via a PVC; distinguish DCS **File vs Block** storage classes; prove data persists across a restart; know that classification drives SC choice and S3 comes via ITSM.
**Narrative arc:** Stateless app loses data → request a PVC (SC name via variable) → mount it → survive a restart → understand classification-driven SC choice + S3-via-ticket.
**Code exercises:** Apply PVC (`{{< param dcs_sc_file >}}`), mount, write, restart, confirm persistence; challenge with a Block PVC.
**Key code examples:** PVC + volume mount using variable SC names. DCS-specific: `/concepts/storage`; PV/SC constructs → upstream.
**Config note:** New params `dcs_sc_file`, `dcs_sc_block`. Foundations concept lab; Developer B05 is the hands-on deep dive.

### Workshop A08: RBAC Deep Dive

**Directory name:** `lab-a08-rbac-deep-dive`
**Detailed plan:** [workshop-plans/lab-a08-rbac-deep-dive.md](workshop-plans/lab-a08-rbac-deep-dive.md)
**Covers ideas:** 5b (RBAC depth — see course-topics.md)
**Type:** Core (recommended; split out of A05 per author review)
**Prerequisites:** A05
**Learning objectives:** Distinguish Role/ClusterRole and RoleBinding/ClusterRoleBinding; read rules; trace subject → binding → role → rule; create a Role+RoleBinding in your namespace and prove it.
**Narrative arc:** "can I?" (A05) → why, and how it's wired → read the objects → create one → prove least privilege.
**Code exercises:** Inspect ClusterRoles/RoleBindings; apply a Role+RoleBinding; `oc auth can-i --as` to prove effect.
**Key code examples:** Role + RoleBinding YAML; impersonation checks. RBAC construct → upstream; DCS-specific: `/concepts/rbac`.

### Workshop A09: Operators on DCS

**Directory name:** `lab-a09-operators`
**Detailed plan:** [workshop-plans/lab-a09-operators.md](workshop-plans/lab-a09-operators.md)
**Covers ideas:** 6c (operator concept — see course-topics.md)
**Type:** Core (prerequisite for Module F — Operators track)
**Prerequisites:** A02
**Learning objectives:** Explain the Operator pattern (controller + reconcile), CRD vs CR, OLM/OperatorHub; state the **DCS ownership model** (platform owns the operator, tenant owns the instance); create and inspect a CR.
**Narrative arc:** Built-in resources → operators extend them → CRD vs CR → create an instance and watch it reconcile → the platform-owns-operator / tenant-owns-instance split.
**Code exercises:** Inspect CRDs/api-resources; apply a sample CR; watch reconciliation; console Installed Operators view.
**Key code examples:** A minimal Custom Resource (reuse CloudNativePG images). Operator pattern → upstream; DCS-specific: `/concepts/operators`.

## Notes

Foundations is the prerequisite for all tracks. Keep A01–A02 light for learners with prior Kubernetes exposure; A03–A07 are the DCS-specific spine and must be thorough. A08 (RBAC depth) and A09 (Operators) are recommended-core: A08 deepens A05, A09 is the conceptual prerequisite for the Operators track (Module F). Sequence the spine A03→A07; A08/A09 can slot after their prerequisites.
