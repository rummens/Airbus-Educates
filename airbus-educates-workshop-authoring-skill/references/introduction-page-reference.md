# Introduction Page Reference

Every workshop produced with this skill **must** begin with an introduction/overview page: `workshop/content/00-workshop-overview.md`. This is a house standard — it is not optional, even for short workshops.

The introduction page orients the learner before any hands-on work: what product this is part of, what they will learn, what they need to know already, what the environment gives them, and where to go for more depth. It is the first thing every learner reads, so it carries the workshop's framing.

## Required content

The page must contain the following, in this order. Use `##` headings (never `#` — the frontmatter `title` renders the page header).

1. **Product framing (first paragraph).** Open by stating the product/service the workshop is delivered under, using the mandatory variable — never a hardcoded product name:

   ```markdown
   Welcome to this workshop, part of **{{< param product_name >}}**.
   ```

   Follow with one or two sentences describing what the workshop covers (the subject, not the Educates platform).

1a. **First-time note (mandatory).** Immediately after the framing, add a short note for first-time learners pointing to the environment guide, so newcomers learn the terminal/editor/console/actions before diving in. Link the internal guide via the `dcs_docs_base_url` param:

   ```markdown
   {{< note >}}
   **First time in one of these labs?** Take two minutes to read the
   [DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
   it explains the terminal, editor, console, slides and the clickable actions you'll use here.
   {{< /note >}}
   ```

2. **What you'll learn.** A short bulleted list of concrete learning objectives — what the learner will be able to *do* afterwards. Align these with the workshop plan's learning objectives if one exists.

3. **Prerequisites.** What prior knowledge is assumed, and any concepts the learner should already understand. Link the docs for each named prerequisite concept (see [documentation-links-reference.md](documentation-links-reference.md)) so a learner who is missing background can catch up. Example:

   ```markdown
   This workshop assumes familiarity with [containers](https://kubernetes.io/docs/concepts/containers/)
   and basic [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) usage.
   ```

4. **Your environment.** A brief description of what the session provides — the embedded terminal, editor, and any session applications this workshop enables (Kubernetes/OpenShift access, image registry, git server, etc.). Keep it factual and short; describe capabilities the learner will use, not Educates internals. Mention that commands are run with `oc` on OpenShift.

5. **Estimated time and difficulty.** State the expected duration and difficulty so learners can plan. These should match `spec.duration` and `spec.difficulty` in `workshop.yaml`.

6. **Further reading (optional but recommended).** A short list of official documentation links for the main concepts the workshop builds on, so motivated learners can go deeper. See [documentation-links-reference.md](documentation-links-reference.md).

## Rules

- **Product name is a variable.** Always `{{< param product_name >}}` / `{{< param product_short >}}`, never a literal. See [workshop-variables-reference.md](workshop-variables-reference.md).
- **Link concepts to docs.** Any concept named in prerequisites or further reading links to official upstream documentation on first mention.
- **No level-1 heading.** The `title` frontmatter generates the header.
- **Subject over platform.** Describe what the learner will learn about the topic, not how Educates works — unless the workshop is specifically about Educates.
- **No hands-on actions.** The overview is read-only orientation; the first `terminal:execute` / `editor:*` action belongs on `01-*.md` onward.

## Template

```markdown
---
title: Workshop Overview
---

Welcome to this workshop, part of **{{< param product_name >}}**. In it you will
<one-sentence description of the subject and the goal>.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- <objective 1>
- <objective 2>
- <objective 3>

## Prerequisites

This workshop assumes you are comfortable with:

- [<concept>](<official-docs-url>)
- Basic [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) command usage

No prior experience with <advanced thing> is required.

## Your Environment

This session provides a browser-based environment with an embedded terminal and
editor. <State the enabled session applications, e.g. "You have OpenShift access
scoped to your own project, where you will deploy the sample application.">
Commands are run with `oc` in the terminal.

## Time and Difficulty

- **Estimated time:** <matches spec.duration, e.g. 30 minutes>
- **Difficulty:** <matches spec.difficulty, e.g. Intermediate>

## Further Reading

- [<concept> documentation](<official-docs-url>)
- [<related tool> documentation](<official-docs-url>)
```

## Checklist

- [ ] `workshop/content/00-workshop-overview.md` exists
- [ ] Opens with `{{< param product_name >}}` framing — no hardcoded product name
- [ ] Has the first-time note linking the environment guide via `{{< param dcs_docs_base_url >}}`
- [ ] Contains: What You'll Learn, Prerequisites, Your Environment, Time and Difficulty
- [ ] Every named concept in Prerequisites/Further Reading links to official docs
- [ ] Duration and difficulty match `workshop.yaml`
- [ ] No `terminal:execute` or `editor:*` actions on the overview page
