# DCS Academy — Console Tour Authoring Skill

A Claude Code skill for creating **console labs**: guided tours of the OpenShift web console,
run by the academy console plugin from `ConsoleLab` custom resources. Skill name:
`airbus-educates-console-tour-authoring`.

This is the third authoring surface of the DCS Academy, alongside
`airbus-educates-workshop-authoring` (terminal labs) and `airbus-educates-course-design`
(course planning).

## What it covers

- Choosing between a **default** tour (listed in the console for anyone) and a **hidden** lab
  (launched by the academy portal into a provisioned namespace)
- The `ConsoleLab` contract: steps, targets, operations, verifications, launch parameters
- Pairing a hidden lab with an Educates Workshop that pre-deploys its environment
- Portal catalog metadata — a console lab has no README, so the course page is annotations
- The house voice for step text, and the pedagogical rule that makes the format work

## The rule that shapes everything

Concepts are taught in the **terminal labs**. A console lab only **applies** them: it shows where
the thing the learner already understands lives in the graphical console, and what its CLI
equivalent was. A step that teaches a Kubernetes concept for the first time belongs in a terminal
lab; a step that says "click here" and nothing more is not worth a step.

## Layout

| File | Contents |
|---|---|
| [SKILL.md](SKILL.md) | House standards, the create/review workflows |
| [references/consolelab-crd-reference.md](references/consolelab-crd-reference.md) | Full CR contract and the placement rules that strand learners |
| [references/step-writing-reference.md](references/step-writing-reference.md) | Voice, depth, worked before/after examples |
| [references/portal-launch-reference.md](references/portal-launch-reference.md) | Workshop pairing, session objects, RBAC, lifecycle |
| [references/portal-metadata-reference.md](references/portal-metadata-reference.md) | Catalog tile and course page copy |
| [references/testing-reference.md](references/testing-reference.md) | Verifying a lab on CRC before shipping |

Reference implementation:
`workshops-monorepo/tracks/core-track/lab-u01-container-access/`.
