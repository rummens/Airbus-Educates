---
name: airbus-educates-course-review
description: >
  Review an existing DCS Academy Educates course or workshop against the house
  standards and quality criteria, and produce ranked findings with file locations
  and concrete improvement suggestions. Checks OpenShift/`oc` usage, air-gapped
  Harbor images, variablization and the param trio, the mandatory introduction
  page and first-time note, hybrid documentation links, content depth (one
  concept per page; what/why/how; expected output; analogies; diagrams; learning
  styles; realistic duration), examiner coverage (a check for every command) plus
  knowledge check and challenge, the vcluster-vs-namespace decision, `config.yaml`
  params format, split-terminal wording, and planning/cross-reference consistency.
  Optionally, if the user grants access to the internal (otherwise unreachable)
  versioned DCS documentation, it also checks that linked doc pages are still valid
  and relevant, are pinned to a fixed version (never the floating `latest`), and
  whether a newer doc version is available to bump links to.
  Use when asked to review, audit, QA, or grade a DCS academy course or workshop,
  check it against the rules, or suggest improvements. It reports and suggests; it
  does not rewrite unless separately asked.
---

# DCS Academy Course Review Skill

This skill reviews existing Educates workshops/courses built with the
`airbus-educates-workshop-authoring` and `airbus-educates-course-design` skills,
against their house standards. It is the QA counterpart to those skills: they
*create*, this one *checks and advises*.

The authoritative definition of each rule lives in the authoring/course-design
skill references (cited per dimension below). This skill consolidates them into a
review rubric — when a reference is available, consult it for the full rule; when
not, the rubric here is sufficient to review against.

## When to use

- "Review / audit / QA this workshop (or course) against our rules."
- "How can this workshop be improved?"
- Before publishing a workshop, or when returning to an older one.

Scope it first: a **single workshop** (a `workshops/lab-*` dir) or a **whole
course** (the `planning/` docs + all workshops). Confirm scope, then review.

## Review process

1. **Gather.** List the workshop dir(s) and, for a course, the `planning/` docs.
   Read each workshop's `resources/workshop.yaml`, `workshop/config.yaml`,
   `workshop/content/**`, `workshop/examiner/tests/**`, and `exercises/**`.
2. **Review by dimension** (the rubric below). For each check, look at the actual
   files; cite `file:line` for every finding.
3. **Offer the documentation check (optional — must ask).** The DCS documentation
   is **internal and not reachable from anywhere by default**, so this skill
   cannot assume access. Near the start of a review, **ask the user** whether they
   want to grant access to the internal DCS docs for this run (e.g. an internal
   URL/portal, an export, or a proxy). If they decline, skip dimension L and note
   it as not-checked. If they grant it, run dimension L. Never require it.
4. **Verify live (optional but recommended).** If a cluster is available, deploy
   and run the smoke test — setup/ytt/render/link errors only show at runtime
   (see dimension K).
5. **Report.** Ranked findings with severity, location, the problem, and a
   concrete fix. End with prioritized improvement suggestions. Do not edit files
   unless the user asks; this skill advises.

## Severity levels

- **Blocker** — will not work / breaks the session or the automated pipeline
  (e.g. `config.yaml` params as a map; a command with no examiner check; a
  hardcoded external image on the air-gapped platform).
- **Major** — violates a house standard or materially hurts learning (missing
  intro page or first-time note; concept scripted not taught; no diagram for a
  structural concept; `kubectl` instead of `oc`).
- **Minor** — smaller quality issue (inflated duration; missing doc link on a
  first mention; "left/right" instead of "upper/lower" terminal).
- **Suggestion** — optional improvement (an extra analogy, a clearer diagram).

## The rubric

Each item: **Rule** — what must hold · **Check** — how to verify · **Fix** —
the usual remedy. References point at the authoritative source.

### A. Course structure & planning *(course scope)*
- **Rule:** module/track map, naming (`lab-<code>-name`), and cross-references are consistent; plans match built workshops. **Check:** every workshop in a module file has a plan and a dir; "Detailed plan" links resolve; page listings match actual pages. **Fix:** reconcile plan ↔ workshop; fix stale links/names. *(course-design skill.)*

### B. Workshop definition (`resources/workshop.yaml`)
- **Rule:** required sections present; `spec.publish` + `spec.workshop.files` (not deprecated `spec.content.files`); `duration`/`difficulty` set; only needed apps enabled; `examiner.enabled: true`. **Check:** read the YAML. **Fix:** add/correct sections. *(workshop-yaml-reference.)*

### C. Variablization & `config.yaml`
- **Rule:** `workshop/config.yaml` declares `params` as a **list of `{name, value}`** (NOT a map) with the trio `product_name`, `dcs_registry`, `dcs_docs_base_url`. No hardcoded registry/domain/route/namespace/version anywhere. **Check:** open `config.yaml` (a map fails setup with ytt `string index: got string, want int`); grep content/definition for literals. **Fix:** convert to list; replace literals with the right variable plane. *(workshop-variables-reference — Blocker if map.)*

### D. OpenShift / `oc` / run-location
- **Rule:** `oc` everywhere (never `kubectl`); Routes/session-proxy over raw Ingress; SCC-aware; a deliberate **vcluster (default) vs OpenShift namespace** choice recorded (namespace only when operator/real-cluster access is needed; vcluster needs `budget: large` + the `educates-privileged-scc` RoleBinding). **Check:** grep for `kubectl`; read the session config. **Fix:** swap to `oc`; state and justify the run-location. *(openshift-reference.)*

### E. Air-gapped images
- **Rule:** every image from Harbor via `$(image_repository)` or `{{< param dcs_registry >}}`; no external registry (`docker.io`, `quay.io`, `ghcr.io`, `registry.k8s.io`, bare names); workshop image is `dcs-workshop-base`/`dcs-tools`. **Check:** grep all `image:`/pull refs in content, exercises, `*.objects`, `workshop.yaml`. **Fix:** repoint to Harbor; request a mirror. *(air-gapped-images-reference — Blocker for external refs.)*

### F. Introduction page & first-time note
- **Rule:** `00-workshop-overview.md` exists with product framing via `{{< param product_name >}}`, the **first-time note** linking the environment guide via `{{< param dcs_docs_base_url >}}`, What You'll Learn, Prerequisites, Your Environment, Time & Difficulty; no clickable actions. **Check:** read page 00. **Fix:** add the missing elements. *(introduction-page-reference.)*

### G. Documentation links (hybrid)
- **Rule:** first mention of each concept links its docs — standard constructs → upstream; DCS-specific concepts → `{{< param dcs_docs_base_url >}}` with an inline blurb; internal procedures → DCS docs. No standard construct mislinked to the DCS portal, or vice versa. **Check:** scan each page's first mentions. **Fix:** add/repoint links. *(documentation-links-reference, dcs-concepts-reference.)*

### H. Content depth
- **Rule:** one concept per page; each explains **what/why/how** (+ trade-offs), shows and explains **expected output**, explains non-obvious flags; foundational concepts aren't skipped; **structural concepts have a diagram** (SVG page bundle); new abstractions use an **analogy** (VM world) that tapers with skill level; multiple learning styles per key concept; **duration realistic and erring low** (~3 min/guided page). **Check:** read pages; count concepts/page; look for diagrams, analogies, expected output; sanity-check `duration`. **Fix:** split pages; add why/output/diagram/analogy; lower an inflated estimate. *(content-depth-reference.)*

### I. Assessment
- **Rule:** **every command** has a paired `examiner:execute-test` (automated-pipeline coverage; atomic sequences may share one); checks emit **diagnostic** failure messages; a **knowledge check** per workshop and (recommended) an unguided **challenge** with hint + reveal-solution; long-running steps have an experience note + polling check. **Check:** map each `terminal:execute` to a check; read test scripts for diagnostics; confirm the summary section. **Fix:** add missing checks/diagnostics/knowledge-check. *(assessment-reference — Blocker for an unverified command.)*

### J. Clickable actions & terminal
- **Rule:** guided experience (no manual typing); YAML block-scalar safety (`|-`, indent indicators, `|+`+`eot`); dashboard tab visibility tracked; split terminal referred to as **upper/lower** (`execute-1`=upper, `execute-2`=lower), never left/right; terminal working directory tracked. **Check:** read actions and prose. **Fix:** correct wording/YAML/tab guidance. *(clickable-actions reference, workshop-dashboard-reference, content-depth-reference.)*

### K. Live verification *(optional)*
- **Rule:** the workshop actually deploys, renders, its links resolve, and every examiner check passes. **Check:** `crc-local-testing/deploy_workshop.py <name>` then `smoke_test.py <name>` (examiner + link check + restart). **Fix:** address whatever the run surfaces (setup/ytt, render, unreachable link, failing check). *(authoring SKILL "Smoke-Test in a Live Session".)*

### L. Internal DCS documentation currency *(optional — only if access was granted)*
Run this dimension **only when the user has explicitly granted access** to the internal DCS docs (see Review process step 3). The DCS docs are internal and unreachable by default, so **always ask first**; if access isn't given, skip and report "internal-docs check: not run (no access granted)". Never treat missing access as a finding.

When access **is** granted, for **every link that points at the DCS documentation** (`{{< param dcs_docs_base_url >}}/...` in content, plus internal-procedure references):
- **Rule 1 — page still valid & relevant.** The linked page still exists and still describes the concept the workshop links it for (docs get restructured/renamed). **Check:** resolve each DCS-docs link against the internal docs; confirm the target is live and on-topic. **Fix:** repoint to the current page, or flag the workshop text if the underlying concept changed.
- **Rule 2 — pinned to a fixed version, not floating `latest`.** DCS docs are **fully versioned**. Links must use a **fixed version** — do **not** use the floating `latest` tag (it drifts and can silently break or misdescribe). **Check:** grep DCS-docs links for `latest` (or an unversioned path); flag any that float. **Fix:** replace `latest` with the specific current version path.
- **Rule 3 — newer version available (periodic bump).** Because links are pinned, they go stale as the docs release new versions. **Check:** for each pinned link, compare its version against the newest available version in the internal docs; list links that lag. **Fix:** bump the link to the newer version **after confirming the newer page still matches the workshop's intent** (don't bump blindly — a newer version may have moved/changed the content). Treat this as a recurring maintenance pass, not a one-off.

**Severity:** a dead/wrong DCS-docs link is **Major**; a floating `latest` link is **Major** (violates the fixed-version rule); a link that merely lags a newer version is a **Suggestion** (queue for the next bump pass). *(course-brief `dcs_docs_base_url`; documentation-links-reference.)*

## Output format

Report as:

1. **Summary** — scope reviewed; per-workshop status (Excellent / Good / Needs work / Blocked) and a one-line verdict.
2. **Findings** — ranked most-severe first, each: `severity · file:line · problem · fix`.
3. **Improvement suggestions** — a short prioritized list of the highest-leverage changes.

Keep findings concrete and located. Prefer a handful of high-value findings over an exhaustive nitpick list; group repeated issues (e.g. "no docs link on first mention — 6 pages") rather than listing each.

## Skill version

When asked about the skill version, read `VERSION.txt` and report it.
