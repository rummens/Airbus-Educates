---
name: dcs-test-case-authoring
description: >
  Write DCS test cases in the house format and create them in GitLab as test_case work
  items. Use when asked to write, draft, or create test cases, test coverage, or a test
  plan for the Digital Container Service (DCS) platform, or to make a story or bug
  testable. Produces the <PREFIX>-TST-<nn> title and matching body ID, the markdown
  table with Prerequisites, copy-pasteable oc Manual Test Steps, objectively assertable
  Expected Outcome, and an Automation Proposal for Kyverno Chainsaw or Robot Framework;
  sets the required type::test, component::, test::<tool>, test-automation::<state> and
  test-de/div/es::<state> labels resolved against the live GitLab label list; never sets
  P:: or release::; files it in dcs-helm-charts under /quality/test_cases/; and returns
  the test case URL.
metadata:
  artifact: test-case
  gitlab-level: project
---

# DCS Test Case Authoring

A test case documents **one objectively verifiable behaviour**: prerequisites, explicit
manual steps, an exact expected outcome, and a concrete proposal for automating it in
**Robot Framework** or **Kyverno Chainsaw**. If the result cannot be asserted
programmatically, it is not a valid test case.

Test cases do **not** live in the epic tree. They live in `dcs-helm-charts` as GitLab
**`test_case` work items** — URL path `/-/quality/test_cases/<iid>`, never `/-/issues/`
— and link back to their epic with a `**Related Epics:**` footer.

## 0. Resolve the GitLab target — always first

1. `git -C /projects/<any-repo> remote get-url origin` → GitLab host + group path.
   Never hardcode a host. Never assume gitlab.com.
2. Target project is `<group>/dcs-helm-charts` unless the user names another.
3. It must be created as work-item type **`test_case`**, not a plain issue.

## 1. Discover before writing

| Need | MCP tool | REST fallback |
|---|---|---|
| exact label strings | `list_labels(namespace=<group>, include_ancestor_groups=true)` | `GET /groups/<group>/labels?include_ancestor_groups=true` |
| existing cases for this component — the prefix in use and the highest `nn` | `list_work_items(namespace=<group>/dcs-helm-charts, types=["TEST_CASE"])` | `GET /projects/<id>/issues?issue_type=test_case&search=<PREFIX>-TST` |
| the epic to reference in the footer | `list_work_items(namespace=<group>, types=["EPIC"])` | `GET /groups/<group>/epics?search=<topic>` |
| the chart template under test | `get_repository_tree` / `get_file_contents` | `GET /projects/<id>/repository/tree` |

**Never invent a label value or a `component::` name.** Copy the exact string the API
returned — the corpus has near-miss names that must not be duplicated.

## 2. The ID prefix

Title format: `<PREFIX>-TST-<nn> - <Verb-led title>`, e.g.
`NP-TST-026 - Harbor Project CVE Allowlist exception Configuration`.

There is **no central prefix registry**. Resolve it in this order:

1. The prompt states the prefix → use it.
2. Search existing test cases for the component (step 1 above) → reuse the prefix
   already in use, and take the highest `nn` + 1.
3. Neither → **ask the user for the prefix.** Never invent one.

Known prefixes seen in the project: `NP-` (namespace provisioner), `SS-` (sealed
secrets), `GRAF-`, `KC-`/`KCST-` (Keycloak), `PGW-` (Pushgateway), `AG-`, `EIP-`
(EgressIP), `SM-` (Service Mesh), `GLR-` (GitLab Runner), `Kasten-`, `Trident-`,
`DCS-` (user scenarios). Sequence is unique **per prefix**.

The `Test Case ID` row in the body must equal the title prefix exactly.

## 3. Labels

### Required

| Label | Values | How to set | Ask when |
|---|---|---|---|
| `type::test` | fixed | always | — |
| `component::<name>` | 1+ | The component under test, exact live value (e.g. `component::namespace provisioner`, `component::keycloak`, `component::harbor`, `component::argocd`, `component::sealed secrets`, `component::monitoring`, `component::logging`, `component::GPU`, `component::EgressIP`, `component::Service Mesh`, `component::GitLab Runner`, `component::Kasten`, `component::operators`, `component::crossplane`, `component::push-gateway`) | no live label matches the component |
| `test::<tool>` | `chainsaw`, `robot`, `python`, `helm-test`, `scenario`, `grafana`, `performance` | Pick by what the assertion needs — see the tool table below | the assertion needs two tools; then split the case |
| `test-automation::<state>` | `planned`, `implemented`, `not-planned` | `planned` on every new case unless the automation already exists | automation status is contested |
| `test-de::` / `test-div::` / `test-es::` | `pass`, `fail`, `planned`, `n/a` | One label per national environment the case targets. `planned` on a new case; `n/a` when the component is not deployed there | you cannot tell which environments the component runs on |

### Tool picker

| Assertion is about | `test::` |
|---|---|
| applying a manifest and asserting the API accepts / denies / mutates it | `chainsaw` |
| an HTTP endpoint, a UI login, a cluster query via KubeLibrary keywords | `robot` |
| logic too involved for Robot keywords, or an SDK/API client flow | `python` |
| a chart's own smoke test hook | `helm-test` |
| a human/tenant workflow with allowed and blocked actions | `scenario` |
| a metric existing, a datasource provisioning, a dashboard query | `grafana` |
| latency, throughput, or resource limits under load | `performance` |

### Forbidden

**Never** set `P::<n>` and never set `release::<n>` on a test case. Prioritisation
belongs on the parent story or epic; release tracking is inherited.

Optional: `status::<state>` (`open` is the default for new items).

Ask for any required label you cannot infer, in one short question listing the allowed
values.

## 4. Body — markdown table template

Use this layout for new cases. (An HTML `<table>` variant exists in the older `SS-` and
`GRAF-` series — match it only when extending one of those directly.)

```markdown
### Test Case <n>: <Short Name>

| | |
|---|---|
| **Test Case ID** | `<PREFIX>-TST-<nn>` |
| **Test Case Name** | `<Verifiable claim, e.g. Verify Route Exception Validation (3-Month Limit)>` |
| **Component(s)** | `<dcs-namespace-provisioner>`, `<ovn-kubernetes>` |
| **Priority** | `<Critical\|High\|Medium\|Low>` |
| **Prerequisites** | 1. `oc` access to the OpenShift cluster with <role>.<br>2. <prereq>.<br>3. <prereq>. |
| **Manual Test Steps** | 1. <concrete command>.<br>2. <command>.<br>3. <command>. |
| **Expected Outcome** | 1. <exact assertable outcome>.<br>2. <outcome>. |
| **Automation Proposal** | <tool> — <what it applies and exactly what it asserts>. |
| **Reference** | <full URL to the chart template / design doc / upstream doc> |

**Related Epics:** <full URL to the epic>
```

Field rules:

- **Test Case ID** — equals the title prefix. Non-negotiable.
- **Test Case Name** — a verifiable claim, not a topic. "Verify …", "Validate …".
- **Component(s)** — backtick-quoted real chart/resource names, comma separated.
- **Priority** — `Critical`, `High`, `Medium`, `Low`. This is a body field only; it
  never becomes a `P::` label.
- **Prerequisites** — numbered `1.` … separated by `<br>`. Never markdown bullets
  inside a table cell; they do not render.
- **Manual Test Steps** — numbered, concrete, copy-pasteable `oc` commands with real
  resource names. Always OpenShift `oc`, never `kubectl`. Include the exact
  `-o jsonpath=` / `-o yaml` flags when the assertion depends on parsing output.
- **Expected Outcome** — numbered and objectively assertable: exit code `0`, status
  `Bound`, `200 OK`, `"allowPrivilegeEscalation":false`, a named column value. Never
  "should work", "pod is fine".
- **Automation Proposal** — name the tool and enumerate the asserts, specific enough
  that a test engineer implements it without guessing. Load
  `references/automation-proposals.md` for per-tool skeletons.
- **Reference** — full URL, pinned to a sha for chart files (`/-/blob/<sha>/...`),
  never `main`.

One test case = one behaviour. Two unrelated assertions = two test cases.

### Scenario layout — `test::scenario` only

For tenant/user-level behaviour (the `DCS-TST-` series):

```markdown
# Objective:
* <what the user or capability must be able to do>

# Preconditions:
* <account, onboarded state, cluster>

# Steps:
* <user action>
* <what the system shows / what the user can then do>
* What is blocked :
  * <negative behaviour that must be forbidden>

# Fail reasons:
* <why the test would fail>
```

Always cover both the positive path and the explicit blocked path.

## 5. Positive and negative

Every case that involves a boundary states both sides:

- success: the resource is created · the status is `Bound` · the command exits `0`
- failure: the `Secret` must **NOT** appear in the other namespace · the API must
  return `401 Unauthorized` · admission must deny with the named policy

Wrong-namespace, wrong-role, expired-exception and over-quota are the usual negative
halves in this platform.

## 6. Diagram

Add one ```mermaid block only when the case tests a **multi-hop flow** — admission
chains, metric push paths, backup/restore sequences — and the diagram makes the step
order unambiguous. Skip it for a single-command assertion.

- ≤ 12 nodes, `sequenceDiagram` or `flowchart LR`.
- No styling directives, no emoji in node labels.

## 7. Links — always full URLs

- epic footer: `**Related Epics:** https://<host>/groups/<group>/-/epics/<iid>`
- the story this covers: `https://<host>/<group>/<project>/-/issues/<iid>`
- the bug it guards against: same form
- chart template under test, pinned:
  `https://<host>/<group>/dcs-helm-charts/-/blob/<sha>/charts/<chart>/templates/<file>`
- public docs freely (`docs.openshift.com`, `kyverno.io/docs`, `goharbor.io`,
  `robotframework.org`). The instance is not air-gapped.

## 8. Create it

Writes are direct — no confirmation gate for a **new** test case. Editing an existing
one needs the user's explicit OK first.

**Use the REST API, not the MCP `create_work_item` tool**: that tool cannot attach
labels to Test Case work items, and the label stack is the whole point here.

1. `glab` if on PATH:
   ```
   glab api --method POST "projects/<group>%2Fdcs-helm-charts/issues" \
     -f title="NP-TST-027 - <title>" \
     -f description=@body.md \
     -f issue_type=test_case \
     -f labels="type::test,component::namespace provisioner,test::chainsaw,test-automation::planned,test-de::planned,test-div::planned,test-es::n/a"
   ```
2. `curl` REST with `$GITLAB_TOKEN`: same endpoint and fields.
3. Verify the returned `web_url` contains `/-/quality/test_cases/`. If it contains
   `/-/issues/`, the `issue_type` did not apply — fix it rather than leaving a plain
   issue behind.

Print the `web_url`.

## 9. Self-check before creating

- [ ] Title is `<PREFIX>-TST-<nn> - <verb-led title>`, `nn` is unused for that prefix.
- [ ] Body `Test Case ID` equals the title prefix, character for character.
- [ ] All nine table rows present, none empty.
- [ ] Steps are copy-pasteable `oc` commands with real names — no `kubectl`.
- [ ] Expected Outcome is numbered and states exact values, codes or statuses.
- [ ] Negative assertion present where a boundary exists.
- [ ] Automation Proposal names the tool and its asserts.
- [ ] Labels: `type::test`, `component::`, `test::<tool>`, `test-automation::<state>`,
      and the `test-de/div/es::` set — all verbatim from the live list.
- [ ] No `P::` label. No `release::` label.
- [ ] `**Related Epics:**` footer present with a full URL.
- [ ] Created as `issue_type=test_case`; `web_url` shows `/-/quality/test_cases/`.

## Gold example

Title: `NP-TST-026 - Harbor Project CVE Allowlist exception Configuration` ·
Labels: `type::test`, `component::harbor`, `test::robot`, `test-automation::planned`,
`test-de::planned`, `test-div::planned`, `test-es::n/a`

```markdown
### Test Case 26: Harbor Project CVE Allowlist Exception

| | |
|---|---|
| **Test Case ID** | `NP-TST-026` |
| **Test Case Name** | `Verify a project-scoped CVE allowlist exception is applied and expires` |
| **Component(s)** | `harbor-core`, `dcs-namespace-provisioner` |
| **Priority** | `High` |
| **Prerequisites** | 1. `oc` access to the OpenShift cluster with the platform-admin role.<br>2. A Harbor project `tenant-demo` exists with vulnerability blocking enabled.<br>3. An image in `tenant-demo` with a known CVE that currently fails the quality gate. |
| **Manual Test Steps** | 1. Confirm the pull is blocked: `skopeo inspect docker://<registry>/tenant-demo/app:1.0` and record the failure.<br>2. Apply the allowlist exception for that CVE with an expiry 30 days out via the provisioner CR: `oc apply -f exception.yaml`.<br>3. Re-run the inspect from step 1.<br>4. Read back the stored expiry: `oc get harborproject tenant-demo -o jsonpath='{.spec.cveAllowlist.expiresAt}'`.<br>5. Set the expiry to a past date and re-run step 1. |
| **Expected Outcome** | 1. Step 1 fails with a vulnerability-policy rejection.<br>2. Step 2 exits `0`.<br>3. Step 3 succeeds and the manifest is returned.<br>4. Step 4 returns the date set in step 2.<br>5. Step 5 is blocked again — an expired exception must NOT permit the pull. |
| **Automation Proposal** | Robot Framework with KubeLibrary and the Harbor REST API: apply the CR, poll `GET /api/v2.0/projects/tenant-demo` until `cve_allowlist.items` contains the CVE, assert the `expires_at` field equals the requested date, assert a pull returns `200`, then patch the expiry into the past and assert the pull returns `412 PRECONDITION FAILED`. |
| **Reference** | https://<host>/dcs/dcs-helm-charts/-/blob/<sha>/charts/dcs-namespace-provisioner/templates/harbor-project.yaml |

**Related Epics:** https://<host>/groups/dcs/-/epics/3
```
