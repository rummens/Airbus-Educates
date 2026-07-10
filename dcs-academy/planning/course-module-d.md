# Module D — Architect / Onboarding Track (Elective)

For architects and new joiners who need orientation and design guidance rather than deep hands-on. Beginner → intermediate. Conceptual with "observe and diagnose" exercises. Builds on Foundations. Names: `lab-d0N-name`.

*Breakdown-level plan — expand to full per-workshop plans when scheduled (see `tasks.md`).*

---

### Workshop D01: DCS Service Catalog & When to Use What

**Directory name:** `lab-d01-service-catalog`
**Covers ideas:** 17
**Type:** Elective (Architect)
**Prerequisites:** Module A (Foundations)
**Learning objectives:** Describe what DCS offers and choose the right capability for a scenario.
**Narrative arc:** Tour the catalog → map common needs to DCS capabilities → decision guidance.
**Code exercises:** Observe deployed examples of each capability; a decision exercise.
**DCS-specific:** Link catalog concepts to `dcs_docs_base_url`.

### Workshop D02: Tenancy & Landing-Zone Design

**Directory name:** `lab-d02-tenancy-design`
**Covers ideas:** 18
**Type:** Elective (Architect)
**Prerequisites:** Module A (esp. A03, A05)
**Learning objectives:** Structure projects/quotas/environments for a team; apply the prod/dev model at design level.
**Narrative arc:** A team's needs → propose a project/namespace layout → validate against DCS constraints.
**Code exercises:** Inspect a reference tenancy layout (vcluster); critique/adjust it.

### Workshop D03: Reference Architectures / Golden Paths

**Directory name:** `lab-d03-reference-architectures`
**Covers ideas:** 19
**Type:** Elective (Architect)
**Prerequisites:** D01
**Learning objectives:** Recognise recommended patterns for tenant apps on DCS; apply a golden path.
**Narrative arc:** Common app shapes → the DCS golden path for each → walk a reference deployment.
**Code exercises:** Observe a reference architecture deployed; identify how it uses DCS features.

## Future Expansion Ideas

- Cost/capacity planning for tenants.
- Migration playbook (bringing an existing app onto DCS).
