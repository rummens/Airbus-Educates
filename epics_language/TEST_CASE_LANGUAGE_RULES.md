# DCS Test Case Language & Structure Rules

> Derived by reading 226 real `test_case` work items (GitLab issue type
> `issue_type=test_case`, not the label `type::test`) in the DCS group
> (primarily `dcs/dcs-helm-charts`, e.g. NP-, SS-, GRAF-, KC-, KCST-, PGW-,
> AG-, EIP-, SM-, GLR-, Trident-TST- series).
>
> In GitLab a test case is **an issue created with the `test_case` work item
> type** — the URL path segment is `/quality/test_cases/<iid>` (never
> `/-/issues/<iid>`). It is **not** defined by the `type::test` label, although
> the `type::test` label is almost always applied alongside it. These are the
> source material our test engineers turn into automated tests using
> **Robot Framework** and **Kyverno Chainsaw**.
>
> Use these rules when writing a **new test case** in this format.

---

## 1. What a test case is (scope)

- A test case is an **issue of the `test_case` GitLab work-item type**, found
  under `/quality/test_cases/`.
- It documents **one, objectively verifiable test**: a named behavior, the
  prerequisites to run it, explicit manual steps, and an exact expected
  outcome — plus a **proposal for how to automate it** so a test engineer can
  implement it in Robot Framework or Chainsaw (or Helm tests / Python/KubeLibrary
  where appropriate).
- Every test case must be **clear, testable, and its result verifiable**. If a
  result cannot be asserted programmatically, it is not a valid test case.

## 2. Required labels (mandatory for new test cases)

A well-formed test case sets these labels. Aim to include **all** of the core
set below; they drive the QA board, environment tracking, and automation backlog.

### Core (apply to every test case)

| Label | Value | Meaning / guidance |
|---|---|---|
| `type::test` | fixed | Marks the item as a test (required on essentially all test cases). |
| `component::<name>` | 1+ | Component under test, e.g. `component::namespace provisioner`, `component::keycloak`, `component::harbor`, `component::argocd`, `component::sealed secrets`, `component::monitoring`, `component::logging`, `component::GPU`, `component::EgressIP`, `component::Service Mesh`, `component::GitLab Runner`, `component::Kasten`, `component::operators`, `component::crossplane`, `component::push-gateway`. Use the exact existing value — do not invent a near-name. |

### Automation type — pick the tool (`test::<tool>`)

| Label | Meaning |
|---|---|
| `test::chainsaw` | Kyverno Chainsaw test (declarative apply/assert/error/command steps). |
| `test::robot` | Robot Framework test (KubeLibrary etc.). |
| `test::python` | Python test script (KubeLibrary / pytest). |
| `test::helm-test` | Helm test hook / chart smoke test. |
| `test::scenario` | Behavioural user scenario (steps / preconditions, see §5). |
| `test::grafana` | Grafana metric / provisioning verification. |
| `test::performance` | Performance / load validation. |

### Automation status — pick one (`test-automation::<state>`)

| Label | Meaning |
|---|---|
| `test-automation::planned` | Automation is planned but not yet written (most common on new cases). |
| `test-automation::implemented` | Automation exists and is runnable. |
| `test-automation::not-planned` | Automation intentionally on hold / not planned. |

### Verification status per environment — `test-<env>::<state>`

These track the test's outcome against the three national environments. Include
them when the test is intended to run on the clusters:

| Label | Meaning |
|---|---|
| `test-de::pass` / `test-div::pass` / `test-es::pass` | Passed on Germany / Divisional / Spain. |
| `test-de::fail` / `test-div::fail` / `test-es::fail` | Failed on that environment. |
| `test-de::planned` / `test-div::planned` / `test-es::planned` | Planned to run on that environment. |
| `test-de::n/a` / `test-div::n/a` / `test-es::n/a` | Not applicable to that environment. |

### Optional but useful

- `status::<state>` — workflow state; `status::open` is the default on new
  items. Other values: `backlog`, `refinement`, `in-progress`, `review`,
  `blocked`, `support`, `rollout`.

> **Do not** apply a `P::<n>` (priority) or `release::<n>` label to a test case.
> Prioritisation belongs on the parent story/epic that the test case documents,
> and release tracking is inherited from its parent work items.

---

## 3. Title ID prefix (naming convention)

- Prefix the title with a short **component ID + `-TST-<nn>`** sequence, then a
  verb-led, imperative title. Examples:
  - `NP-TST-026 - Harbor Project CVE Allowlist exception Configuration`
  - `SS-TST-007 - Apply a \`SealedSecret\` to a specific namespace`
  - `GLR-TST-03 Pod Security Context Restrictions`
  - `Kasten-TST-009 - Kasten Disaster Recovery (DR) Status Verification`
  - `PGW-TST-001 - Validate Pushgateway Baseline Deployment Health`
- Keep the sequence unique per component. The `Test Case ID` inside the body
  must match this prefix (e.g. `NP-TST-026`).

---

## 4. Body format

Two accepted layouts are widely used. Match the style already used in the
target component/epic. Either way the **same fields must be present**.

### Template A — Markdown table (most common; recommended)

```
### Test Case <n>: <Short Name>

| | |
|---|---|
| **Test Case ID** | `<ID>-TST-<nn>` |
| **Test Case Name** | `<Verifiable behavior being tested>` |
| **Component(s)** | `<component>, <component>` |
| **Priority** | `<High\|Medium\|Low\|Critical>` |
| **Prerequisites** | 1. `oc`/`kubectl` access to the OpenShift cluster.<br>2. <prereq><br>3. <prereq> |
| **Manual Test Steps** | 1. <numbered step with concrete command>. <br>2. <step>. |
| **Expected Outcome** | 1. <objectively assertable outcome>.<br>2. <outcome>. |
| **Automation Proposal** | <which tool: Chainsaw / Robot / Helm / Python> and concretely what it asserts. |
| **Reference** | <opt. link to chart template / design / docs> |
```

### Template B — HTML `<table>` (also common for the SS-/GRAF- series)

Identical fields, but each cell is wrapped in HTML `<tr><td>` rows. Prefer the
markdown table for new cases unless the surrounding work items use this layout.

### Field-by-field rules

- **Test Case ID**: `<PREFIX>-TST-<nn>` — must equal the title prefix.
- **Test Case Name**: phrased as a verifiable claim, e.g. "Verify Route
  Exception Validation (3-Month Limit)".
- **Component(s)**: backtick-quoted, comma separated; reference the real Helm
  chart / resource names (e.g. `dcs-namespace-provisioner`, `ovn-kubernetes`,
  `grafana-sc-datasources`, `sealed-secrets-controller`).
- **Priority**: `Critical`, `High`, `Medium`, `Low`.
- **Prerequisites**: numbered list using `1.` ... `<br>` separated (not markdown
  bullet lists inside the table cell).
- **Manual Test Steps**: **numbered, concrete, copy-pasteable** `oc`/`kubectl`
  commands with real resource names. Give exact `jsonpath` / `-o` flags when
  the assertion depends on parsing output.
- **Expected Outcome**: **numbered and objectively assertable**. State exact
  values (exit code `0`, `"allowPrivilegeEscalation":false`, `200 OK`, specific
  column values). No fuzzy language like "should work".
- **Automation Proposal**: name the tool(s) and enumerate the **assert** steps
  (e.g. for Chainsaw: apply / assert / error / command steps; for Robot:
  which keywords/endpoints + expected status codes).

---

## 5. Scenario-style test cases (`test::scenario`)

For behavioural/user-level cases use an `Objective / Preconditions / Steps`
layout (see the DCS-TST series):

```
# Objective:
* <what the user/capability must do>

# Preconditions:
* <account / onboarded state / cluster>

# Steps:
* <user action>
* <what the system shows / user can do>
* What is blocked :
  * <negative behaviour that must be forbidden>

# Fail reasons:
* <why the test would fail>
```

Cover both positive ("user can …") and explicit negative ("what is blocked …")
behaviour so negative assertions are unambiguous.

---

## 6. Language and tone

- **English, formal engineering tone.** Imperative, outcome-oriented verbs:
  "verify", "validate", "assert", "confirm", "measure", "enforce".
- **Be specific and quantitative.** Every expected outcome must be machine/lab
  verifiable: exact exit codes, exact status strings, exact resource names,
  exact columns/fields to inspect.
- Distinguish **success** ("the resource is created / the status is `Bound` /
  the command exits `0`") from **failure** ("the `Secret` must NOT be created in
  the other namespace", "the API must return `401 Unauthorized`").
- Use `**bold**` for key terms and backticks for resource names, commands,
  namespaces, and file paths. Keep acronyms as used on the platform (ArgoCD,
  Helm, CRD, NetworkPolicy, PVC, CVE, SCC).
- Keep each test case focused on **one verifiable behavior**.

## 7. Do's

- Link to the source chart template / reference docs (Reference row).
- Add a `**Related Epics:**` footer linking the epic(s) that scope the test
  (e.g. `&52 - Secrets Manager`).
- Reference concrete cluster/namespace names the test targets (e.g.
  `dcs-monitoring`, `dcs-sealed-secret`, `dcs-gitlab`).
- Include both a **positive** and, where relevant, a **negative** assertion
  (apply-to-wrong-namespace, blocked resource, etc.).
- Make the Automation Proposal specific enough that a test engineer can
  implement it without guessing.

## 8. Don'ts

- Don't leave the case without **Expected Outcome** (that is the core of a test
  case; label `no-description` is discouraged).
- Don't write vague outcomes ("pod should be fine", "check it works").
- Don't dump multiple unrelated behaviors into one test.
- Don't forget the `test::<tool>` or `test-automation::<state>` label — these
  drive the automation backlog.
- Don't drop the environment status labels if the case runs on DE/DIV/ES.
- Don't create the test as a regular issue — it must be the `test_case`
  work-item type so it appears under `/quality/test_cases/`.