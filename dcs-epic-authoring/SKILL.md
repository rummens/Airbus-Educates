---
name: dcs-epic-authoring
description: >
  Write a DCS epic in the house format and create it in GitLab. Use when asked to
  write, draft, or create an epic for the Digital Container Service (DCS) platform —
  a release-sized capability under a "Development Stream R<n>" tracking epic. Produces
  the locked section order (Description, Importance of the Epic, Functional Requirements,
  Non-Functional Requirements, Success Criteria, Roadmap Summary), the required
  P::/complexity::/subproduct:: labels resolved against the live GitLab label list, a
  Mermaid diagram where it explains the capability, full-URL links to related work items
  and public docs, and then creates the epic at group level and returns its URL. Also
  converts a local design document into one epic plus child user-story stubs.
metadata:
  artifact: epic
  gitlab-level: group
---

# DCS Epic Authoring

An epic is a **release-sized platform capability**. It states *what* and *why*, never
per-task acceptance checkboxes — those live in its user stories
(`dcs-user-story-authoring`).

Hierarchy, always three levels:

```
Development Stream R<n>      group epic, label type::tracking-only, body = one line
└─ topic epic                THIS SKILL — one per capability
   └─ user story issues      project issues, ordered, P:: = order inside the epic
```

## 0. Resolve the GitLab target — always first

1. `git -C /projects/<any-repo> remote get-url origin` → GitLab host + group path.
   Any repo under `/projects` works. Never hardcode a host. Never assume gitlab.com.
2. Group = the segment before the project (e.g. `dcs`). **Epics are group level.**
3. If `/projects` is empty or has no git remote, ask for host + group path.

## 1. Discover before writing

| Need | MCP tool | REST fallback |
|---|---|---|
| exact label strings | `list_labels(namespace=<group>, include_ancestor_groups=true)` | `GET /groups/<group>/labels?include_ancestor_groups=true` |
| the release stream epic | `list_work_items(namespace=<group>, types=["EPIC"])` | `GET /groups/<group>/epics?search=Development%20Stream` |
| neighbouring epics to match style | same | same |

**Never invent a label value.** Casing is not guessable — the group uses
`subproduct::naaS`, not `naas`. Copy the exact string the API returned.

## 2. Labels — all three are required

| Label | Values | Infer from | Ask the user when |
|---|---|---|---|
| `P::<n>` | `1`, `2`, `3` | 1 = release goal, customer commitment, or blocks other epics · 2 = planned this release · 3 = opportunistic | no priority signal in the prompt |
| `complexity::<v>` | `low`, `medium`, `high` | low = config/policy change on one component · medium = one new component, one cluster · high = new stack, several operators, or multi-cluster | scope is unclear |
| `subproduct::<v>` | `infrastructure`, `naaS`, `registry` | infrastructure = clusters, nodes, GPU, virtualization, storage, vcluster · naaS = the managed-namespace product: tenancy, policies, upgrades, tenant observability · registry = Harbor, images, supply chain, signing, CI/CD pipelines | the capability spans two, or fits none |

Optional, only when clearly true: `component::<name>` (exact live value),
`external-support` (needs a vendor/RH), `type::dev`.
`type::tracking-only` is for release-stream epics only.

**Never** put `test-de::` / `test-div::` / `test-es::` / `env::` on an epic — those
belong to test cases and bugs.

Ask for every label you cannot infer. One short question listing the allowed values.

## 3. Body — locked template

Use exactly this section order. Every heading is `## `. No emoji in headings.

```markdown
## Description

<One paragraph. The goal of this Epic is to <deliver X> ... Spell out
Digital Container Service (DCS) on first mention. State the delivery
principle where it applies: managed declaratively via **ArgoCD** and
**Helm charts**.>

## Importance of the Epic

<Why it matters, who it serves, what risk it removes. Name the audience:
"This release targets Tenant Application Owners & Security Operations Teams".
Note security/compliance drivers (BSI, SLA, audit) where real.>

## Functional Requirements

* <Concrete deliverable, verb-led: deploy, mirror, harden, blueprint, validate.>
* <...>

## Non-Functional Requirements

* **Security:** <...>
* **Scalability:** <...>
* **Maintainability:** <...>
* **Compliance:** <...>

## Success Criteria

* <Objectively verifiable outcome. "<Capability> can be successfully <done>
  without manual interventions.">
* <...>

## Roadmap Summary

<One or two sentences tying the epic back to the release stream and the
customer outcome. MANDATORY — an epic without this section is not done.>
```

Optional extra sections, only when they carry real content. Each has a fixed slot —
do not place them anywhere else:

| Section | Slot | Use for |
|---|---|---|
| `## Strict Architectural Principle` | directly after `## Description` | a hard constraint, as a `> ⚠️ **CRITICAL CONSTRAINT:**` blockquote — network directionality, isolation boundaries |
| `## Scope` (`### In Scope:` / `### Out of Scope:`) | directly after `## Importance of the Epic` | when exclusions must be explicit |
| `## Milestones / Key Deliverables` | directly after `## Success Criteria` | phased delivery (`**Phase 1:** ...`) |
| `## Documentation` | after Milestones, immediately before `## Roadmap Summary` | links to design docs, wikis, spreadsheets |

`## Roadmap Summary` is always last.

## 4. Diagram

Add one ```mermaid block when the epic describes a **flow, topology, sequence, or
state machine** — data paths, cluster relations, deployment order. Skip it for a
config or policy change.

- ≤ 12 nodes. `flowchart LR` or `sequenceDiagram`.
- No styling directives, no emoji in node labels, no `<br/>`.
- Place it directly after `## Description` or inside the section it explains.

```mermaid
flowchart LR
  NAT[National cluster] -->|remote_write outbound| REC[Thanos Receive]
  REC --> Q[Thanos Querier]
  Q --> G[Central Grafana]
```

## 5. Links

Always **full URLs** — they survive cross-project moves.

- work items: `https://<host>/groups/<group>/-/epics/<iid>`,
  `https://<host>/<group>/<project>/-/issues/<iid>`,
  `https://<host>/<group>/<project>/-/quality/test_cases/<iid>`
- public docs: link freely (`docs.openshift.com`, `kyverno.io`, `goharbor.io`,
  `argo-cd.readthedocs.io`, vendor docs). The instance is not air-gapped.
- Link the sibling/blocking epics and the design doc whenever one exists.

## 6. Language

Formal engineering tone, complete sentences, English only. Title Case title, no
`Epic:` prefix. Bold key terms (`**ArgoCD**`, `**vcluster**`). Real stack names:
OpenShift, ArgoCD, Helm, Operators, CRDs, vcluster, NeuVector, Kyverno, Keycloak,
Harbor, Splunk. Concrete verbs, never "improve" or "look into".

## 7. Create it

Writes are direct — no confirmation gate for a **new** epic. Modifying an
**existing** epic requires the user's explicit OK first.

Order of preference:

1. `glab` if on PATH:
   `glab api --method POST "groups/<group>/epics" -f title="..." -f description=@body.md -f labels="P::1,complexity::high,subproduct::naaS" -f parent_id=<stream-epic-id>`
2. `curl` REST with `$GITLAB_TOKEN`:
   `POST https://<host>/api/v4/groups/<group>/epics`
   fields: `title`, `description`, `labels`, `parent_id`.
3. MCP `create_work_item(workItemType="EPIC", namespace="<group>", ...)` last — it
   takes label **IDs** not names, and has no parent field, so you must follow up with
   `update_work_item`.

Set `parent_id` to the `Development Stream R<n>` epic. If the stream epic for the
target release does not exist, ask before creating one.

Then print the epic's `web_url` so the user can refine it in the UI.

## 8. Design doc → epic + stories

When handed a local design document (Problem / Approach / risks / inline `US-n`
sections):

1. `## Problem` → `## Description` + `## Importance of the Epic`.
2. Approach bullets → `## Functional Requirements`.
3. Risks → `## Non-Functional Requirements`, or a `Strict Architectural Principle`
   blockquote if one is a hard constraint.
4. Per-`US-n` acceptance criteria → **do not keep them in the epic**. Emit them as a
   handoff list for `dcs-user-story-authoring`, one story per `US-n`, in the document's
   order (that order becomes `P::`).
5. Deep technical reference (source files, code excerpts) → `## Documentation` links
   on the epic, and the story body for the story it belongs to.
6. Write `## Roadmap Summary` yourself — design docs never have one.

## 9. Self-check before creating

- [ ] Six `## ` sections present, in the locked order.
- [ ] `## Roadmap Summary` is the last section and is not empty.
- [ ] No acceptance-criteria checkboxes anywhere in the body.
- [ ] `P::`, `complexity::`, `subproduct::` all set, each copied verbatim from the
      live label list.
- [ ] `parent_id` points at the correct `Development Stream R<n>`.
- [ ] Description is one paragraph, not a bullet dump.
- [ ] Every link is a full URL.
- [ ] Mermaid block present if the epic describes a flow/topology, absent otherwise.

## Gold example

Title: `Platform Enablement for Mistral On-Premise AI Multi-Tenant Stack`
Labels: `P::1`, `complexity::high`, `subproduct::infrastructure` · Parent: `Development Stream R5`

```markdown
## Description

The goal of this Epic is to deliver the underlying platform infrastructure,
automation, and operational support necessary to deploy the Mistral On-Premise AI
stack in a multi-tenant architecture. All platform deployments must be managed
declaratively via **ArgoCD** and **Helm charts**. The deployment sequence will begin
with initial validation in the **Sandbox cluster**, followed by provisioning and
hardening a **dedicated virtual cluster (vcluster)** equipped with GPU access.

## Importance of the Epic

Without a hardened, GPU-enabled tenancy the Application team cannot onboard the
Mistral suite on the Digital Container Service (DCS) at all. This release targets
Tenant Application Owners and the central Platform Operations team, and removes the
risk of a bespoke, undocumented deployment that cannot be replicated per country.

## Functional Requirements

* Mirror all required artifacts (images, Helm charts) to internal secure registries.
* Deploy and automate the foundational operators (ClickHouse, APISIX, Temporal) as
  individual lifecycle units with robust test suites.
* Establish a secure workaround for the OpenShift/APISIX cluster-scoped RBAC limitation.
* Deliver an isolated, GPU-enabled **vcluster** for the Mistral multi-tenant workload.
* Provide a global blueprint and documentation for replication across country clusters.

## Non-Functional Requirements

* **Security:** No cluster-scoped RBAC granted to tenant workloads.
* **Maintainability:** Every operator is an independently upgradable lifecycle unit.
* **Compliance:** All images resolve from the internal registry only.

## Success Criteria

* Mistral base Helm charts can be successfully rendered and deployed via ArgoCD
  without manual interventions.
* The APISIX Ingress Controller functions seamlessly behind an OpenShift Passthrough Route.
* Virtual cluster workloads can seamlessly leverage underlying physical GPU resources.
* The Application team successfully deploys their components with zero structural
  platform blockers.

## Roadmap Summary

Bring the Mistral AI Suite to DCS, so the company can use its services.
```
