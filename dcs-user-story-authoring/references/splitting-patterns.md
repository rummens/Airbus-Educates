# Splitting an epic or an oversized story into DCS stories

Load this when an epic needs its stories, or a story is too big for one iteration.
Apply the **first pattern that fits** — do not stack patterns. Output an ordered list;
that order becomes `P::`.

## Split when

- The work does not fit one iteration.
- The acceptance criteria contain two unrelated outcomes.
- Two environments, two clusters, two charts, or two components are involved.
- Part of it is unknown (that part becomes a `type::spike`).

## Do not split when

- It is already a one-to-three day change.
- The split halves cannot be verified separately.
- Splitting would only create a hand-off queue with no separately verifiable state.

---

## House patterns — try these first

These fit DCS platform work better than the generic agile patterns, and the corpus is
full of them.

### H1 — Environment / rollout ladder
Deliver into one environment, verify, then advance. Each rung is separately verifiable
and separately valuable (it de-risks the next).

- `Set a permissive policy baseline for DEV namespaces` → `Turn Kyverno into Enforce
  mode in DIV` → `Deploy Status Page to all countries`
- Rungs that take an existing capability to a further environment are
  **`type::deployment`**, not `type::dev`. Add `rollout::<country>` where a rung is
  country-specific.

### H2 — Observe → enforce
Ship the rule in audit/report mode, review the violations, then enforce. Two stories,
because the review changes what gets enforced.

- `Review PSS violations for whitelisted apps` → `Switch policy to enforce`

### H3 — Lifecycle chain
Platform delivery has a fixed chain. Each link is a story when it carries real work:

`mirror artifacts` → `deploy component` → `configure / integrate` → `test / automate`
→ `document / runbook`

- `Mirror all required artifacts to the internal registry` → `Deploy the signing
  solution to Harbor` → `Integrate signing to pipeline` → `Add test cases for the
  signing pipeline` → `Document the offline update workflow`

### H4 — Spike then build
An unknown becomes a `type::spike` story with a timebox and a written outcome, then
one or more `type::dev` stories that implement the chosen option.

- `PoC to sign helm chart` (`type::spike`) → `Create custom Chart to enable Cosign
  within Harbor projects` (`type::dev`)
- The spike's acceptance criteria are "a decision is recorded", not "it works".

### H5 — Per component / per chart / per policy
One story per component, chart, operator, or policy — when each has its own values
file, its own upgrade path, or its own owner.

- `Deploy and automate ClickHouse operator` / `... APISIX` / `... Temporal`
- `Kyverno Policy for Pod Disruption Budgets` / `Kyverno Policy for Using Secure Images`

### H6 — Automation and documentation as their own stories
`type::test` and `type::docs` work is a story, not a checkbox on the dev story, when it
is more than an hour and can be picked up by someone else.

---

## Generic patterns — when no house pattern fits

| # | Pattern | Ask | Example |
|---|---|---|---|
| G1 | Workflow steps | Sequential steps in one journey? | onboard tenant → create namespaces → apply baseline policies |
| G2 | Business-rule variations | Different rules per case? | DEV namespaces permissive vs PROD namespaces enforced |
| G3 | Data variations | Different inputs or resource kinds? | policies for Deployments vs StatefulSets vs Jobs |
| G4 | Acceptance-criteria complexity | Two unrelated outcomes in the criteria? | split along the criteria boundary — the most common signal |
| G5 | Major effort | Deliverable incrementally? | read-only dashboard → alerting → auto-remediation |
| G6 | External dependency | Several external systems? | LDAP integration, then Splunk forwarding, then Keycloak |

---

## Validate every split

1. Does each story leave the platform in a **verifiable state**?
2. Can it be tested on its own?
3. Is it startable when its turn in the order arrives?
4. Do the parts, together, equal the original scope — nothing dropped?
5. Is each one small enough for a single iteration?

Any "no" → re-split.

## Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Task decomposition | "Write the values file", "Open the MR" | Those are steps of one story, not stories |
| Fake parallelism | Every story blocks on story 1 being fully merged | Reorder, or merge them into one story |
| Duplicate outcome | Two stories with an identical payoff | You split the action, not the work — reconsider |
| Silent scope loss | Parts do not sum to the epic's Functional Requirements | Add the missing story |
| Over-splitting | Five stories of two hours each | Merge; per-component splitting needs per-component work |

**Note on horizontal slicing:** the generic agile advice "never split by layer or by
DevOps step" does **not** apply to DCS. Platform work legitimately splits by
environment (H1), by lifecycle step (H3), and by component (H5) — each of those slices
is independently deployable and independently verifiable on a cluster. What stays
forbidden is splitting into steps that produce **no verifiable cluster state on their
own** (see the Task-decomposition pitfall).
