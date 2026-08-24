# DCS GitLab artifact skills

Four opencode skills that write DCS work items in house format and create them in
GitLab. Derived from `epics_language/` (the encoded rules plus 14 real epics and 175
real user stories) and adapted from four public PM/QA skills.

| Skill | Artifact | GitLab level |
|---|---|---|
| `dcs-epic-authoring/` | topic epic under `Development Stream R<n>` | group |
| `dcs-user-story-authoring/` | user story issues (+ splitting) | project |
| `dcs-bug-authoring/` | `type::bug` issues under `ContainerHub Ops & Bugs` | project |
| `dcs-test-case-authoring/` | `test_case` work items in `dcs-helm-charts` | project |

## Install

opencode requires `<dir-name>/SKILL.md` with `name:` equal to the directory name.
Discovery paths, project level first:

```
.opencode/skills/<name>/SKILL.md
.claude/skills/<name>/SKILL.md
.agents/skills/<name>/SKILL.md
```

Global: `~/.config/opencode/skills/<name>/`. Copy or symlink the four directories into
one of those. Keep the directory names — renaming one breaks its frontmatter.

## Hierarchy the skills assume

```
Development Stream R<n>        group epic, type::tracking-only, body = one line
├─ topic epic                  P:: complexity:: subproduct::
│  └─ user story issues        type:: P:: (= work order inside the epic), milestone "Release <n>"
└─ ContainerHub Ops & Bugs     bugs: type::bug P:: env::
test cases                     dcs-helm-charts → /-/quality/test_cases/, own label stack
```

## Label rules, at a glance

| Artifact | Required | Never |
|---|---|---|
| epic | `P::1-3`, `complexity::low\|medium\|high`, `subproduct::infrastructure\|naaS\|registry` | `env::`, `test-*::` |
| user story | `type::dev\|deployment\|spike\|test\|docs\|bug`, `P::1-3` (order inside epic) | `env::`, `test-*::` |
| bug | `type::bug`, `P::1-3` (severity **and** priority), `env::de\|div\|es` | `test-*::` |
| test case | `type::test`, `component::`, `test::<tool>`, `test-automation::<state>`, `test-de/div/es::<state>` | `P::`, `release::` |

Every skill resolves the exact strings from the live GitLab label list first and asks
the user for anything it cannot infer. Casing is not guessable — the group uses
`subproduct::naaS`.

## Design choices

- **Target model is DeepSeek** (reasoning + interleaved on). So: literal fill-in
  templates instead of descriptions of templates, decision tables instead of
  judgement calls, closed label vocabularies inline with "never invent a value", one
  gold example per skill taken from the real corpus, and a self-check list before any
  write. Deeper material sits in `references/` and is loaded only when needed.
- **No validator scripts.** Live label discovery plus the GitLab API rejecting bad
  values covers the same failure mode without four copies of a linter to maintain.
- **Writes are direct for new items**, and gated on an explicit OK for edits to
  existing ones. Every skill prints the `web_url` so the item can be refined in the UI.
- **GitLab target is discovered**, never hardcoded:
  `git -C /projects/<any-repo> remote get-url origin`.
- **Mermaid only** for diagrams, added when the artifact describes a flow, topology,
  sequence or state machine. Links are always full URLs, chart links pinned to a sha.

## Divergences from the public skills they are based on

- `user-story`: kept the `As a / I want / So that` opening — mandatory on every story —
  and the one-When/one-Then split heuristic. **Dropped Gherkin**: zero occurrences
  across 175 real stories, so acceptance criteria are checkboxes. Titles stay imperative
  and task-shaped; the persona lives in the body.
- `epic-hypothesis`: kept falsifiable success criteria and outcome-over-output;
  dropped the if/then bet framing, experiments-before-build, and product metrics.
  "Tiny act of discovery" maps to a `type::spike` story.
- `user-story-splitting`: kept 6 of 8 patterns; **reversed its ban on horizontal and
  DevOps splitting** — DCS legitimately splits by environment, lifecycle step and
  component, because each of those slices is separately deployable and verifiable.
  Added 6 house patterns (`references/splitting-patterns.md`).
- `qa-test-planner`: kept preconditions/steps/expected structure; dropped Figma,
  browser matrices, bug reports and `TC-001` ids in favour of the `test_case` work
  item, the label stack, `oc` steps and Chainsaw/Robot automation proposals.

## Corpus findings worth keeping in mind

- The encoded rules are aspirational; the corpus is looser. 73 of 175 stories match
  neither documented template, 64 have no checkbox criteria, median body is ~1.3 kB.
  A short story is normal — the skills state a floor, not a maximum.
- A **third de-facto story template** exists that the rules do not name: `# Description`
  \+ `* **Key Requirements:**` + `**Acceptance Criteria**` checkboxes. It is the most
  common shape for platform work, so it became **the** story template — the full
  developer template and the standalone persona template were dropped, and the
  `As a / I want / So that` opening folded into the one that remains.
- `&41` numbers its stories to match the epic's phases — that convention is encoded as
  optional title numbering.
- `epics_language/epic-oauth-console-login-customization.md` is a *local design doc*,
  not a published epic: it packs stories inline and has no Roadmap Summary. The epic
  skill has an explicit converter path for that shape.

## Open items

- **Test case ID prefixes have no central registry.** The skill searches existing cases
  for the component and asks when it finds nothing. A registry file would remove that
  question.
- **Which project holds epic child stories** is inferred from the parent epic's existing
  children. Pin it in a skill edit if it is always the same project.
- **Label taxonomy is unverified against the live instance** — the GitLab MCP available
  during authoring pointed at gitlab.com. First real run will confirm it.
