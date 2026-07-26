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
