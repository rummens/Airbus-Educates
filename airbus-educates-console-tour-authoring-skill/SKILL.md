---
name: airbus-educates-console-tour-authoring
description: >
  Create and edit DCS Academy CONSOLE LABS — guided tours of the OpenShift web console run by
  the academy console plugin from ConsoleLab custom resources, as opposed to the terminal-based
  Educates workshops. Covers the two lab kinds (default tours anyone can start from the console
  catalog, and hidden labs launched by the academy portal into a provisioned namespace), the
  ConsoleLab contract (targets, operations, verifications, launch parameters), pairing a hidden
  lab with an Educates Workshop that pre-deploys its resources, the portal catalog metadata, and
  the house voice for step text: apply concepts already taught in the terminal labs, never
  re-teach them, and never write a bare "click here". Use this skill when asked to create,
  edit, or review a console lab, console tour, guided console walkthrough, ConsoleLab CR, or a
  UI-based lab for the DCS Academy.
---

# DCS Academy — Console Tour Authoring

A **console lab** is a guided tour of the real OpenShift web console. The academy console plugin
reads a `ConsoleLab` custom resource, highlights the element the learner should look at, explains
it in a small box beside it, and advances when the console reaches the expected state.

This is a different medium from an Educates workshop, and it has a different job.

| | Terminal lab (`airbus-educates-workshop-authoring`) | Console lab (this skill) |
|---|---|---|
| Job | **Teach the concept.** What a Deployment is, why it exists, what breaks without it | **Apply it in the GUI.** Where that same Deployment lives on screen |
| Medium | Instruction pages, terminal, editor | Highlight + one short box on the live console |
| Content | `workshop/content/*.md`, examiner checks, slides | One `ConsoleLab` CR, ordered steps |
| Length | 20–60 minutes | 5–15 minutes |
| Prerequisite | The concepts it teaches | **A terminal lab that already taught them** |

**The pedagogical contract: concepts are taught in the terminal labs and only *applied* here.**
A console lab never introduces a Kubernetes concept for the first time. If a learner would meet
"what a PersistentVolumeClaim is" for the first time in your tour, the tour is wrong — either
point it at a later slot in the track or send the concept back to a terminal lab.

## House standards (every console lab)

1. **Pair with a terminal lab.** Name the prerequisite lab(s) in the description and refer back
   to them in the step text. State the CLI equivalent of each screen (`oc get pods`, `oc logs`).
2. **Explain the why, not the click.** Never ship a step whose text is "Click Deployments".
   Every step says what this screen is *for* and why a practitioner would come here. See
   [references/step-writing-reference.md](references/step-writing-reference.md).
3. **A real prospectus in the portal.** A console lab has no README, so
   `academy.dcs/details` (markdown, rendered on the course page) is its description. A single
   sentence is not enough — see [references/portal-metadata-reference.md](references/portal-metadata-reference.md).
4. **Plain language, DCS voice.** Same rules as the workshop skill: no idioms, no metaphors, no
   marketing tone. Short sentences. Define nothing that a prerequisite lab already defined.
5. **Naming.** Folder name, `ConsoleLab` `metadata.name`, and the paired Workshop name are
   identical. Default tours are `tour-<subject>`; portal-launched labs are `lab-u<NN>-<subject>`
   (`u` for the console/UI series, numbered in delivery order).
6. **Every step must be reachable.** A target that does not exist on the current page stalls an
   assisted learner. Verify placement rules in
   [references/consolelab-crd-reference.md](references/consolelab-crd-reference.md).
7. **Parameters use `<<name>>`.** Lab files are rendered by Helm at deploy time, so `{{ }}` and
   `$( )` are already taken. `ns` is always supplied by the portal; never declare it.
8. **Test on a cluster before you ship.** A console lab is coupled to console markup; reviewing
   the YAML is not evidence that it runs. See
   [references/testing-reference.md](references/testing-reference.md).

## Decide the kind first

Ask one question: **does the learner need resources that must be created for them?**

- **No — the lab teaches the console itself** (navigation, where resource types live, how the
  project selector works) → a **default** lab. `spec.visibility: default`, listed in the console's
  own catalog, startable by anyone at any time. It must work for a learner with only their own
  project: either use no namespaced paths at all, or template `<<namespace>>`, which falls back
  to the project the console is currently scoped to.
- **Yes — the lab inspects a running pod, a failing deployment, two projects side by side** →
  a **hidden** lab. `spec.visibility: hidden`, never listed, launched only from the academy
  portal with the parameters it needs. It is paired with an Educates Workshop whose
  `spec.session.objects` create that environment. See
  [references/portal-launch-reference.md](references/portal-launch-reference.md).

`hidden` is not a security control — lab text is not secret, and the real boundary is namespace
RBAC. It means "this lab is meaningless without an environment somebody provisioned".

## Creating a console lab

### 1. Gather

- Which **terminal lab(s)** teach the concepts this tour applies. Read them; reuse their
  vocabulary and reference them by title.
- The **console journey**: the exact pages, in order, a practitioner would visit.
- For a hidden lab: the **resources** the learner needs, and the **parameters** beyond `ns`.

### 2. Write the ConsoleLab CR

Location: `workshops-monorepo/tracks/<track>/<lab-name>/resources/consolelab.yaml`.
Field-by-field contract, targets, operations and verifications:
[references/consolelab-crd-reference.md](references/consolelab-crd-reference.md).

Keep tours to **4–8 steps**. A longer journey is two tours.

### 3. Pair it with a Workshop (hidden labs only)

`workshops-monorepo/tracks/<track>/<lab-name>/resources/workshop.yaml` with
`academy.dcs/lab-format: console`, the `console-lab` annotations, `academy.dcs/orphaned: "0s"`,
and the `session.objects` that build the environment.
Full recipe and the traps: [references/portal-launch-reference.md](references/portal-launch-reference.md).

### 4. Write the portal metadata

`academy.dcs/summary`, `academy.dcs/details` (markdown), duration, difficulty, icon `monitor`.
[references/portal-metadata-reference.md](references/portal-metadata-reference.md).

### 5. Test it on CRC

Apply the CR, run the tour end to end as a learner, and confirm every step advances **without**
pressing Continue. [references/testing-reference.md](references/testing-reference.md).

### 6. Ship

`git push`. The workshops chart globs `tracks/*/*/resources/consolelab.yaml` and ArgoCD applies
it. No image is rebuilt for a content change.

## Reviewing an existing console lab

Check, in this order:

1. Does any step teach a concept instead of applying one? → move it to a terminal lab.
2. Does any step text amount to "click this"? → rewrite with the reason and the CLI equivalent.
3. Is the portal description one thin sentence? → write the `details` prospectus.
4. Does every target exist on the page the previous step leaves the learner on?
5. Do all `<<parameters>>` come from the portal, and is `ns` absent from `console-lab-params`?
6. Does it run start to finish on a cluster without using Continue as a crutch?

## References

| File | Read it when |
|---|---|
| [references/consolelab-crd-reference.md](references/consolelab-crd-reference.md) | Writing or debugging steps, targets, operations, verifications |
| [references/step-writing-reference.md](references/step-writing-reference.md) | Writing the prose in a step (voice, depth, worked before/after) |
| [references/portal-launch-reference.md](references/portal-launch-reference.md) | Building a hidden lab: Workshop pairing, session objects, RBAC, lifecycle |
| [references/portal-metadata-reference.md](references/portal-metadata-reference.md) | Catalog tile and course page copy |
| [references/testing-reference.md](references/testing-reference.md) | Verifying a lab on CRC before shipping |
