# Tasks

Task tracking for the DCS Academy. Priorities: **P1** (blocker), **P2** (important), **P3** (nice-to-have).

## Course-wide

- [ ] **P1** Confirm real values for the param trio: `dcs_registry` (Harbor project), `dcs_docs_base_url` (docs portal), and confirm `product_name`. Currently placeholders in `course-brief.md` / `resources.md`.
- [ ] **P1** Confirm the two base images (`dcs-workshop-base`, `dcs-tools`) exist / are built and mirrored in Harbor, with `oc` and required tooling.
- [ ] **P2** Confirm the DCS docs portal has (or will have) pages for the four DCS concepts (`namespace-types`, `registry`, `tenancy-and-access`, `networking`).
- [ ] **P2** Choose the per-track sample applications (Developer, Security, Architect) — all images Harbor-mirrored.
- [ ] **P2** Validate vcluster is available/sized on DCS for the sessions that need the prod/dev model (A03).
- [ ] **P3** Run `scripts/collect-images.sh` once the first workshops exist and hand the manifest to the Harbor mirroring workflow.

## Module A — Foundations

- [x] **P1** Write per-workshop plans (Step 4) for A01–A06 in `workshop-plans/`. *(Done — 6 plans linked from course-module-a.md.)*
- [x] **P1** A04 auth resolved from customer docs: Harbor **robot accounts**. *(Remaining P2: per-session robot provisioning + target project.)*
- [ ] **P2** A03: confirm the technical mechanism DCS uses to mark DEV vs PROD namespaces (labels / CRD / request objects). Lifecycle + quick-comparison confirmed from customer docs; mechanism not in shared docs.
- [ ] **P2** Consider a dedicated **Network Policies** workshop if A06 runs past 60m (network policies added from customer docs).
- [ ] **P3** Fold newly-surfaced DCS topics into later tracks: costing/recharging + why-OpenShift (Architect D), data classification/RACI/security-exception (Security C), Helm charts (Developer).
- [ ] **P2** Produce the `hello-dcs` sample image (OpenShift-friendly, non-root) and a Harbor-mirrored base for A04's Containerfile.
- [ ] **P2** Produce the DCS architecture diagram asset for A01.
- [ ] **P3** Implement A01 first (with the authoring skill) to prove the format end-to-end, then A02–A06.

## Module B — Developer

- [ ] **P2** Write per-workshop plans for B01–B05 after Foundations plans are done (read A0x plans first for continuity).

## Modules C / D / E

- [ ] **P3** Plan after A + B are implemented and the format is proven.
