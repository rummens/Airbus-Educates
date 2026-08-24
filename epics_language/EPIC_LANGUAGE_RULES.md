# DCS Epic Language & Structure Rules

> Derived by reading real epics in the DCS group (e.g. `&256` Mistral Platform
> Enablement, `&3` Registry Improvements / Supply Chain Security, `&41` Cross
> Country Metric Aggregation, `&160` Kyverno Enhancements, `&197` DCS Uptime
> Tracking, `&199` Splunk Integration PoC, `&206`/`&269` Runtime Security,
> `&244` OpenShift Virtualization, `&252` Project Capsule, `&258` DCS Upgrades).
> Use these rules when writing a new **Epic**.

---

## 1. Purpose & scope of an epic

- An epic is a **release-sized capability**, not a single task.
- It describes the **"what" and the "why"** of a capability at platform/infrastructure
  scope, and may list core objectives — it does not enumerate per-task acceptance
  checkboxes (that belongs in user stories).
- Epics sit under a **Release tracking epic** (e.g. `&220` "Development Stream R5"):
  `&220` → sub-epic (e.g. `&256`) → user-story issues.

## 2. Required headline blocks (use "## " markdown headings)

A well-formed epic typically contains (in this order):

1. **Description** — 1 paragraph goal statement.
2. **Importance of the Epic** (or **Business Value & Objectives**) — why it matters,
   who it serves, risk/value.
3. **Functional Requirements** — bullet list of what must be built/delivered.
4. **Non-Functional Requirements** — Security, Scalability, Maintainability,
   Compliance bullets (optional but common).
5. **Success Criteria** — measurable outcomes (`* Result ...`).
6. **Roadmap Summary** — **MANDATORY**. A closing `## Roadmap Summary` section
   that ties the epic back to its broader goal and the release stream.

Some epics instead use **Plan & Overview** + **Detailed Description** (see
`&206`, `&269`), or add an explicit **Strict Architectural Principle** call-out
for a hard constraint (see `&41`). Pick one consistent style per epic.

## 3. Language and tone

- **Formal, engineering tone.** Write in complete sentences; avoid chatty/casual
  phrasing.
- **Title case titles**, e.g. "Platform Enablement for Mistral On-Premise AI
  Multi-Tenant Stack", "Cross Country Metric Aggregation".
- Spell out the platform's full name on first mention, then the acronym, e.g.
  "Digital Container Service (DCS)".
- Reference the **actual tech stack** explicitly: ArgoCD, Helm charts, OpenShift,
  Operators, CRDs, vcluster, NeuVector, Kyverno, Keycloak, Splunk, Harbor.
- Use **bold** for key terms, e.g. `**ArgoCD**`, `**Sandbox cluster**`,
  `**dedicated virtual cluster (vcluster)**`.
- Emphasize **declarative GitOps** ("managed declaratively via ArgoCD and Helm
  charts") as a platform principle.
- State target audiences/teams, e.g. "This release targets Tenant Application
  Owners & Security Operations Teams".
- Note **security/compliance** drivers (BSI, SLA, audit) where relevant.

## 4. Formatting

- Use `## ` for major sections; `### `/bullets for sub-points.
- Use `*` or `-` bullet lists for requirements and success criteria.
- Success criteria phrased as outcomes: `* <Capability> can be successfully
  <done> without manual interventions.`
- Reference design docs/blueprints via inline links (Wikis, Google Docs) and
  include images where helpful.

## 5. Do's

- Keep the description concise (a paragraph) — detail goes in requirements.
- Make Success Criteria objectively verifiable.
- Tie work back to a concrete platform/customer outcome.
- Add relevant labels (e.g. `P::` priority, `complexity::`, `subproduct::`).

## 6. Don'ts

- Don't dump per-task acceptance criteria into the epic — leave that to the
  user-story children.
- Don't use vague verbs; prefer concrete deliverables ("deploy", "harden",
  "validate", "mirror", "blueprint").
- Don't leave the description empty or a single terse line unless it is a pure
  tracking epic.