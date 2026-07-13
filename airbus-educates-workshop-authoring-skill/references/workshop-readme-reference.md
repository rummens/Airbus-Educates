# Workshop README Reference (house standard)

Every workshop has a root **`README.md`**. It is the workshop's **description /
prospectus** — the "should I take this lab?" page a learner reads *before* they
launch. It is surfaced in two places, so write it for both:

1. **DCS Academy portal, course-detail view** — rendered as the rich body below the
   title, meta pills, and rating. This is the primary audience.
2. **Git / repo browsing** — read standalone on the source host.

## What the portal renders FOR you (do NOT duplicate as hardcoded prose)

The course-detail page already prints, as chrome around the README:

| Rendered by the portal | Source |
|---|---|
| The **title** as the page `<h1>` | Workshop CR (`spec.title` / `academy.dcs/display-name`) |
| **Duration** + **difficulty** pills | CR (`spec.duration`, `spec.difficulty`) |
| A **live community star rating** + review count | feedback DB, live |
| Track / lab sequence, "Start session" button | catalog + portal |

Consequences:

- **The portal strips the README's own leading `# H1`** before rendering (so the
  title isn't printed twice). Keep an `# Title` at the top anyway — it's the title
  when the file is read standalone on Git; the portal drops it.
- **Never hardcode the rating / "community feedback" into the README.** It is shown
  live from the database and would go stale instantly. (This is the one item on a
  naive "what a description needs" list that belongs to the platform, not the file.)
- Duration and difficulty appear in pills; you *may* still list them in the meta
  block below for standalone Git readers — a small, harmless duplication. Keep them
  in sync with the CR (which is the source of truth).

## Required structure

```markdown
# <Human Title>          <!-- e.g. "What is DCS?" — portal strips this; keep for Git -->

**<One-sentence hook>** — what this lab is and who it's for, in a single bold line.

<Lead paragraph: what we talk about. 2–4 sentences of plain prose — the topic, why
it matters on DCS, and the shape of the hands-on work. No marketing, no command dumps.>

- **Track:** Core — DCS Foundations · Lab 1 of 9
- **Audience:** Beginner — no Kubernetes experience needed
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in <a per-session vcluster | your OpenShift session namespace>
- **Prerequisites:** <prior labs by metadata.name, then a semicolon and the assumed background — e.g. "lab-a02-kubernetes-essentials; comfortable with the Linux CLI">

## By the end of this lab you'll be able to

- <Verb-first objective — "Explain what a container image is and how DCS stores it">
- <3–6 bullets. Concrete, learner-facing, testable. Mirror the workshop's learning objectives.>

## What you'll do

<Short paragraph or 3–5 bullets outlining the hands-on flow / what you build — the
concrete deliverable, e.g. "deploy a sample app with `oc`, scale it, and read its logs".>

## Before you start   <!-- OPTIONAL: only when prerequisites need real explanation -->

<Prior labs to finish first, external accounts/tools/access needed, or assumed
knowledge. Skip the heading entirely if the one-line meta prereq says it all.>
```

## Rules

- **Match the CR.** Duration/difficulty in the meta block must equal `spec.duration`
  / `spec.difficulty`; audience should reflect difficulty. Prerequisites should name
  actual prior labs by `metadata.name`.
- **Prerequisites read as one clause.** List prior labs, then a semicolon and the
  assumed background. Don't write "none" (state the real assumed background — a login,
  Linux CLI, etc.) and don't label a part "external:" — just say it plainly.
- **Name tracks, not modules.** In the meta block and the prose, refer to a body of
  prior work by the **track name** the learner sees in the portal (e.g. "the Core
  track", "the Developer track") — not by an internal module letter ("Module A"). The
  meta label is `**Track:**` (the earlier `Track / module` form is retired). Don't
  reference tracks/modules that don't exist in the catalog.
- **Objectives are the contract.** The "By the end…" bullets are what the workshop
  actually teaches and what the knowledge check verifies — keep them honest and in
  sync with the content and `00-workshop-overview.md`'s *What You'll Learn*.
- **Prose, not commands.** No clickable actions, no `oc` invocations, no examiner
  blocks — this is a description, not a content page.
- **Variablize the product name** where natural (`Digital Container Service (DCS)`),
  but a README may hardcode DCS naming for readability since it isn't ytt-rendered.
- **Keep it scannable.** Hook → lead → meta → objectives → what-you'll-do. A learner
  should decide in 20 seconds. Depth lives in the workshop pages, not here.
- **Don't restate the overview verbatim.** `00-workshop-overview.md` is the in-lab
  orientation; the README is the pre-launch pitch. Overlap on objectives is fine;
  don't copy the whole environment section.
