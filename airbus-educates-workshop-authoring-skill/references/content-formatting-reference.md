# Content Formatting Reference

**House rule: a learner must be able to skim a page and still know what to do.** Depth is
governed by [content-depth-reference.md](content-depth-reference.md); *this* reference governs
how that depth is laid out on the page. The two are not in tension — the same explanation reads
twice as easily when the key nouns are bold, the paragraphs are short, the choices are a list,
and the asides are in call-outs.

Apply it to **every** learner-facing surface of a lab:

| Surface | Formatting applies? |
|---|---|
| `workshop/content/*.md` instruction pages | Yes — full standard |
| `README.md` (the portal course page prospectus) | Yes — full standard, but `> ` blockquote call-outs instead of Hugo shortcodes |
| `academy.dcs/details` annotation (console labs) | Yes — same as README |
| `examiner:execute-test` titles + test script output | Yes — the emoji rules below |
| `workshop/slides/slides.md` | Bold key terms; slides are already lists |
| ConsoleLab `description` / `completionText` step text | **No** — plain text only (see below) |

## 1. Bold the key terms

**Bold the domain nouns and verbs a learner needs to carry forward.** The page's vocabulary
should be visible at a glance without reading a sentence.

- Bold the **first meaningful mention** of each concept on the page: `**Deployment**`, `**Pod**`,
  `**namespace**`, `**Route**`, `**PersistentVolumeClaim**`, `**tenant**`.
- Bold the key **verb** of a step when it is the point of the step: the platform **pulls** the
  image, the Deployment **replaces** the Pod, the change **rolls out**.
- Bold UI targets exactly as they are labelled on screen: the **Slides** tab, the **Actions**
  menu, press **Next**.
- Bold the answer in a `**Answer:**` block, the label in a call-out, and the two halves of a
  contrast (`**Imperative**` / `**Declarative**`).

Do **not**:
- bold the same term again three paragraphs later — after the first mention it is plain prose;
- bold inside or around `code`. A resource name is `hello-dcs` (code), not **hello-dcs**;
- bold whole sentences. If everything is bold, nothing is;
- bold a term at the same time as linking it — a link is already emphasis. Pick one. (An
  existing `[**Deployment**](…)` link is fine; do not add more.)

Rule of thumb: **3–8 bolded terms per page**, not per paragraph.

## 2. Keep paragraphs short — one idea each

- **Two or three lines per paragraph. Never more than three sentences.**
- One idea per paragraph. A second idea means a second paragraph.
- **Split long sentences into separate sentences**, each on its own source line, with a **blank
  line** between them when they are separate ideas.

> **📌 Note:** in Markdown, consecutive lines without a blank line between them render as
> *one* paragraph. Breaking a long sentence across source lines alone changes nothing the
> learner sees. To make the split real, break it into separate sentences **and** either a blank
> line or a list item.

Wrong — one long sentence, one wall:

```markdown
A Deployment is how you tell the platform to keep one copy of this image running for you and
it pulls the image, starts a Pod, keeps it alive, and replaces it if the node it was running
on disappears, which is why you never create Pods directly in production.
```

Right — three ideas, three paragraphs, terms bold:

```markdown
A **Deployment** tells {{< param product_short >}}: *keep one copy of this image running*.

It **pulls** the image, starts a **Pod**, and keeps that Pod alive.

If the node running the Pod disappears, the Deployment **replaces** it. That is why you do not
create Pods directly.
```

## 3. Actions and choices are lists

**Any sequence of two or more actions, and any set of options, facts, or columns to look at, is
a list.** Prose is for explanation; lists are for things the learner has to *scan*.

- **Numbered list** — ordered steps, a sequence of events, a chain (`Deployment → ReplicaSet →
  Pod`), anything where "first / then" matters.
- **Bulleted list** — options, alternatives, fields on a screen, things to notice in the output,
  reasons why.
- Keep each item to **one line** where possible. An item that needs a paragraph is a sign the
  item is really a step with its own explanation — give it a sub-paragraph, indented.
- **Lead each item with its bolded key term**, then an em dash, then the explanation:
  `- **Status** — whether the Pod is running, and why not if it is not.`
- Do not put a clickable action block inside a list item. Introduce the list, then the action.

Wrong:

```markdown
You should look at the STATUS column to see if the Pod is running, the READY column tells you
how many containers passed their probes and RESTARTS tells you whether it has been crashing.
```

Right:

```markdown
Three columns carry the answer:

- **STATUS** — whether the Pod is running, and why not if it is not.
- **READY** — how many of its containers passed their probes.
- **RESTARTS** — whether it has been crashing and being recreated.
```

## 4. Call-outs for hints, warnings, and asides

Anything that is *not* the main line of the page goes in a call-out, so the main line stays
readable and the aside is impossible to miss.

**On instruction pages, use the Hugo admonition shortcodes** (they render as styled boxes — see
[hugo-shortcodes-reference.md](hugo-shortcodes-reference.md)) with a **bold emoji label** as the
first thing inside:

```markdown
{{< note >}}
**💡 Tip:** you can also read this value from the **Slides** tab without leaving the terminal.
{{< /note >}}

{{< warning >}}
**⚠️ Watch out:** the running Pod keeps the *old* value until the rollout finishes. Changing a
ConfigMap does not restart anything by itself.
{{< /warning >}}

{{< danger >}}
**🛑 Careful:** this deletes the namespace and everything in it. It cannot be undone.
{{< /danger >}}
```

**In portal markdown** (`README.md`, `academy.dcs/details`) Hugo shortcodes do not exist. Use a
blockquote with the same bold emoji label:

```markdown
> **💡 Tip:** you do not need a DCS account to run this lab — the session gives you one.
```

The label set — use these, and only these:

| Label | Emoji | For |
|---|---|---|
| `**💡 Tip:**` | 💡 | An optional shortcut, an easier way, a "you can also" |
| `**📌 Note:**` | 📌 | Background or an aside that is not essential to the step |
| `**⚠️ Watch out:**` | ⚠️ | A pitfall, a prerequisite, a surprising behaviour |
| `**🛑 Careful:**` | 🛑 | Destructive or irreversible — `{{< danger >}}` only |
| `**⏳ This takes a moment:**` | ⏳ | The experience note before a slow step (image pull, rollout) |
| `**❓ Answer:**` | ❓ | The revealable answer in a Check Your Understanding block |
| `**💡 Hint:**` | 💡 | The graduated hint on a diagnose-and-fix step |

A **descriptive** bold lead is fine — and usually better — as long as it starts with the
emoji and reads as a label: `**⚠️ Amber means waiting, not broken.**`,
`**📌 Not the OpenShift web console.**`, `**💡 If a box seems to do nothing** — click it
again.` Use the generic `**💡 Tip:**` / `**📌 Note:**` form when there is nothing more
specific to say.

**Budget: two or three call-outs per page, no more.** A page of boxes has no emphasis left.
If boxes start to outnumber the prose blocks between them, the content belongs in the prose
or on its own page.

## 5. Emoji — a small fixed set, used for signposting only

Emoji exist here to make a page scannable, not decorative. The whole sanctioned set:

- 💡 📌 ⚠️ 🛑 ⏳ ❓ — call-out labels (above)
- ✅ — a passing/verifying examiner check, and a completed item in the summary
- 🔍 — an examiner check that verifies *observation* rather than a change
- ❌ — an examiner failure message
- 📊 — the **Slides** tab jump link (already the house convention)

Never put emoji in: page `title:` front matter, headings, resource names, commands, or prose
sentences. One emoji per place, at the start.

## 6. Examiner checks — friendly titles, friendly messages

The learner reads two examiner strings: the `title:` on the button, and the script's output when
it fails. Both are the moment a beginner is most likely to give up, so both get attention.

**Titles** get a leading emoji and stay short:

````markdown
```examiner:execute-test
name: verify-ready
title: ✅ Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```
````

- `✅` for a check that something was **created, changed, or is now working**.
- `🔍` for a check that something was **observed** (an inspection command's state assertion).
- Keep the existing `Verify …` / `Confirm …` wording — imperative, names the outcome.

> **⚠️ Watch out:** the examiner `title:` and `description:` are rendered as **plain text**, not
> Markdown. `**bold**` there shows the asterisks literally. Emoji render fine. Put the bold in
> the surrounding page prose, never in the title.

**Script output** is the diagnostic a stuck learner reads. Keep the expected-vs-found detail
required by [assessment-reference.md](assessment-reference.md), and lead with an emoji:

```bash
#!/bin/bash
# workshop/examiner/tests/verify-ready
avail=$(oc get deploy hello-dcs -o jsonpath='{.status.availableReplicas}' 2>/dev/null)
if [ "${avail:-0}" -ge 1 ] 2>/dev/null; then
  echo "✅ hello-dcs has ${avail} ready replica(s)."
  exit 0
fi
echo "❌ hello-dcs is not ready yet (availableReplicas=${avail:-0}). The image may still be pulling — this check keeps retrying." >&2
exit 1
```

- Success line: `✅ ` then what is true now.
- Failure line: `❌ ` then **what was expected, what was found, and what to do next**. A failure
  message that only states the problem leaves the learner stuck; name the next move ("run the
  apply step above", "check `oc get events`", "this check keeps retrying").
- Plain text only — script output is not Markdown either.

## 7. Page skeleton

The shape every instruction page ends up with:

```markdown
---
title: Deploy It
---

<one or two short paragraphs of what/why, key terms bold>

<the 📊 Slides jump link>

## <A heading per action>

<one short paragraph: what this command does and why>

<terminal:execute>

<what you should see — as a list if it is more than one thing>

<examiner:execute-test with ✅ title>

<{{< note >}} call-out, if the page needs one>

<one short closing paragraph linking to the next page>
```

## Console lab step text is the exception

The academy console plugin renders `ConsoleLab` step `description`, `title`, and
`completionText` as **plain text in a small box beside a highlighted control**. It is not
Markdown: backticks, `**`, bullets, and blockquotes all show up literally. That is why existing
labs write `oc get pods` without backticks.

So in a `ConsoleLab` CR:
- **No** bold, no lists, no call-outs, no emoji.
- The formatting standard applies instead to that lab's `academy.dcs/details` prospectus, which
  *is* markdown and *is* rendered by the portal.
- Skimmability in a step box comes from the existing rule: 2–4 short sentences, one idea each
  (see the console-tour skill's `step-writing-reference.md`).

## Anti-patterns (reject these)

- A five-line paragraph containing three ideas.
- A sentence listing four things the learner should look at, in prose, comma-separated.
- A page with no bolded terms — nothing to anchor a skim.
- A page where every second block is a `{{< note >}}`.
- `**bold**` inside an examiner `title:` (renders as literal asterisks).
- Emoji in a heading or in `title:` front matter.
- Decorative emoji chosen ad hoc (🚀 🎉 🔥) instead of the sanctioned set.
- A blockquote call-out on an instruction page where `{{< note >}}` was available.
- Bolding a term and linking it and putting it in code, all at once.

## Checklist

- [ ] Key domain nouns/verbs bold on first meaningful mention (~3–8 per page, not repeated)
- [ ] No bold inside/around `code`, no bolded sentences, no bold in examiner titles
- [ ] Every paragraph is ≤3 lines and carries one idea
- [ ] Long sentences split into separate sentences with a blank line or a list, not just a line break
- [ ] Every sequence of ≥2 actions is a numbered list; every set of options/facts is a bulleted list
- [ ] List items lead with a bolded term + em dash where they name a thing
- [ ] Hints/warnings/asides are call-outs with a bold emoji label from the sanctioned set
- [ ] `{{< note >}}`/`{{< warning >}}`/`{{< danger >}}` on instruction pages; `> ` blockquotes in README/`details`
- [ ] Two or three call-outs per page at most — boxes never outnumber the prose between them
- [ ] Every `examiner:execute-test` title starts with `✅` (change) or `🔍` (observation)
- [ ] Every examiner script prints `✅ …` on success and `❌ … expected/found/next step` on failure
- [ ] Emoji only from the sanctioned set, only at the start of a call-out label, check title, or check message
- [ ] ConsoleLab step text left as plain text — no markdown, no emoji
