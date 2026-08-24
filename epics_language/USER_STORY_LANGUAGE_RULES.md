# DCS User Story Language & Structure Rules

> Derived by reading 175 real user-story work items spread across many epics in
> the DCS group (e.g. `&256` Mistral, `&206` Runtime Security, `&41` Cross
> Country Metric Aggregation, `&267` Pipelines, `&3` Supply Chain, `&160`
> Kyverno, `&244` Virtualization). Use these rules when writing a new **user
> story** (i.e. an issue work item under an epic).

---

## 1. Two accepted templates

Stories in DCS follow either a **full developer template** or a **compact
user-story template**. Match the style already used in your epic.

### Template A — Full developer template (common; the "standard")

```
# Description

<what this story does, plain English; optionally include an As a / I want / So that line>

## Requirements

### Functional Requirements (Optional but Recommended)
- bullet of functional behavior

### Non-Functional Requirements (Optional)
- bullet

## How to Test (Optional)
- a concrete manual/automated verification step

## How to Demo (Optional)
- what to show at the demo

## External References (Optional)
- links

## Definition of Ready
- [ ] Does it have business value and acceptance criteria?
- [ ] Does it have a clear scope and requirements?
- [ ] Is it technically feasible, testable and compliant?
- [ ] Does it have minimal dependencies?
- [ ] Is it small enough?
- [ ] Does it have a Priority, Epic, Milestone and Iteration assigned?

## Definition of Done
- [ ] Has acceptance criteria been met?
- [ ] Has it been validated and verified?
- [ ] Has it passed review and has it been merged/released?
- [ ] Has it been documented?
- [ ] Has the development space been cleaned after the work has finished?
```

### Template B — Compact user story (As a / I want / So that)

```
**As a** <role>,
**I want to** <capability>,
**So that** <payoff>.

**Acceptance Criteria:**
* [ ] verifiable checkbox outcome
* [ ] verifiable checkbox outcome
```

---

## 2. Core content rules (both templates)

- **Acceptance Criteria are mandatory and must be a checkbox list** that is
  objectively verifiable. Use `* [ ]` (or `- [ ]`) bullets; never a prose-only
  list.
- Keep each story small and testable. Prefer several focused stories over one
  large one.
- Tie the story to a real **role / persona**: Platform Engineer, DCS Operator,
  Application Team Engineer, Capacity Planner, Platform Administrator, Tenant
  Application Owner.
- State the **"why"** (the payoff) explicitly via Acceptance Criteria outcome
  wording even if no formal "So that" line is used.

## 3. Language and tone

- English, concise, engineering tone. Imperative or outcome-oriented verbs:
  "deploy", "configure", "install", "validate", "verify", "author", "mirror".
- Prefer plain technical terminology; keep acronyms as used in the platform
  (ArgoCD, Helm, CRD, vcluster, NeuVector, Kyverno, Harbor, GPU).
- Use `**bold**` for key terms (e.g. `**Key Requirements:**`).
- Where relevant, put the user-story sentence on its own line:
  `**As a** ... / **I want to** ... / **So that** ...`
  (occasionally wrapped in blockquote `>` lines).

## 4. Formatting

- Top heading is `# Description` (`## Description` and `### Description` also
  occur — match neighboring work items).
- Use `## ` for sections, `### ` for sub-sections (e.g. Functional vs
  Non-Functional Requirements).
- Acceptance Criteria as `* [ ]` or `- [ ]` checkboxes.
- "How to Test" / "How to Demo" are optional but encouraged for dev tasks.

## 5. Labels

- Every story gets a `type::` label: `type::dev` (default), `type::docs`,
  `type::deployment`, `type::spike`, `type::ops`.
- Priority via `P::<n>` (`P::1`..`P::3`).
- Optionally add `complexity::<low|medium|high>`, `component::<name>`,
  `external-support`, `rollout::<country>`, `lifecycle`, `release-orphan`.

## 6. Do's

- Always finish with checkable Acceptance Criteria.
- Reference the epic and milestone (Done criteria expect a Milestone assigned).
- Use the "Definition of Ready" list verbatim for user stories written with
  the full template (it is a standardized boilerplate in DCS).

## 7. Don'ts

- Don't leave the description empty (label `no-description` is discouraged).
- Don't create stories without acceptance criteria and a milestone.
- Don't copy the epic-level objectives verbatim; break them into small,
  individually verifiable units.