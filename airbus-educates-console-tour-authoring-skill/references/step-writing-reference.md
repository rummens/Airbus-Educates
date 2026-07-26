# Writing step text

The step box is small and sits beside a highlighted control. It is the whole lesson for that
screen. Two failure modes, and the second is the common one:

- too long — nobody reads a paragraph while a button is glowing at them;
- too thin — "Click Deployments" teaches nothing that the highlight did not already say.

**Target: 2–4 sentences, roughly 25–60 words.** Enough for a reason, not a lecture.

## What a step must contain

1. **What this screen is for** — the job a practitioner comes here to do.
2. **Why it matters** — the reason, the risk, or the trade-off. This is the part usually missing.
3. **The CLI equivalent** — the command from the terminal lab they already did (`oc get pods`,
   `oc logs -f`, `oc describe`). This is the hook that connects the two formats.

Optional, when it earns its place: a caution, or what to notice on screen (a column, a status,
a selector).

Do **not** include: what to click (the highlight says it), concept definitions (the terminal lab
taught them), or restating the step title.

## Before and after

**Too thin — the reported problem:**

> Open Deployments
> Click on Deployments to see the deployments.

Says nothing the highlight did not. No reason, no connection to prior learning.

**Too heavy — re-teaching:**

> A Deployment is a Kubernetes object that manages a ReplicaSet, which in turn manages Pods. It
> provides declarative updates, rollback, and scaling. Deployments are the standard way to run
> stateless applications on Kubernetes and were introduced in version 1.2 …

The learner met all of this in *Deploy Your First App*. Repeating it wastes the box and implies
the terminal lab did not count.

**Right:**

> Deployments show desired replicas, availability and rollout status on one row — the same facts
> you read from `oc get deployment`, without re-running it. This is where you check whether a
> rollout finished before you start debugging the pods underneath it.

Job, reason, CLI equivalent, and something to notice.

## Name the command, do not appear to issue it

A console lab runs entirely in the browser. The learner types nothing. So a trailing
parenthesis holding a command reads as an instruction to run it:

> Open the project's ConfigMaps and read the application config (`oc get cm -o yaml`)

Write the command as the thing this screen *replaces*, never as something to do:

> Read the application config, values and YAML, where `oc get cm -o yaml` would print it

Phrases that work: "the same facts `oc get deployment` reports", "the screen behind
`oc set env --from`", "what you read with `oc describe`", "this form and `oc set` write the
same field". Applies to step text, `completionText`, and the `academy.dcs/details` prospectus
alike — the bullet list in the prospectus is the usual offender.

## Getting to a page is half a step — teach the page

The common gap in a finished lab is not the navigation. It is what happens after the object
opens: the tour explains where ConfigMaps live and what they are for, the learner arrives on the
ConfigMap, and the next highlight is already a different sidebar link. The screen with the actual
information on it was never explained.

**Rule: whenever a step opens a details page, the following steps explain that page** — before
the tour navigates away. A details page has three parts, and a console lab is largely about
knowing they exist:

| Part | What it holds | Worth its own step when |
|---|---|---|
| The Details tab | the fields the console chose to render — values, status, selectors, owner | there is something to notice that the CLI prints differently |
| The other tabs | YAML, Pods, ReplicaSets, Environment, Events, Logs, Terminal | the tab answers a question the Details tab cannot |
| The Actions menu | everything that writes: Edit …, Restart rollout, Delete | once, in a lab whose subject includes changing the object — it is the console's `oc set` / `oc edit` / `oc delete`. A read-only lab (inspect a pod, follow the traffic chain) is complete without it |

Reach for the specific control, not a paragraph about it. `revealSecretValues` highlights the
Reveal values button; `actionsMenu` highlights the Actions toggle; a tab is an `href` target.
A sentence saying "the Environment tab lists them" is not the same lesson as standing on the
Environment tab looking at them.

### The rule: a page you open must be a page you show something on

**Every navigation step is followed by at least one step that points at something on the page
it opened.** If there is nothing on that page worth highlighting, the lab had no reason to open
it — cut the navigation step instead.

The page a step arrives at often has nothing to click: a ConfigMap's values, a Deployment's
strategy fields, the env sources on the Environment tab. Those get their own step with
`target: { type: consoleElement, id: detailsSection, value: <the section's heading> }` and:

```yaml
complete:
  operation: { type: none }
  verify: { type: acknowledge }
```

`acknowledge` never satisfies itself, so the step stays on screen until the learner presses
**Next**. That is the point: the step exists to be read.

This also fixes the two-sentence navigation step. When the *next* step explains the content,
the navigation step only has to say what kind of thing is over there and why to go:

> **Open the application config** — The details page has two halves: the metadata at the top,
> and the configuration itself lower down. What you came for is the lower half.
>
> **Read the values** — Every key in this ConfigMap is listed below with its full value,
> unhidden and wrapped for reading. This is the console's answer to printing the object with
> `oc get configmap app-config -o yaml` …

**Do not end a lab on a signpost.** A last step that opens the Actions menu and stops has
pointed at a door without going through it. Follow it with the `menuItem` the lab is about, and
then a step on the page that opens.

### Every action has a reaction

**A step that makes something happen is followed by a step that says what happened.** The
learner reads a step's text *before* they act on it, so a step whose text describes the result
is describing something not on screen yet — and by the time it is, the box has moved on.

Reveal values is the clearest case. The old lab explained decoding in the step that asked for
the click, then jumped straight to the Deployment: the moment the plain-text values appeared,
the guidance was already talking about something else.

Split it in two. The action step says what to do and why; the reaction step, an `acknowledge`
on what changed, says what the learner is now looking at:

> **Reveal the values** — target `revealSecretValues`, verify `targetText: Hide values`
>
> **What that just did** — target `detailsSection: Data`, verify `acknowledge` — "Every key is
> now readable in plain text … Nothing was unlocked: the value was never encrypted, only
> encoded."

The same split applies to a tab. `open-pods-tab` becomes one short step ("A replica count is a
number. The pods behind it are on the next tab") plus `read-pods-tab` on the table that
appeared. Tab bodies carry no heading, so their reaction step targets `pageContent`.

A navigation step whose *next* step acts on the page it opened already has its reaction — a
list page followed by a step that opens a row from it needs nothing extra.

**Link the objects to each other.** A lab that shows a ConfigMap, then a Secret, then a
Deployment has shown three pages, not a system. One step must land on the page where the
relationship is visible — the Deployment's Environment tab, a Service's pod selector, a PVC's
mounting pod — and say that this is where the wiring lives.

This is why a lab that opens two or three objects runs longer than the 4–8 steps of a pure
navigation tour: roughly two steps per page it opens, one to go and one to look. Fifteen to
seventeen steps is fine when they are teaching object pages; eight is too many when they are
all navigation.

A step that highlights a whole block puts a large ring on the page, and the guidance box sits
beside it. Both are over the console, so a learner reading a long YAML or a wide table may want
them gone: the panel's **Hide** button removes the spotlight and the box until they press
**Show guidance**, and the lab keeps running underneath. Say so in the step text on the pages
where it matters — a YAML tab is the usual one.

## Voice

Follow the house rules from the workshop authoring skill:

- Plain language. No idioms, no metaphors, no "simply", "just", "easily".
- Short sentences. One idea each.
- Second person, present tense: "you check", not "the user can check".
- British-neutral spelling consistent with the rest of the catalog.
- Never promise that the GUI is better than the CLI. Say when each is faster — the console for
  looking around and correlating, the CLI for anything repeatable or reviewable.

## Referring back to terminal labs

Name them by title, as the learner sees them in the catalog:

> …as you did in **Configure & Troubleshoot Your App**.

Reference the lab when the tour applies a concept it taught, and the command when the screen has
a direct CLI equivalent. Do not reference a lab that comes *later* in the track.

## Titles and completion text

- **Step title**: imperative, 2–5 words. "Open Pods", "Read the logs", "Select the project".
  Not "Pods" (not an action), not "Now let us open the Pods list" (too long).
- **`completionText`**: one or two sentences naming what the learner can now do, tied back to the
  CLI. "Done. You located a pod, read its logs, and opened a shell inside its container —
  the console equivalent of `oc get pods`, `oc logs` and `oc rsh`."

## A worked step set

`lab-u01-container-access` is the reference implementation:
`workshops-monorepo/tracks/core-track/lab-u01-container-access/resources/consolelab.yaml`.
Note in particular the terminal step, which uses its two sentences of "why" to teach a real
operational rule (a container is recreated from its image, so repairs made in a shell disappear)
rather than describing the button.
