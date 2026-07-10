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

- [ ] **P1** Write per-workshop plans (Step 4) for A01–A06 in `workshop-plans/`.

## Module B — Developer

- [ ] **P2** Write per-workshop plans for B01–B05 after Foundations plans are done (read A0x plans first for continuity).

## Modules C / D / E

- [ ] **P3** Plan after A + B are implemented and the format is proven.
