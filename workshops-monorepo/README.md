# dcs-academy-workshops (monorepo + chart)

This repo **is** the DCS Academy catalog. The Helm chart at the root discovers
every workshop/track from the folder tree — there is no catalog list to edit.

```
<repo root>/            <- chart lives here (Chart.yaml, templates/, values.yaml)
  tracks/
    core-track/         <- a TRACK folder (name is free; the id is in track.yaml)
      track.yaml        <- track metadata incl. explicit `id` → one Track CR
      lab-a05-what-is-dcs/
        resources/
          workshop.yaml <- a complete Educates Workshop CR (emitted verbatim)
        workshop/ …     <- lab content (built to an OCI files-image by CI; chart ignores it)
    advanced-track/
      track.yaml
      lab-b01-…/
        resources/workshop.yaml
```

## Adding or changing content — use the skills

Don't hand-write workshops. The DCS Academy is authored with three **Claude Code
skills** that encode every house standard (OpenShift `oc`, air-gapped Harbor images,
the param trio, examiner checks, split terminal, the README/overview/feedback
contracts, …). **The skills live in a separate repo** (`airbus-educates-*-skill`) and
are installed into Claude Code — they are not part of this catalog repo.

| I want to… | Invoke the skill | It produces |
|---|---|---|
| Create or edit a single workshop | **airbus-educates-workshop-authoring** | a complete workshop folder — `resources/workshop.yaml` (CR + catalog metadata), `workshop/content/*.md`, `README.md`, `exercises/` |
| Plan a multi-workshop course / module | **airbus-educates-course-design** | a course brief, topic/module map, and per-workshop plans |
| Review / QA a workshop or course | **airbus-educates-course-review** | a findings + suggestions report against the house standards (advises, doesn't rewrite) |

Typical flow for a new lab:

1. **Design** (if it's a new course/module) — run *course-design* to get the plan and
   per-workshop briefs.
2. **Author** — run *workshop-authoring* against a brief. It writes the folder under
   `tracks/<track-folder>/<lab-name>/` following the layout below, filling in the
   `academy.dcs/*` catalog metadata the chart needs.
3. **Review** — run *course-review* and apply its findings.
4. **Test** — deploy portal-less to a local CRC cluster and run the examiner
   smoke test (see `crc-local-testing/` in the skills/tooling repo).
5. **Push** — merging to `main` deploys via ArgoCD (see deploy order below).

The "Add a track" and "Add a workshop" sections further down document the *mechanical*
contract the skill output must satisfy — read them to review or hand-fix generated
files, but let the skill generate the first draft.

> ## ⚠️ DEPLOY ORDER — READ THIS ⚠️
>
> This chart is **downstream of the `dcs-academy-portal` chart**. It must sync
> **after** it. The dependency:
>
> 1. **Track CRD** (`tracks.academy.dcs`) is owned by the **portal chart**, not
>    this one. If this chart syncs first, the Track CRs have no CRD → sync fails.
> 2. The **portal app Service** is the target of the TrainingPortal's analytics
>    webhook. It must exist first or analytics events 404.
> 3. The **Educates `Workshop`/`TrainingPortal` CRDs** (platform chart) must exist.
>
> **Enforcement:**
> - **Cross-app**: the app-of-apps orders the portal app (and platform) before
>   this workshops app. Keep it that way.
> - **In-app**: the TrainingPortal CR carries **`argocd.argoproj.io/sync-wave: "100"`**
>   so it settles dead last — after the Workshop CRs it names and after the CRD.
>   `SkipDryRunOnMissingResource=true` covers the first-ever apply.
>
> If you ever see the workshops app sync before the portal, the fix is app-of-apps
> ordering, **not** a bigger wave — sync-waves only order resources *within one
> Application*.

## What the chart emits

| Template | Source (globbed) | Output |
|---|---|---|
| `templates/tracks.yaml` | `tracks/*/track.yaml` | one **Track** CR per track folder (name = its `id`) |
| `templates/workshops.yaml` | `tracks/*/*/resources/workshop.yaml` | each **Workshop** CR **verbatim** |
| `templates/trainingportal.yaml` | `tracks/*/*/resources/workshop.yaml` (re-parsed for names) | one **TrainingPortal** listing all (wave 100) |

The Track **CRD** itself is shipped by the `dcs-academy-portal` chart. This chart
only fills it with instances. One ArgoCD Application points at this repo (prune +
selfHeal). Add a lab = add a folder with a `workshop.yaml` + push. Remove = delete
the folder + push.

## Add a track

`tracks/<any-folder>/track.yaml`:
```yaml
id: core                          # required — the track id (NOT the folder name)
title: "Core — DCS Foundations"   # required
description: "…"                  # optional
order: 10                         # optional (default 100; low = first)
icon: code                        # optional (default "layers")
```

## Add a workshop

Drop a full Educates Workshop CR at `tracks/<track-folder>/<lab>/resources/workshop.yaml`
(Educates requires the CR under `resources/`). The chart emits it **unchanged**, so
it must carry the portal metadata itself:

**Required labels** (portal catalog grouping):
- `academy.dcs/track: <track-id>` — must equal a track's `id`
- `academy.dcs/order: "10"` — sort within the track (string)

**Optional annotations** (display + session lifetime; all have fallbacks):
- `academy.dcs/summary`, `academy.dcs/duration`, `academy.dcs/difficulty`,
  `academy.dcs/icon`, `academy.dcs/display-name`, `academy.dcs/author`,
  `academy.dcs/details`
- `academy.dcs/expires`, `academy.dcs/orphaned` — per-workshop session lifetime
  in the TrainingPortal (else `values.portal.{expires,orphaned}`)

**Recommended annotations** (GitOps):
- `argocd.argoproj.io/sync-wave: "5"` and
  `argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true` — so ArgoCD
  can apply the CR before the Educates Workshop CRD is dry-run-checked. Keep the
  workshop wave well **below** the TrainingPortal's 100.

See `tracks/core-track/lab-a05-what-is-dcs/resources/workshop.yaml` for a filled, commented example.

## vcluster note (the one duplication cost)

Because workshops are emitted verbatim, per-session boilerplate lives in each
lab's file — including the vcluster SCC workaround (coredns needs the
`educates-privileged-scc` in `$(vcluster_namespace)`, or the vcluster hangs).
For a vcluster lab, author it in that file's `spec.session`:
```yaml
    applications:
      vcluster:
        enabled: true
    objects:
      - apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata: { name: educates-vcluster-scc, namespace: $(vcluster_namespace) }
        roleRef: { apiGroup: rbac.authorization.k8s.io, kind: ClusterRole, name: educates-privileged-scc }
        subjects:
          - kind: Group
            apiGroup: rbac.authorization.k8s.io
            name: system:serviceaccounts:$(vcluster_namespace)
```
If this repeats too much, switch `templates/workshops.yaml` from verbatim to
`fromYaml` + merge so the chart injects it — costs central logic, buys DRY.

## Ownership split (two charts)

| Chart | Owns |
|---|---|
| `dcs-academy-portal` | portal app, oauth gate, CNPG/feedback, **Track CRD** |
| `dcs-academy-workshops` (this) | **Track CRs, Workshop CRs, TrainingPortal** |

Keep these in sync between the two: `educates.portalName` and the academy
`hostname` (`portal.hostname` here == `auth.hostname` in the portal chart).

## Render locally
```bash
helm template dcs-workshops .
```
