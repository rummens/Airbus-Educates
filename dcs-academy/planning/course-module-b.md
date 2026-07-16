# Module B — Developer Track (Elective)

For app developers who already got a quick win in Core and now want to **build** for DCS and understand the platform they run on. **Reworked (2026-07-16)**: the app-lifecycle basics (deploy, config, debug, storage) moved *into Core*; this track now pivots to **build & platform integration** — getting your own source onto DCS, the registry, tenancy/policy internals, scaling, and operators.

Builds on Foundations (Module A). Carries the same **`hello-dcs`** sample app plus each learner's own repo where relevant.

> **Restructure note.** Target design. Built dev-track workshops (`workshops-monorepo/tracks/dev-track/lab-b01…b06`) still reflect the old app-lifecycle track. Old → new mapping and the refactor/rename work is tracked in [tasks.md](tasks.md#module-b--developer-restructure).

## Workshop Structure Conventions

Same conventions as [course-module-a.md](course-module-a.md). Names: `lab-b0N-name`. All follow the house standards. **Sample app:** `hello-dcs` (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`); build labs also use the learner's own source / a provided git repo.

---

### Workshop B01: Docker → Kubernetes Migration

**Directory name:** `lab-b01-docker-to-k8s`
**Detailed plan:** [workshop-plans/lab-b01-docker-to-k8s.md](workshop-plans/lab-b01-docker-to-k8s.md)
**Covers ideas:** 7b
**Type:** Elective (Developer) · **Intermediate**
**Prerequisites:** Module A (Core)
**Source:** new.
**Learning objectives:** Translate a Docker / docker-compose mental model to Kubernetes objects; map `docker run`/compose concepts to Deployment/Service/env/volumes; understand what changes on DCS (no local docker, restricted SCC, images from Harbor).
**Narrative arc:** "I know Docker — how does this map?" → a `docker run` / compose file → the equivalent Deployment + Service + ConfigMap → what doesn't translate (privileged, host mounts, `latest`, root) and why DCS rejects it → land the app the "K8s way".
**Code exercises:** Take a compose/`docker run` example → produce the equivalent K8s manifests → deploy → reconcile the differences (non-root, resource limits, Harbor image ref). Examiner checks the migrated app runs.
**Key code examples:** Side-by-side compose ↔ Deployment/Service/ConfigMap. Constructs → upstream; DCS constraints (SCC, Harbor, no `latest`) → `dcs_docs_base_url`.
**Design note:** On-ramp lab — deliberately early so Docker-native developers have a bridge before the build labs.

### Workshop B02: Building Images with BuildConfigs

**Directory name:** `lab-b02-image-buildconfigs`
**Detailed plan:** [workshop-plans/lab-b02-image-buildconfigs.md](workshop-plans/lab-b02-image-buildconfigs.md)
**Covers ideas:** 7c
**Type:** Elective (Developer)
**Prerequisites:** B01
**Source:** new. First of the two "connect my git" labs — **git as a build source**.
**Learning objectives:** Connect a git repo as a **build source**; build an image *on the cluster* with a BuildConfig (S2I and/or Dockerfile strategy); push the result to Harbor; deploy it.
**Narrative arc:** "How do I get *my* code into an image without a local Docker?" → point a BuildConfig at a git repo → build on-cluster (S2I / Dockerfile) → image lands in Harbor → deploy it with the A02 skills → trigger a rebuild on a change.
**Code exercises:** Create a BuildConfig from a git repo; run a build; watch it push to `{{< param dcs_registry >}}`; deploy the built image; trigger a rebuild. Examiner checks the build succeeds and the app runs from the built image.
**Key code examples:** BuildConfig (git source, S2I/Dockerfile strategy, Harbor output), ImageStream. BuildConfig/S2I → upstream; Harbor output + air-gapped builder images → `dcs_docs_base_url`.

### Workshop B03: Cloud Development with OpenShift Dev Spaces

**Directory name:** `lab-b03-dev-spaces`
**Detailed plan:** [workshop-plans/lab-b03-dev-spaces.md](workshop-plans/lab-b03-dev-spaces.md)
**Covers ideas:** 11b
**Type:** Elective (Developer)
**Prerequisites:** B01
**Source:** old B06 (Dev Spaces). Second "connect my git" lab — **git as an in-cluster IDE**.
**Learning objectives:** Explain what OpenShift Dev Spaces is (in-cluster, browser-based, air-gapped IDE — Eclipse Che) and why it fits DCS; launch a workspace from a **devfile** against a git repo; edit + run the app inside the cluster; distinguish it from the Educates editor and from BuildConfigs.
**Narrative arc:** "How do I *develop on* DCS, not just deploy to it?" → Dev Spaces gives a consistent, policy-compliant, air-gapped IDE → open a workspace from the sample repo's devfile → edit + run in the workspace → compare with `oc apply` (A02) and BuildConfigs (B02).
**Code exercises:** Open/inspect a Dev Spaces workspace from a `devfile.yaml`; run the app in the workspace terminal; make a change and see it live.
**Key code examples:** `devfile.yaml` referencing a **Harbor-mirrored** UDI via `{{< param dcs_registry >}}`; Dev Spaces dashboard as a session tab. Dev Spaces → upstream; DCS-specific → `{{< param dcs_docs_base_url >}}/services/dev-spaces`.
**Design note:** Dev Spaces is operator-provided (platform installs it). If unavailable in the test cluster, deliver as an annotated, screenshot-driven concept lab. UDI/dev images all from Harbor.

### Workshop B04: Harbor & Image Scanning

**Directory name:** `lab-b04-harbor-scanning`
**Detailed plan:** [workshop-plans/lab-b04-harbor-scanning.md](workshop-plans/lab-b04-harbor-scanning.md)
**Covers ideas:** 4, 12
**Type:** Elective (Developer)
**Prerequisites:** B02
**Source:** old A04 (Working with Harbor) + **all image-scanning content merged here** (from Security C01/C04 — see overlap note).
**Learning objectives:** Navigate DCS Harbor catalogs (DCS / Allowed External / Proxy-Cached); pull with `skopeo`; push your built image; **read a vulnerability/compliance scan report and understand the scan gate**; know how mirroring/quota happen via ITSM.
**Narrative arc:** "Where do my images live and what guards them?" → Harbor catalogs + robot accounts → `skopeo inspect`/pull → push the B02 image → **view the scan result and the gate** (vulnerability vs compliance, per-image/project) → remediate a finding → mirroring/quota via ITSM.
**Code exercises:** `skopeo inspect`/pull against Harbor (read-only robot); push the built image; view scan status (live scan-API read if a scanner-backed Harbor is reachable, else static fixture); browse the Harbor UI tab.
**Key code examples:** `skopeo` pull/inspect/push; a Deployment referencing a Harbor image; scan-report read. Harbor/scanning → `{{< param dcs_docs_base_url >}}/services/registry`.
**Overlap note:** Per the 2026-07-16 decision, **all image-scanning teaching consolidates here** rather than being split with the Security track. The built Security workshops C01 (image-scanning) and C04 (supply-chain) now overlap — reconcile when the Security track is next revised (tracked in [tasks.md](tasks.md#security-track-scanning-overlap)). Security track keeps the *governance/policy/provenance* angle; the developer-facing "read the scan, pass the gate" flow lives here.
**Config note:** `skopeo` already in `dcs-workshop-base`. Harbor UI embedded as a dashboard tab (feasibility to validate).

### Workshop B05: RBAC, Tenancy & Namespaces

**Directory name:** `lab-b05-rbac-tenancy`
**Detailed plan:** [workshop-plans/lab-b05-rbac-tenancy.md](workshop-plans/lab-b05-rbac-tenancy.md)
**Covers ideas:** 5, 5b
**Type:** Elective (Developer)
**Prerequisites:** Module A (Core A06 gives the vocabulary)
**Source:** old A05 (Access & Tenancy) + old A08 (RBAC Deep Dive), consolidated.
**Learning objectives:** Explain the **Tenant → Namespaces** model in depth (no separate "project" layer); read and reason about RBAC (Role vs ClusterRole, RoleBinding vs ClusterRoleBinding, rules); trace subject → binding → role → rule; create a Role+RoleBinding and prove least privilege; read quotas and understand ITSM increase.
**Narrative arc:** "Who can do what, and why?" → Tenant → Namespaces + onboarding/SSO → `oc auth can-i` (can I?) → *why* (read the objects) → create a Role+RoleBinding → prove effect with `--as` → quotas + ITSM increase.
**Code exercises:** Inspect RBAC (`oc auth can-i`, rolebindings); apply a Role+RoleBinding; `oc auth can-i --as` to prove effect; `oc describe quota`. Examiner checks the binding takes effect.
**Key code examples:** Role + RoleBinding YAML; impersonation checks; ResourceQuota read. RBAC → upstream; DCS tenancy/quotas → `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access`.

### Workshop B06: DEV vs PROD Namespaces & Policies

**Directory name:** `lab-b06-dev-prod-namespaces`
**Detailed plan:** [workshop-plans/lab-b06-dev-prod-namespaces.md](workshop-plans/lab-b06-dev-prod-namespaces.md)
**Covers ideas:** 3
**Type:** Elective (Developer)
**Prerequisites:** B05
**Source:** **new** (the missing lab) + the deep model from old A03 (vcluster).
**Learning objectives:** Distinguish DCS **DEV vs PROD** namespace types by their **policy posture**: PROD enforces harsher policies (Kyverno) **and can create Routes**; DEV has looser policies **but cannot create Routes**; describe the promotion (DEV → PROD, don't edit in place) and why the split exists.
**Narrative arc:** "Why did A04's Route need a PROD namespace?" → see a DEV and a PROD namespace side by side (**vcluster**) → deploy to DEV (loose policy, no Route) → try to create a Route in DEV → **it's blocked** → do it in PROD (Route works, but stricter Kyverno policy applies) → understand promotion and the policy trade-off.
**Code exercises:** Deploy the same workload to DEV and PROD (vcluster); attempt a Route in DEV (observe the block) and succeed in PROD; inspect the Kyverno policy that PROD enforces; observe promotion.
**Key code examples:** Same workload across two namespace types; a Route that fails in DEV / succeeds in PROD; a Kyverno policy read. DCS-specific: `{{< param dcs_docs_base_url >}}/concepts/namespace-types`.
**Config note:** Enable **vcluster** so both namespace types are visible. PROD requires Kyverno present to demonstrate enforcement (screenshot fallback if the test cluster lacks it, as in old A03).

### Workshop B07: Scaling, Health & Resources

**Directory name:** `lab-b07-scaling-health`
**Detailed plan:** [workshop-plans/lab-b07-scaling-health.md](workshop-plans/lab-b07-scaling-health.md)
**Covers ideas:** 9
**Type:** Elective (Developer)
**Prerequisites:** Module A (Core)
**Source:** old B03 (Scaling, Health & Resources).
**Learning objectives:** Set replicas; add liveness/readiness probes; set requests/limits within quota; understand self-healing.
**Narrative arc:** Scale up → hit the quota → right-size requests/limits → add probes for reliability → kill a Pod and watch it self-heal.
**Code exercises:** Scale the app; add probes; set resources within budget; delete a Pod and confirm recovery. Examiner checks readiness + self-heal.
**Key code examples:** Probes + resources block (mind the namespace budget). Constructs → upstream.

### Workshop B08: Operators on DCS

**Directory name:** `lab-b08-operators`
**Detailed plan:** [workshop-plans/lab-b08-operators.md](workshop-plans/lab-b08-operators.md)
**Covers ideas:** 6c
**Type:** Elective (Developer) · **Advanced**
**Prerequisites:** B05
**Source:** old A09 (Operators on DCS).
**Learning objectives:** Explain the Operator pattern (controller + reconcile), CRD vs CR, OLM/OperatorHub; state the **DCS ownership model** (platform owns the operator, tenant owns the instance); create and inspect a CR. Prerequisite for Module F (Operators / Platform Services).
**Narrative arc:** Built-in resources → operators extend them → CRD vs CR → create an instance and watch it reconcile → the platform-owns-operator / tenant-owns-instance split.
**Code exercises:** Inspect CRDs/api-resources; apply a sample CR; watch reconciliation; console Installed Operators view.
**Key code examples:** A minimal Custom Resource (reuse CloudNativePG images). Operator pattern → upstream; DCS-specific → `{{< param dcs_docs_base_url >}}/concepts/operators`.
**Design note:** Still the conceptual prerequisite for **Module F** (GitLab, Argo CD, CloudNativePG). Formerly Core A09; now the capstone of the Developer track.

## Notes

- **Two "connect my git" labs, different purpose:** B02 (BuildConfigs) connects git as a *build source* → image in Harbor; B03 (Dev Spaces) connects git as an *in-cluster IDE*. Sequenced adjacently on purpose.
- **Levels:** B01 Intermediate (Docker bridge), B08 Advanced (operators); the rest standard.
- App-lifecycle basics (deploy, config, debug, storage) are **in Core** now (A02/A03/A05) — this track does not re-teach them.

## Old → New mapping (for the refactor)

| Old workshop | New home |
|---|---|
| old B01 Deploy First App | → Core **A02** |
| old B02 Config & Secrets | → Core **A03** |
| old B03 Scaling, Health & Resources | **B07** |
| old B04 Debugging & Logs | → Core **A03** |
| old B05 Stateful Storage | → Core **A05** |
| old B06 Dev Spaces | **B03** |
| old A04 Working with Harbor | **B04** (+ merged scanning) |
| old A05 Access & Tenancy | **B05** |
| old A08 RBAC Deep Dive | **B05** |
| old A03 Namespace model (vcluster) | **B06** (deep) |
| old A09 Operators | **B08** |
| — | **B01** Docker→K8s (new), **B02** BuildConfigs (new), **B06** DEV/PROD policies (new) |

## Future Expansion Ideas

- Blue/green or canary rollout workshop (once a CI/CD module exists).
- Multi-service app (front + back + db) tying config/scaling/storage together.
- Dev Spaces + GitLab (Module F): clone from the tenant's GitLab straight into a workspace.
- GitOps deploy of the B02-built image via Argo CD (Module F).
