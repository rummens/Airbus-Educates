# Airbus-Educates — repo guide

This repo delivers the **DCS Academy**: interactive [Educates](https://educates.dev/)
training for the **Digital Container Service (DCS)** — Airbus Defence and Space's on-prem,
air-gapped, multi-national (Europe), OpenShift-based container platform. It holds both the
**platform deployment** (Helm/ArgoCD) and the **course** (authoring skills + workshops).

Rich background lives in auto-memory (loaded each session). Read those first —
especially **dcs-academy-course-design**, **dcs-domain-corrections**, and
**crc-workshop-testing**. This file is the map.

## Layout

| Path | What |
|---|---|
| `airbus-educates-workshop-authoring-skill/` | Skill: create/author Educates workshops (OpenShift house standards). Fork of upstream. |
| `airbus-educates-course-design-skill/` | Skill: plan multi-workshop courses. |
| `airbus-educates-course-review-skill/` | Skill: review/QA a workshop or course against all house standards; reports findings + suggestions (advises, doesn't rewrite). |
| `dcs-academy/` | The course: `planning/` (brief, topics, module maps, per-workshop plans) + `workshops/` (built workshops: A01, A02 done; A03–A06 planned). See `dcs-academy/CLAUDE.md`. |
| `images/` | `dcs-workshop-base` (Educates base + oc) and `hello-dcs` (RH UBI9) Containerfiles + `build.sh`. Pushed to `ghcr.io/rummens/*` (public, multiarch). |
| `crc-local-testing/` | Portal-less deploy + smoke-test to the local CRC cluster: `deploy_workshop.py`, `smoke_test.py`, `smoke-plans/`, README. |
| `docs/dcs-academy/` | Learner-facing environment guide (linked from workshop overviews). |
| `argocd/`, `dcs-academy-{platform,workshops,kapp-controller}/` | Platform install via ArgoCD app-of-apps (syncs from GitHub `main`; prune+selfHeal). |

## Which skill to use

- Authoring/editing a workshop → **airbus-educates-workshop-authoring**.
- Planning a course / module / per-workshop plans → **airbus-educates-course-design**.
- Reviewing/QAing an existing workshop or course → **airbus-educates-course-review**.

The workshop authoring skill's `references/` are the authoritative source for the house
standards; the review skill's rubric consolidates them.

## Non-negotiable house standards (workshops)

OpenShift `oc` (never `kubectl`) · air-gapped: every image from Harbor
(`$(image_repository)` / `{{< param dcs_registry >}}`), no external registries · variablize
everything, param trio `product_name`/`dcs_registry`/`dcs_docs_base_url` · `workshop/config.yaml`
`params` is a **list of {name,value}** (a map breaks the ytt setup step) · mandatory
`00-workshop-overview.md` with the first-time note · hybrid doc links (upstream for standard
constructs, `dcs_docs_base_url` for DCS concepts) · teach concepts not commands (one/page,
what/why/how, expected output, **VM-world analogies tapering with level**, **SVG diagrams**,
realistic err-low duration) · an **examiner check for every command** + knowledge check ·
split terminal = **upper/lower** (`execute-1`/`-2`) · decide **vcluster (default) vs OpenShift
namespace** and record why.

## Before implementing A03–A06

Apply the author's corrections in **dcs-domain-corrections** memory — they override the
plans: no "project" layer (Tenant→Namespaces); Harbor **pull-only** + **skopeo, not
docker/podman**; PROD ns enforce Kyverno (DEV don't); Route needs a PROD ns; NetworkPolicy
isn't self-service yet (teach as observe).

## Testing a workshop (local CRC OpenShift, arm64)

```bash
cd crc-local-testing
./deploy_workshop.py lab-a02-kubernetes-essentials      # portal-less, git source
./smoke_test.py     lab-a02-kubernetes-essentials       # examiner checks + link check + restart
```
The CRC git-source reads `origin/main`, so **push content changes before re-deploying**.
Portal is broken on CRC arm64 (SIGILL) — always portal-less. Editor/console tabs need the
CRC self-signed cert trusted (see crc-local-testing/README).

## Deploy / git

Platform changes sync to the cluster via ArgoCD on push to `main` (prune+selfHeal) — the
skills/course/images dirs are authoring assets, not Argo apps. Commit when the user asks;
don't push without asking (push is the deploy trigger for platform paths).
Commit trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
