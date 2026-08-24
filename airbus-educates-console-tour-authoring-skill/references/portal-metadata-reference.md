# Portal catalog metadata for a console lab

A terminal lab's rich description is its `README.md`, fetched from git. **A console lab has no
content directory, so there is no README** — its course page is built entirely from annotations
on the Workshop CR. Leave them thin and the lab looks unfinished next to every other lab in the
catalog.

Where each field surfaces:

| Field | Surfaces as |
|---|---|
| `spec.title` / `academy.dcs/display-name` | the tile title and the course page `<h1>` |
| `academy.dcs/summary` | the one-line hook on the catalog tile |
| `spec.description` | the lead paragraph on the course page |
| `academy.dcs/details` | the full prospectus below it — **markdown, rendered** |
| `academy.dcs/duration`, `difficulty` | the pills on the tile and course page |
| `academy.dcs/icon` | the tile icon — use `monitor` for console labs |
| `academy.dcs/lab-format: console` | the "Console lab" badge (and the redirect behaviour) |

## Summary

One sentence, the hook. Say what the learner will do and that it happens in the console. Connect
to the CLI they already know.

> Do the pod investigation you already know from the terminal — get pods, logs, rsh — in the
> OpenShift web console instead, guided step by step.

## Description

Two to four sentences. Name the prerequisite terminal labs explicitly and state what this tour
adds. This is the paragraph that decides whether someone starts the lab.

> You already inspected workloads from the terminal in Deploy Your First App and Configure &
> Troubleshoot Your App, using `oc get pods`, `oc logs` and `oc rsh`. This lab walks the same
> investigation through the OpenShift web console, so you can recognise each command's
> equivalent on screen and pick whichever tool is faster for the job.

## Details (the prospectus)

Markdown, in a YAML block scalar. Cover, with `###` headings:

1. **What this lab is** — that it is a console lab: no instruction pages, the step is highlighted
   on the live console, the environment is real and created for them.
2. **What you should already know** — the prerequisite labs by title, and an explicit statement
   that no new concepts are introduced.
3. **What you will do** — a short bullet list of the journey, each with its CLI equivalent in
   backticks.
4. **When to reach for the console** — the honest trade-off against the CLI. Console for looking
   around and correlating; CLI for anything repeatable, scriptable or reviewable.
5. **Cleaning up** — that Finish records the completion and shuts the environment down.

```yaml
    academy.dcs/details: |
      ### What this lab is

      A **console lab**. Instead of a terminal and instruction pages, ...
```

`lab-u01-container-access` is the reference implementation.

### Formatting the prospectus

`details` and `summary` are the console lab's only markdown surfaces, so the house
skimmable-formatting standard applies to them in full — see
[the workshop skill's content-formatting-reference.md](../../airbus-educates-workshop-authoring-skill/references/content-formatting-reference.md):

- **Bold the key terms** on first mention (`**console lab**`, `**Logs** tab, the prerequisite
  lab titles).
- **Paragraphs of ≤3 lines**, one idea each. Split long sentences.
- Every journey step and every option is a **list item**, led by its bolded term where it names
  one.
- Hints and cautions go in a **blockquote call-out** — the portal renders markdown, not Hugo, so
  `{{< note >}}` is unavailable:

  ```markdown
  > **💡 Tip:** you will not type a single command — every screen names the `oc` command it
  > replaces, so you can map one onto the other afterwards.
  ```

- Two or three call-outs at most. Emoji only from the sanctioned set (💡 📌 ⚠️).
- None of this reaches the step boxes — see
  [step-writing-reference.md](step-writing-reference.md).

## Ordering and tracks

- `academy.dcs/track` puts the lab in a track; `academy.dcs/order` sorts it within that track.
- Place a console lab **after** the terminal labs it depends on. The order number is the promise
  that its prerequisites come first.
- Default tours (`tour-*`) usually have no Workshop CR at all, so they never appear in the portal
  catalog — they live only in the console's own lab list. Only labs with a Workshop CR are
  portal-visible.
