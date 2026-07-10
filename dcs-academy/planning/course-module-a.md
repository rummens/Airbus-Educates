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
**Learning objectives:** Explain what DCS is and where it fits; describe containers and images at a high level; navigate the workshop environment.
**Narrative arc:** Orientation → what DCS is (on-prem, air-gapped, OpenShift-based) → containers/images primer → tour of the session (terminal, editor, `oc`).
**Code exercises:** Run first `oc` commands (`oc whoami`, `oc get project`); observe the pre-provisioned project.
**Key code examples:** Basic `oc` inspection commands. Mostly conceptual + observe.

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
**Learning objectives:** Pull and push images to the DCS Harbor registry; understand projects and scan gates.
**Narrative arc:** Why a single registry (air-gapped) → pull an image → push an image to your project → see the scan result.
**Code exercises:** `podman`/`oc` pull + push against Harbor (`{{< param dcs_registry >}}`); view scan status.
**Key code examples:** Push/pull commands; a Deployment referencing a Harbor image. DCS-specific: `/concepts/registry`.
**Config note:** Uses `dcs-tools` (build tooling); may need image registry app enabled.

### Workshop A05: Access & Tenancy

**Directory name:** `lab-a05-access-tenancy`
**Detailed plan:** [workshop-plans/lab-a05-access-tenancy.md](workshop-plans/lab-a05-access-tenancy.md)
**Covers ideas:** 5
**Type:** Core
**Prerequisites:** A01
**Learning objectives:** Describe how teams onboard to DCS; read RBAC roles; understand quotas and SSO login.
**Narrative arc:** Tenant model → who can do what (RBAC) → quotas in your project → self-service request flow.
**Code exercises:** Inspect your RBAC (`oc auth can-i`, `oc get rolebinding`); view quota (`oc describe quota`).
**Key code examples:** RBAC + ResourceQuota inspection. DCS-specific: `/concepts/tenancy-and-access`; RBAC construct → upstream.

### Workshop A06: Networking & Exposing Apps

**Directory name:** `lab-a06-networking`
**Detailed plan:** [workshop-plans/lab-a06-networking.md](workshop-plans/lab-a06-networking.md)
**Covers ideas:** 6
**Type:** Core
**Prerequisites:** A02
**Learning objectives:** Expose an app via a Route with DCS DNS naming; understand egress restrictions.
**Narrative arc:** Deploy an app → expose it (session proxy for browser, Route where appropriate) → reach it → understand egress limits (air-gapped).
**Code exercises:** Create a Route (`host: app-{{< param session_hostname >}}`); reach the app; attempt/observe a blocked egress call.
**Key code examples:** Route YAML; session ingress/dashboard. DCS-specific: `/concepts/networking`; Route construct → upstream.

## Notes

Foundations is the prerequisite for all tracks. Keep A01–A02 light for learners with prior Kubernetes exposure; A03–A06 are the DCS-specific spine and must be thorough.
