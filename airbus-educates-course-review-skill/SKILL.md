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
  params format, split-terminal wording, plain-language tone (no idioms; no AI-voice
  tells; simple explained commands; declarative/imperative defined before use), the
  always-visible feedback tab, the per-page slides deck (one slide per page, page
  diagrams repeated on their slides, `reload-dashboard` jump links), and
  planning/cross-reference consistency. It also runs the **learner-facing consistency
  sweep** distilled from real cohort feedback: internal lab codes (`A01`) leaking into
  learner text, difficulty/audience/duration disagreeing across README, overview and
  `workshop.yaml`, examiner checks that pass when the step was **not** done, documented
  expected output that a real run does not produce, stale screenshots and slide order,
  and dead or mislabelled links.
  Also reviews CONSOLE LABS (`ConsoleLab` custom resources run by the academy console
  plugin): step depth, a page you open being a page you show something on, every action
  having a reaction, CLI commands named rather than apparently issued, target reachability,
  steps the engine would silently skip, and the portal prospectus.
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

**Two media, two rubrics.** A lab folder holding `resources/consolelab.yaml` is a
**console lab** — a guided tour of the OpenShift web console, not an Educates
workshop. Dimensions C–M do not apply to it (no content pages, no examiner, no
slides, no terminal); review it against **dimension N** instead, plus B2 and E for
its paired `workshop.yaml`. A lab with both files is one lab in two halves: the
Workshop provisions the namespace, the ConsoleLab is the lesson.

## Review process

1. **Gather.** List the workshop dir(s) and, for a course, the `planning/` docs.
   Read each workshop's `resources/workshop.yaml`, `workshop/config.yaml`,
   `workshop/content/**`, `workshop/examiner/tests/**`, and `exercises/**`. For a
   catalog-repo workshop, also read the owning `tracks/<track>/track.yaml` (needed
   for dimension B2). If `resources/consolelab.yaml` is present, read it in full and
   review it under dimension N.
2. **Review by dimension** (the rubric below). For each check, look at the actual
   files; cite `file:line` for every finding.
3. **Offer the documentation check (optional — must ask).** The DCS documentation
   is **internal and not reachable from anywhere by default**, so this skill
   cannot assume access. Near the start of a review, **ask the user** whether they
   want to grant access to the internal DCS docs for this run (e.g. an internal
   URL/portal, an export, or a proxy). If they decline, skip dimension L and note
   it as not-checked. If they grant it, run dimension L. Never require it.
4. **Run the no-cluster checks (always).** `test/workshops/coverage_check.py <lab>` and
   `link_check.py <lab>` need no cluster and catch the two most common regressions —
   a command with no smoke test (dimension I2) and a dead link (I3). Run them every review.
   **Verify live (optional but recommended).** If a cluster is available, also deploy and
   run the smoke test / flow test — setup/ytt/render errors only show at runtime (dim K).
5. **Read it as a learner, not as an author (always).** Most cohort findings are invisible
   to a rule-by-rule file scan; they only appear when the workshop is read front to back as
   a first-timer who has *not* read the plan. Do this pass explicitly and ask:
   - Does every name the learner sees match what the catalog shows them (dim O1)?
   - Do the numbers agree — difficulty, audience, duration, lab number (dim O2)?
   - Is every claim about what the screen will show actually true at that moment (dims H4, O4)?
   - Would a check go green if I skipped the step, or clicked it early (dim I4)?
   - Does anything read like it was generated rather than written (dim H5)?
   Findings from this pass outrank stylistic nitpicks; the first cohort reported almost
   nothing else.
6. **Sweep the feedback regression list (always).** Walk the appendix checklist at the end
   of this skill — every entry is a defect a real learner already reported. It is cheap and
   it is where repeat offenders live.
7. **Report.** Ranked findings with severity, location, the problem, and a
   concrete fix. End with prioritized improvement suggestions. Do not edit files
   unless the user asks; this skill advises.

## Severity levels

- **Blocker** — will not work / breaks the session or the automated pipeline
  (e.g. `config.yaml` params as a map; a command with no examiner check; a
  hardcoded external image on the air-gapped platform; **an examiner check that
  passes when the step was not done**; **an exercise command that fails for the
  learner**, e.g. a write into a mounted volume the container user cannot write).
- **Major** — violates a house standard or materially hurts learning (missing
  intro page or first-time note; concept scripted not taught; no diagram for a
  structural concept; `kubectl` instead of `oc`; **documented expected output the
  real run does not produce**; **a dead or mislabelled link**).
- **Minor** — smaller quality issue (inflated duration; missing doc link on a
  first mention; "left/right" instead of "upper/lower" terminal; **an internal lab
  code in learner text**; **difficulty/duration disagreeing across files**;
  **a stale screenshot**).
- **Suggestion** — optional improvement (an extra analogy, a clearer diagram).

## The rubric

Each item: **Rule** — what must hold · **Check** — how to verify · **Fix** —
the usual remedy. References point at the authoritative source.

### A. Course structure & planning *(course scope)*
- **Rule:** module/track map, naming (`lab-<code>-name`), and cross-references are consistent; plans match built workshops. **Check:** every workshop in a module file has a plan and a dir; "Detailed plan" links resolve; page listings match actual pages. **Fix:** reconcile plan ↔ workshop; fix stale links/names. *(course-design skill.)*
- **A2. Teaching order matches conceptual dependency.** **Rule:** a lab that answers "what is this platform / what are these words" comes **before** the labs that use them; the `academy.dcs/order` sequence in the track reflects that, not the order the labs were authored in. **Check:** list the track in `order` sequence and, for each lab, name the concepts it assumes. A lab assuming a concept only introduced later is the finding. Ask it of the whole track, not per lab — this is invisible in a single-workshop review, so a single-workshop review should still state which track position it assumed. **Fix:** renumber `academy.dcs/order` (and every "in Lab N you…" back-reference with it). *(**Major** — the first cohort asked for exactly this: the "what is DCS" lab sat after "deploy your first app".)*
- **A3. Domain claims are true and complete.** **Rule:** statements about what DCS is, who it serves, and what it is for match the author's model — including scope claims ("serves Airbus Commercial, Defence **and** Helicopters", not Commercial alone). **Check:** list every factual assertion about the platform, its users, and its org; confirm each against the `dcs-domain-corrections` memory / the course brief; flag anything the review cannot source. **Fix:** correct it, or raise it with the author — never guess. *(**Major** — a wrong scope claim is read by the people who own the thing.)*

### B. Workshop definition (`resources/workshop.yaml`)
- **Rule:** required sections present; `spec.publish` + `spec.workshop.files` (not deprecated `spec.content.files`); `duration`/`difficulty` set; only needed apps enabled; `examiner.enabled: true`. **Check:** read the YAML. **Fix:** add/correct sections. *(workshop-yaml-reference.)*

### B2. DCS Academy catalog metadata *(catalog-repo workshops)*
- **Rule:** the workshop lives at `tracks/<track-folder>/<lab>/resources/workshop.yaml`; its `metadata.labels` set `academy.dcs/track` (matching an existing `track.yaml` `id`) and `academy.dcs/order` (a **string**); `metadata.annotations` carry argocd `sync-wave: "5"` + `SkipDryRunOnMissingResource=true`; the owning `track.yaml` has an explicit `id` + `title`. **Check:** read the workshop `metadata` and the sibling `tracks/*/track.yaml`; confirm the `track` label resolves to a real track id. **Fix:** add the `academy.dcs/*` labels / the track.yaml `id`. *(dcs-catalog-metadata-reference — **Blocker**: a workshop with no/mismatched `academy.dcs/track` never renders in the portal.)*
- **Rule (vcluster explicit):** `spec.session.applications.vcluster.enabled` is stated explicitly (`true` or `false`); an `enabled: true` lab **also** has the `educates-privileged-scc` RoleBinding in `spec.session.objects` and `namespaces.budget: large`; operator/SCC/UID topics are native (`false`). **Check:** read the session block. **Fix:** add the flag; for a vcluster lab add the SCC RoleBinding + budget. *(dcs-catalog-metadata-reference — **Blocker**: vcluster `true` without the SCC binding crashloops CoreDNS on OpenShift.)*

### C. Variablization & `config.yaml`
- **Rule:** `workshop/config.yaml` declares `params` as a **list of `{name, value}`** (NOT a map) with the trio `product_name`, `dcs_registry`, `dcs_docs_base_url`. No hardcoded registry/domain/route/namespace/version anywhere. **Check:** open `config.yaml` (a map fails setup with ytt `string index: got string, want int`); grep content/definition for literals. **Fix:** convert to list; replace literals with the right variable plane. *(workshop-variables-reference — Blocker if map.)*

### D. OpenShift / `oc` / run-location
- **Rule:** `oc` everywhere (never `kubectl`); Routes/session-proxy over raw Ingress; SCC-aware; a deliberate **vcluster (default) vs OpenShift namespace** choice recorded (namespace only when operator/real-cluster access is needed; vcluster needs `budget: large` + the `educates-privileged-scc` RoleBinding). **Check:** grep for `kubectl`; read the session config. **Fix:** swap to `oc`; state and justify the run-location. *(openshift-reference.)*

### E. Air-gapped images
- **Rule:** every image from Harbor via `$(image_repository)` or `{{< param dcs_registry >}}`; no external registry (`docker.io`, `quay.io`, `ghcr.io`, `registry.k8s.io`, bare names); workshop image is `dcs-workshop-base`/`dcs-tools`. **Check:** grep all `image:`/pull refs in content, exercises, `*.objects`, `workshop.yaml`. **Fix:** repoint to Harbor; request a mirror. *(air-gapped-images-reference — Blocker for external refs.)*

### F. Introduction page & first-time note
- **Rule:** `00-workshop-overview.md` exists with product framing via `{{< param product_name >}}`, the **first-time note** linking the environment guide via `{{< param dcs_docs_base_url >}}`, What You'll Learn, Prerequisites, Your Environment, Time & Difficulty; no clickable actions. **Check:** read page 00. **Fix:** add the missing elements. *(introduction-page-reference.)*

### F2. Feedback page & always-visible tab
- **Rule:** the **Feedback** tab is **pre-declared** in `spec.session.dashboards` so it is always visible, pointing at `$(ingress_protocol)://academy.$(ingress_domain)/form?workshop=<name>&session=$(session_namespace)`; a `98-your-feedback.md` page exists and **opens** that tab with `dashboard:open-dashboard` (name: Feedback) — **not** the old `dashboard:create-dashboard` pattern. Completion/trophies fire only on form **submit**, so an always-visible tab is safe. **Check:** the `dashboards` entry exists with a `workshop=` matching `metadata.name`; page 98 uses `open-dashboard`, not `create-dashboard`. **Fix:** pre-declare the tab; switch page 98 to `open-dashboard`. *(feedback-page-reference — Minor if missing or still using the old create-dashboard/`feedback.<domain>` pattern.)*

### G. Documentation links (hybrid)
- **Rule:** first mention of each concept links its docs — standard constructs → upstream; DCS-specific concepts → `{{< param dcs_docs_base_url >}}` with an inline blurb; internal procedures → DCS docs. No standard construct mislinked to the DCS portal, or vice versa. **Check:** scan each page's first mentions. **Fix:** add/repoint links. *(documentation-links-reference, dcs-concepts-reference.)*

### H. Content depth
- **Rule:** one concept per page; each explains **what/why/how** (+ trade-offs), shows and explains **expected output**, explains non-obvious flags; foundational concepts aren't skipped; **structural concepts have a diagram** (SVG page bundle); new abstractions use an **analogy** (VM world) that tapers with skill level; multiple learning styles per key concept; **duration realistic and erring low** (~3 min/guided page); **plain language** (no idioms/metaphors/figurative flourishes); **commands kept simple** (no dense chained one-liners — split `a | b && c`; explain flags/operators on first use); **term pairs like declarative/imperative defined before first use**. **Check:** read pages; count concepts/page; look for diagrams, analogies, expected output; grep for idioms and chained-command one-liners; confirm declarative/imperative are defined before use; sanity-check `duration`. **Fix:** split pages; add why/output/diagram/analogy; replace idioms with plain wording; split chained commands; define term pairs; lower an inflated estimate. *(content-depth-reference.)*

- **H2. Expected output is what the command really prints.** **Rule:** every "you should see…" block matches a real run in a real session — including the noise: `Forbidden` lines from API groups the session SA cannot list, warnings, an empty result, an error where the text promised silence. If the noise cannot be removed, the page names it and says it is harmless; better, the command is narrowed so it does not appear. **Check:** run each command in a live session (dim K) and diff against the page. Where no cluster is available, flag every broad command (`oc get all`, unfiltered `describe`, `logs` on a container that failed to start) as unverified rather than assuming. **Fix:** paste the real output; narrow the command; explain the noise. *(**Major** — three separate cohort reports were this: promised events that never appeared, promised silence that printed an error, and `oc get all -l …` spraying kubevirt `Forbidden` lines.)*
- **H3. The words match the screen.** **Rule:** UI elements are called what the dashboard calls them — *terminal*, *tab*, *editor*, *console*; no coined or translated synonyms ("pane"). A tab or button the text tells the learner to open **exists at that moment** in the session. **Check:** grep prose for UI nouns and compare with the dashboard; for each "open the X tab", confirm X is declared/visible at that page (dim F2). **Fix:** rename to the dashboard's word; move the instruction after the tab exists. *(**Minor**, **Major** when the element does not exist yet.)*
- **H4. Code blocks read on a learner's screen.** **Rule:** no command or output line so long it is clipped in the narrow instruction column; long commands are split across lines (`\`) or shortened. **Check:** flag content lines inside fenced blocks over ~80 chars; confirm in a live session at default dashboard width. **Fix:** wrap, split, or shorten. *(**Minor**.)*
- **H5. Written, not generated.** **Rule:** no AI-voice tells — the reassuring contrast clause ("instant, honest feedback that a step worked, instead of guessing"), the tricolon, "let's dive in", "powerful/seamless/simply", second-person hype, a paragraph restating the heading. Prose states what the thing is and what to do. **Check:** read each page aloud; a sentence that could be deleted with no loss of information is the finding. **Fix:** cut it. *(**Major** — a learner rated the workshop down explicitly "because of the AI feeling"; it costs credibility disproportionate to its length.)*
- **H6. Explanation proportion.** **Rule:** the depth of an explanation matches how much the learner has to do with it. Background on why a platform behaves oddly is one or two sentences, not a page; the detail belongs in a doc link. **Check:** any page whose explanation exceeds its action; any rationale for a limitation the learner cannot influence. **Fix:** compress to the operative sentence, link the rest. *(**Minor**.)*
- **H7. The interaction model is taught before it is relied on.** **Rule:** the first page that uses a clickable action explains the affordance — that clicking runs it in the terminal, and what happens if you click twice or click ahead. **Check:** find the first `terminal:execute`/`examiner:execute-test` in the workshop and read what precedes it. **Fix:** add the one-line explanation on page 00/01. *(**Major** — cohort feedback: "it took me the two first chapters to use the quick actions", and premature clicking (dim I4) is the single most-reported defect.)*
- **H8. Repetition is bounded.** **Rule:** a task repeated to teach a pattern is done two or three times, not N; anything beyond that is described, not repeated (e.g. one ticket walked end to end, the rest listed). **Check:** count identical action shapes per lab. **Fix:** collapse the tail into a summary or a table. *(**Suggestion**.)*

### I. Assessment
- **Rule:** **every command** has a paired `examiner:execute-test` (automated-pipeline coverage; atomic sequences may share one); checks emit **diagnostic** failure messages; a **knowledge check** per workshop and (recommended) an unguided **challenge** with hint + reveal-solution; long-running steps have an experience note + polling check. **Check:** map each `terminal:execute` to a check; read test scripts for diagnostics; confirm the summary section. **Fix:** add missing checks/diagnostics/knowledge-check. *(assessment-reference — Blocker for an unverified command.)*

### I2. Smoke-plan coverage (test ↔ workshop linkage)
- **Rule:** the workshop has a smoke plan (`test/workshops/smoke-plans/<lab>.json`) and **every** content `examiner:execute-test` block is either exercised by a plan `check` step (matching test name + args) or listed in the plan's `exclude` with a reason. No content check may be silently untested. **Check:** run `python3 test/workshops/coverage_check.py <lab>` — it must exit 0 (100% accounted for). A workshop with no plan, or a plan missing a content check, fails. **Fix:** add the missing plan step (`--scaffold` bootstraps one from content), or an `exclude` entry with a reason for a CRC-impossible check; use `expect_fail: true` for a step that only passes on the real platform. *(**Blocker**: an untested command can break silently; the whole point of the plan is to catch it.)*

### I3. Link integrity
- **Rule:** every link in the workshop description resolves — external links return 2xx, relative targets (SVGs, sibling pages) exist, and `{{< param dcs_docs_base_url >}}` links use a declared param. **Check:** run `python3 test/workshops/link_check.py <lab>` — external must be reachable (bot-blocked 401/403 are tolerated), relative targets must exist. Internal/air-gapped DCS-docs links are validated separately under dimension L (with `--check-internal --param dcs_docs_base_url=…`). **Fix:** repoint the dead link; add the missing asset. *(a dead upstream link = a learner clicking into a 404; Major.)*
- **Rule (label ↔ target):** the link text names the product whose docs it opens. "Route — Kubernetes documentation" pointing at OpenShift docs (Route is not a Kubernetes object) is wrong twice: mislabelled, and it teaches the wrong ownership. **Check:** for every link, compare the anchor text's product word against the target host/path. **Fix:** relabel or repoint — and check the concept really belongs to the product named (dim G). *(**Minor**, **Major** when it misattributes the concept.)*
- **Rule (reachable from the learner's network):** `link_check.py` runs from the author's machine; learners sit on the national/air-gapped network. Any link whose target is internal (DCS docs, the academy host, the source-code GitLab) is only proven by someone on that network. **Check:** list internal-host links in the report as *unverified from here* unless dim L access was granted, and ask the author to confirm one. **Fix:** repoint to the reachable path. *(**Major** — a 404 on the DCS registry docs page and a dead environment-guide link both reached learners this way.)*

### I4. Check specificity — it must go red when the step was skipped
- **Rule:** every `examiner:execute-test` **fails** when its step has not been done, and fails for the right reason. Three failure modes, all reported by the first cohort:
  1. **Tautological check** — asserts something already true (the resource existed before the step; `oc get` on an object the setup created; an exit code that is 0 regardless). The learner skips the rename and still gets green.
  2. **Order-dependent green** — the check passes because an *earlier* step's state satisfies it, so clicking it before doing the current step goes green. Each check asserts the state **its own** step produces, and asserts the discriminating detail (the new value, the new name, the new revision) — not merely that an object of that kind exists.
  3. **Green on a failed command** — the learner's command errored (`Forbidden`, partial output) and the check still passed because it never inspected what the command actually produced.
- **Check:** for each check, ask *what would this return on a session where the learner did nothing?* Then prove it: in a live session (dim K), run the check **before** performing the step — it must fail — and again after — it must pass. A check that cannot fail is not a check. Grep for the usual tautologies: a bare `oc get <kind>` with no field/value assertion, `|| true`, an unused `grep`, a `wait` with no post-condition.
- **Fix:** assert the discriminating value (`oc get cm x -o jsonpath=…` equals the new value; `oc rollout status` on the new revision); add the precondition assertion with its own diagnostic message so a premature click reports *"step 3 not done yet: configmap still named hello-dcs-conf"* instead of going green or hanging in amber.
- *(**Blocker** — a false green teaches the wrong thing and destroys trust in every other check; it was the most-reported defect of the first cohort, across at least five labs.)*

### I5. Failure messages the learner can act on
- **Rule:** a failed check prints *what* was expected, *what* was found, and *which step* to go back to. Silence with a red state is not a result. **Check:** read each test script's failure path; run one deliberately failing check and read what the learner sees. **Fix:** add the diagnostic echo before the non-zero exit. *(**Major** — cohort suggestion: "the UI only changes to a red state without providing any warning or error message".)*

### J. Clickable actions & terminal
- **Rule:** guided experience (no manual typing); YAML block-scalar safety (`|-`, indent indicators, `|+`+`eot`); dashboard tab visibility tracked; split terminal referred to as **upper/lower** (`execute-1`=upper, `execute-2`=lower), never left/right; terminal working directory tracked. **Check:** read actions and prose. **Fix:** correct wording/YAML/tab guidance. *(clickable-actions reference, workshop-dashboard-reference, content-depth-reference.)*

### M. Slides deck
- **Rule:** each lab ships `workshop/slides/` with the **copy-verbatim** renderer (`index.html`, identical to the authoring skill's `references/slides/index.html`) and `slides.md` — **one slide per instruction page**, enriched (short explanation + bullets + key command + expected result where useful, **not** bare bullets); the slides app is enabled in `resources/workshop.yaml` (`spec.session.applications.slides.enabled: true`); **each page's diagram is repeated on its slide** (the SVG copied into `slides/`); each content page links to its slide via a **`dashboard:reload-dashboard`** action (`name: Slides`, `url: …/slides/#/<id>`) — **never** a plain markdown link like `[…](/slides/#/<id>)` (Educates won't route it). **Check:** `index.html` matches the skill reference **byte for byte** (`md5` it against `references/slides/index.html` — the renderer is copy-verbatim, so a fix to it has to reach every lab); slide count ≈ instruction-page count; every `#/<id>` link resolves to a real slide id; `grep` content for a plain `](/slides/` link (should be none); each page that has an SVG shows it on its slide; **`grep '{{<' slides.md` returns nothing** and the deck uses no markdown beyond the renderer's subset (headings, `-` bullets, `**bold**`, `*italic*`, `` `code` ``, fenced code, images, links) — the renderer prints anything else as literal source text, which is how a `{{< param product_name >}}` and an unrendered `*where*` both reached a learner's screen. **Fix:** copy the renderer; author/enrich `slides.md`; copy diagrams into `slides/`; convert any plain slide link to a `reload-dashboard` action. *(slides-reference — **Major** if the deck is missing; **Minor** for bare-bullet slides, a missing diagram-on-slide, or a plain-link jump.)*
- **M2. Slide order = page order.** **Rule:** slides follow the instruction pages in sequence; a deck that shows Editor before Console while the pages teach Terminal → Console → Editor confuses both. **Check:** list slide ids against page filenames in order and diff. **Fix:** reorder `slides.md`. *(**Minor**.)*
- **M3. Screenshots match the product as it is today.** **Rule:** every screenshot in content **and** in the deck shows the current UI — the current dashboard tabs (Feedback included), the current console, the current portal. A UI change invalidates every image of it, in both places. **Check:** open a live session and compare each image against the real screen; grep for images not touched since the last dashboard/portal change. **Fix:** retake the screenshot in content and in `slides/`; prefer a diagram over a screenshot where the point is structural, since diagrams do not rot. *(**Minor**, **Major** when the text tells the learner to click something the screenshot does not show.)*
- **M4. Nothing on screen leaks what it should not.** **Rule:** screenshots, pasted output and the console tab show no other tenant's data, no tokens, no internal hostnames beyond the ones the workshop already teaches, and no stray warning banners carrying cluster internals. **Check:** read every image and output block for identifiers that are not the learner's own session; open the console tab in a fresh session and read what it displays when empty. **Fix:** crop, redact, or filter the command. *(**Major** — reported against the empty console view: "warnings appear in the empty console, maybe could display sensitive information".)*

### K. Live verification *(optional)*
- **Rule:** the workshop actually deploys, renders, its links resolve, and every examiner check passes. **Check:** `test/workshops/deploy_workshop.py <name>` then `test/workshops/smoke_test.py <name>` (examiner + link check + restart); optionally `test/workshops/flow_test.py` for the session-comes-up + basic-commands user flow. **Fix:** address whatever the run surfaces (setup/ytt, render, unreachable link, failing check). *(authoring SKILL "Smoke-Test in a Live Session".)*
- **K2. Run it as the learner runs it, misbehaving.** The smoke test runs the happy path in order, as the session's own identity, and therefore proves the least. When a cluster is available, also:
  - **Every command, every flag, in the session.** Not just the ones with checks — including writes. A `touch`/`echo >` into a mounted PVC exercises the SCC/`fsGroup`/UID path and is exactly where a lab broke for the first cohort (`Permission denied` on `/opt/app-root/src/data/marker`). Any command whose success depends on identity (write to a volume, `oc create`, `oc policy`, anything needing a role the session SA may lack) is verified in the session, never reasoned about.
  - **Negative pass (dim I4).** Run each check before its step. Every one must fail.
  - **Out-of-order pass.** Click checks ahead of their step and while a previous action is still running; note any that go green, and any that sit in the processing state instead of reporting a precondition failure.
  - **End-of-session pass.** Let the session idle to timeout and close it; the dashboard must degrade into something explained, not a raw *"Application is not available"*. Report what the learner sees at the end as part of the review. *(**Blocker** for a command that fails for the learner; **Major** for an unexplained terminal state.)*

### L. Internal DCS documentation currency *(optional — only if access was granted)*
Run this dimension **only when the user has explicitly granted access** to the internal DCS docs (see Review process step 3). The DCS docs are internal and unreachable by default, so **always ask first**; if access isn't given, skip and report "internal-docs check: not run (no access granted)". Never treat missing access as a finding.

When access **is** granted, for **every link that points at the DCS documentation** (`{{< param dcs_docs_base_url >}}/...` in content, plus internal-procedure references):
- **Rule 1 — page still valid & relevant.** The linked page still exists and still describes the concept the workshop links it for (docs get restructured/renamed). **Check:** resolve each DCS-docs link against the internal docs; confirm the target is live and on-topic. **Fix:** repoint to the current page, or flag the workshop text if the underlying concept changed.
- **Rule 2 — pinned to a fixed version, not floating `latest`.** DCS docs are **fully versioned**. Links must use a **fixed version** — do **not** use the floating `latest` tag (it drifts and can silently break or misdescribe). **Check:** grep DCS-docs links for `latest` (or an unversioned path); flag any that float. **Fix:** replace `latest` with the specific current version path.
- **Rule 3 — newer version available (periodic bump).** Because links are pinned, they go stale as the docs release new versions. **Check:** for each pinned link, compare its version against the newest available version in the internal docs; list links that lag. **Fix:** bump the link to the newer version **after confirming the newer page still matches the workshop's intent** (don't bump blindly — a newer version may have moved/changed the content). Treat this as a recurring maintenance pass, not a one-off.

**Severity:** a dead/wrong DCS-docs link is **Major**; a floating `latest` link is **Major** (violates the fixed-version rule); a link that merely lags a newer version is a **Suggestion** (queue for the next bump pass). *(course-brief `dcs_docs_base_url`; documentation-links-reference.)*

### N. Console labs (`resources/consolelab.yaml`)

The authoritative rules are the **`airbus-educates-console-tour-authoring`** skill and its
references; read `references/step-writing-reference.md` and
`references/consolelab-crd-reference.md` before reviewing one. Walk the steps in order and
keep asking two questions: *what is on screen now?* and *what did the last click do?*

- **N1. Pedagogical contract.** **Rule:** the lab applies concepts a terminal lab already
  taught and introduces none of its own; the prerequisite lab is named in the text.
  **Check:** any step that defines what an object *is*. **Fix:** send the concept back to the
  terminal lab. *(**Major**.)*
- **N2. A page you open is a page you show something on.** **Rule:** every navigation step
  (`href` to a tab, `navigationLink`, a `menuItem`) is followed by at least one step pointing
  at something on the page it opened. **Check:** read the step list alone — a run of
  consecutive navigation steps is the defect. A page with nothing worth highlighting should
  not be opened at all. **Fix:** add a `detailsSection` (a block, by its heading) or
  `pageContent` (a tab body with no heading) step with
  `operation: { type: none }` / `verify: { type: acknowledge }`. *(**Major** — the learner is
  taken to the screen that holds the answer and never shown it.)*
- **N3. Every action has a reaction.** **Rule:** a step whose click changes the screen is
  followed by a step saying what changed. **Check:** each `activateTarget` and each tab
  navigation — is the *next* step about the result, or about somewhere else? The learner reads
  a step **before** acting, so a result described in the acting step is described before it
  exists. **Fix:** split into an action step and an `acknowledge` reaction step. *(**Major**.)*
- **N4. Name the command, do not appear to issue it.** **Rule:** the learner types nothing, so
  a trailing `(oc get cm -o yaml)` reads as an instruction to run it. **Check:** grep the CR
  and the `academy.dcs/details` prospectus for a parenthesised command; the prospectus bullet
  list is the usual offender. **Fix:** rewrite as what the screen replaces — "where
  `oc get cm -o yaml` would print it". *(**Minor**.)*
- **N5. Placement.** **Rule:** every target exists on the page the previous step leaves the
  learner on; no step ends the lab on a signpost (an opened Actions menu with nothing after
  it); the lab lands at least once on the page where the objects are wired together.
  **Check:** trace the page the learner is on step by step. **Fix:** add the missing
  navigation step, or the step that goes through the door. *(**Blocker** for an unreachable
  target: assisted mode stalls and the learner must press Continue.)*
- **N6. No step the engine will skip.** **Rule:** no step's `verify` is already true when the
  step becomes current — detection is continuous, so such a step flashes past unread. **Check:**
  `verify: { type: namespace, value: '<<namespace>>' }` in a hidden lab (the launcher already
  scoped the console), and any `route` verification naming the page the previous step ended on.
  **Fix:** delete the step, or verify the state the learner actually has to reach. *(**Major** —
  invisible in review of the YAML alone; it is why walking the lab is mandatory.)*
- **N7. Step budget.** **Rule:** a pure navigation tour is 4–8 steps; a lab that opens objects
  runs about two steps per page, so 12–17 is normal and is depth, not bloat. **Check:** count
  navigation steps versus content steps — many steps that are all navigation is the failure,
  not the total. **Fix:** split the journey into two tours, or add the missing content steps.
  *(**Minor**.)*
- **N8. Parameters and rendering.** **Rule:** placeholders are `<<name>>`, never `{{ }}` (Helm
  renders the file) and never `$( )` (Educates); `ns` is never declared as a parameter; every
  other placeholder appears in the paired Workshop's `academy.dcs/console-lab-params`.
  **Check:** grep for `{{` anywhere in the file, comments included; compare placeholders
  against the annotation. **Fix:** switch the delimiter; declare the parameter. *(**Blocker** —
  a `{{` fails the Helm render for the whole chart.)*
- **N9. Portal prospectus.** **Rule:** a console lab has no README, so `academy.dcs/details`
  (markdown) is the course page. It states what the lab is, what the learner should already
  know, what they will do, and when the console beats the CLI. **Check:** read the annotation.
  **Fix:** write it. *(**Major** if a single sentence.)*
- **N10. It runs.** **Rule:** the lab walks start to finish with no Continue, every step
  anchored. **Check:** add the lab to `ACADEMY_HIDDEN_LABS` (and `LAB_PARAMS`) in the console
  plugin's `tests/e2e/specs/hidden-labs.spec.ts` and run it; then walk it once by hand. Watch
  for the workflow panel saying *"Waiting for the console element"* — the target exists but the
  engine cannot measure it. **Fix:** whatever the run surfaces.
  *(**Blocker** if it needs Continue; see the authoring skill's `references/testing-reference.md`.)*
- **N11. Pacing.** **Rule:** the highlight/transition animation is short enough to read past —
  it points at the target, it is not the experience. A learner waiting for a full-screen tint to
  finish on every step is being slowed down. **Check:** walk the lab and count seconds from
  step change to the target being usable. **Fix:** shorten or drop the animation.
  *(**Minor** — reported on a console lab: "the animations (coloring the screen in blue) is a
  little bit distracting, if possible it could be good to shorten".)*

### O. Learner-facing consistency *(the cohort-feedback dimension)*

Everything here is cheap to check and was reported by real learners anyway. The theme:
**the learner sees one product, assembled from several files that disagree with each other.**
Review this dimension by reading only what is rendered — the catalog card, the overview
page, the pages, the deck — and never the plan.

- **O1. One name for a lab, and it is the learner's name.** **Rule:** internal codes
  (`A01`, `A06`, `B05`, `lab-a04-storage`) appear **only** in filenames, git paths, labels and
  planning docs — never in a title, an overview, a back-reference, a slide, or a feedback
  form. Learner text uses the catalog's display name ("Lab 2", or the lab's title). A
  back-reference is by display name too: "In Lab 1 you set one value…", never "In A01…".
  **Check:** grep all content, `slides.md` and the workshop/track metadata for `\b[A-Z][0-9]{2}\b`
  and for `lab-[a-z][0-9]{2}-`; every hit outside a file path is a finding. Then render the
  catalog and compare each card's name with the workshop's own title. **Fix:** replace with the
  display name; keep a single mapping table in the track plan. *(**Minor** individually, but it
  was reported by five different learners across four labs — the most frequent finding of the
  first cohort, and it reads as an unfinished product.)*
- **O2. The numbers agree everywhere.** **Rule:** for each lab, these must be one value each:
  **difficulty** (`workshop.yaml` `difficulty` = the overview's "Audience:" line = the catalog
  tag), **duration** (`workshop.yaml` `duration` = the overview's Time line = the README = the
  plan), **position** (`academy.dcs/order` = the "Lab N" the learner is told = the numbering the
  other labs use to refer to it). **Check:** build the table for the workshop (or every workshop
  in the track) and diff the columns — do not eyeball one file at a time, the defect is only
  visible side by side. **Fix:** pick the true value, propagate. *(**Minor**; `Beginner` tag vs
  `Intermediate` audience was reported on three labs, `~5 min` README vs `duration: 10m` on one,
  and an overview saying "Lab 0" in a track whose other labs start at "Lab 2" on another.)*
- **O3. Numbering has no holes.** **Rule:** the displayed sequence is contiguous and starts
  where the catalog starts; a lab removed or reordered does not leave a gap or a duplicate.
  **Check:** list `academy.dcs/order` for the whole track, sorted. **Fix:** renumber. *(**Minor**.)*
- **O4. The prose describes the portal the learner is actually in.** **Rule:** statements about
  the portal and the dashboard — where the feedback form is, what the rating does, what appears
  after submitting, what the tabs are — match current portal behaviour. **Check:** submit the
  feedback form and re-open the catalog; the card must reflect the rating (a card still saying
  "Not yet rated" after rating was reported by four learners). Open each tab the text names.
  **Fix:** correct the text, or raise the portal bug — and say which of the two it is in the
  finding, since these arrive as workshop feedback but are usually portal defects. *(**Major**
  when the text promises behaviour the portal does not have.)*
- **O5. The prospectus and the repo describe this project.** **Rule:** the catalog details, the
  README and any linked source repo describe what the learner is getting, with no leftovers from
  the authoring toolchain (references to Claude Code, the skills, internal planning). **Check:**
  read the portal card, the workshop README, and the public catalog repo README as a learner.
  **Fix:** move toolchain notes out of the learner-facing repo. *(**Minor** — reported verbatim
  by a learner who read the catalog repo README.)*

## Appendix — first-cohort feedback regression sweep

Every line is a defect a real learner reported (July–August 2026, labs A00–A07 + the console
labs). Run the list against each workshop under review; each maps to the dimension in brackets.

| # | What a learner hit | Dimension |
|---|---|---|
| 1 | Check went **green** although the step was skipped / clicked early | I4, K2 |
| 2 | Check went **amber and stayed processing** on a premature click instead of reporting a precondition | I4, H7 |
| 3 | Check went green although the command printed `Forbidden`/errors | I4, H2 |
| 4 | Failed check showed red with no message | I5 |
| 5 | Documented events/log output never appeared in the real run | H2, K2 |
| 6 | `Permission denied` writing into the mounted volume | K2 |
| 7 | Internal lab code (`A01`, `B05`, "Lab 0") in learner-facing text | O1 |
| 8 | `Beginner` tag vs `Intermediate` audience; README duration vs `workshop.yaml` | O2 |
| 9 | Dead DCS-docs link (404 on the national network) | I3, L |
| 10 | Link labelled "Kubernetes documentation" pointing at OpenShift docs | I3, G |
| 11 | Screenshot / slide image older than the dashboard it shows | M3 |
| 12 | Slide order not the page order | M2 |
| 13 | Text says "open the Feedback tab" before the tab exists | H3, F2 |
| 14 | Clickable actions not discovered until two chapters in | H7 |
| 15 | Prose reads AI-generated; over-long rationale for a platform quirk | H5, H6 |
| 16 | UI called by a coined name ("pane") | H3 |
| 17 | Code block too narrow to read the line | H4 |
| 18 | Commands compact and under-explained; learner wants to type some, not only click | H (depth), H7 |
| 19 | Structural concept with no analogy (tenancy: building / rooms) | H (analogies) |
| 20 | Fundamentals lab sequenced after the labs that use it | A2 |
| 21 | Platform scope claim incomplete (Commercial only vs Commercial + Defence + Helicopters) | A3 |
| 22 | Rating submitted but catalog still says "Not yet rated" | O4 |
| 23 | Session end / idle shows raw "Application is not available" | K2 |
| 24 | Warnings in the empty console possibly exposing internals | M4 |
| 25 | Same manual task repeated many times (ticket after ticket) | H8 |
| 26 | Console-lab animation too long / distracting | N (step pacing) |

When a review finds a **new** class of learner-reported defect, add a row here and, if it is not
already covered, a rule above — this table is the skill's memory of what actually goes wrong.

## Output format

Report as:

1. **Summary** — scope reviewed; per-workshop status (Excellent / Good / Needs work / Blocked) and a one-line verdict. State which passes ran (no-cluster checks, learner read-through, live/negative pass) and which did not, so the reader knows what is unverified rather than clean.
2. **Findings** — ranked most-severe first, each: `severity · file:line · problem · fix`. Mark each finding **content** (fix in the workshop) or **platform** (fix in the portal / dashboard / console plugin) — cohort feedback arrives mixed, and routing it is half the value.
3. **Consistency table** — for dimension O2, the difficulty / duration / order columns per workshop, so disagreements are visible at a glance.
4. **Improvement suggestions** — a short prioritized list of the highest-leverage changes.

Keep findings concrete and located. Prefer a handful of high-value findings over an exhaustive nitpick list; group repeated issues (e.g. "no docs link on first mention — 6 pages") rather than listing each.

## Skill version

When asked about the skill version, read `VERSION.txt` and report it.
