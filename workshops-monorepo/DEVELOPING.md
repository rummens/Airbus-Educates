# dcs-academy-workshops — developer guide

Everything about the **Helm chart**, the deploy order and the authoring contract for this
catalog. If you only want to find your way around the labs, read [README.md](README.md)
instead.

The chart at the repo root discovers every workshop/track from the folder tree — there is
no catalog list to edit.

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

## Adding or changing content — follow the house standards

Don't improvise a workshop. Every lab in the academy follows one fixed house standard:
OpenShift `oc` (never `kubectl`), air-gapped images from Harbor, the param trio
(`product_name` / `dcs_registry` / `dcs_docs_base_url`), an examiner check for every
command, the split terminal, and the README / overview / feedback page contracts.

Those standards and the authoring guides that encode them live in **separate repos**
(`airbus-educates-*-skill`) — they are not part of this catalog repo:

| I want to… | Authoring guide | It defines |
|---|---|---|
| Create or edit a single workshop | **airbus-educates-workshop-authoring** | the complete workshop folder — `resources/workshop.yaml` (CR + catalog metadata), `workshop/content/*.md`, `README.md`, `exercises/` |
| Plan a multi-workshop course / module | **airbus-educates-course-design** | the course brief, topic/module map, and per-workshop plans |
| Review / QA a workshop or course | **airbus-educates-course-review** | the review rubric — findings + suggestions against the house standards |

Typical flow for a new lab:

1. **Design** (if it's a new course/module) — write the plan and the per-workshop brief.
2. **Author** — build the folder under `tracks/<track-folder>/<lab-name>/` following the
   layout above, filling in the `academy.dcs/*` catalog metadata the chart needs.
3. **Review** — check it against the rubric and apply the findings.
4. **Test** — deploy portal-less to a cluster with oc logged in and run the examiner smoke test
    (see the testing tooling in the platform repo).
5. **Push** — merging to `main` deploys via ArgoCD (see deploy order below).

The "Add a track" and "Add a workshop" sections below document the *mechanical* contract
any new lab must satisfy — read them to review or hand-fix a lab folder.

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

## PostSync hooks (rescan, memory-limit, env-guard)

The chart emits ArgoCD **PostSync** hook Jobs that run after each sync:

| Hook (`templates/…`) | sync-wave | Does |
|---|---|---|
| `memory-limit-job.yaml` | 0 | patches the operator-owned `training-portal` Deployment to 512Mi |
| `catalog-rescan-job.yaml` | 0 | `POST /admin/rescan` so the custom portal refreshes its catalog now, not after TTL |
| `env-guard.yaml` → `env-reconcile` | 1 | `portal.reap` — drains stale/duplicate WorkshopEnvironments (+ orphan sessions) |
| `env-guard.yaml` → `env-validate` | 2 | `portal.validate` — **gate**: fails the sync if any catalog workshop has no Running env |

### Why env-guard exists

The Educates CR chain: **Workshop** + **TrainingPortal** (both synced by Argo) → the
training-portal pod creates a **WorkshopEnvironment** per catalog workshop → a
**WorkshopSession** per learner. The portal reconciles environments by **create/delete
only — never an in-place update**, so when a workshop rolls (new content image, edited
spec) the old env can linger while the new one never appears. A `start` then has no
environment to allocate → **403**. And because WorkshopEnvironment/WorkshopSession are
portal-created, they're **invisible to Argo's health** — the app stays "Synced + Healthy"
while a lab is broken.

env-guard closes both gaps:
- **reconcile** deletes the stale/duplicate env (drain-safe: only envs with 0 Allocated
  sessions, past grace, scoped to this portal + the current catalog) → the portal rebuilds
  it on its working create path, on *every* sync.
- **validate** polls until every `TrainingPortal.spec.workshops` entry has a Running env;
  if not, exits non-zero → the hook fails → Argo goes **Degraded** and retries. Set
  `envGuard.mode: warn` to log-only. Ready = phase `Running` **or** already backing a live
  session (avoids a false fail on an unrecognised phase string).

Steady-state cleanup **between** syncs is the `dcs-academy-portal` chart's
`sessionReaper` CronJob (`reapEnvironments: true` — same `portal.reap` logic, every
15 min). Argo can't see envs, but it *can* see the TrainingPortal: apply
[`argocd/trainingportal-health.yaml`](../argocd/trainingportal-health.yaml) (cluster-admin,
one-off) so the portal's own rollout reports Healthy only when Running.

> **Toggles** (`values.yaml → envGuard`): `enabled`, `mode` (fail|warn), `dryRun`,
> `settleSeconds`, `readyPhases`. First rollout: run `dryRun: true` + `mode: warn`, confirm
> the reconcile logs target only real stale/orphan envs, then flip to act. The Jobs run
> from the **portal image** (`envGuard.image`) — rebuild+push it before syncing chart
> changes that touch `portal.reap`/`portal.validate`.

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

## Console labs (`lab-format: console`)

Two lab formats share this catalog:

| Format | Learner works in | Content |
|---|---|---|
| `terminal` (default) | the Educates dashboard — instructions, terminal, editor | `workshop/content/**` |
| `console` | the OpenShift web console, guided by the academy console plugin | none — a `ConsoleLab` CR |

A console lab still allocates a normal Educates session: the session namespace, its
quota, `spec.session.objects`, capacity and the reaper are all unchanged. Only the
final redirect differs — the portal sends the browser to the console instead of the
workshop dashboard, and the learner never opens the dashboard at all.

Mark one with:

```yaml
metadata:
  labels:
    academy.dcs/lab-format: console
  annotations:
    academy.dcs/console-lab: lab-container-access      # ConsoleLab CR name
    academy.dcs/console-lab-params: podName=lab-app    # everything except ns
    academy.dcs/orphaned: "0s"                         # see below
```

Rules that are easy to get wrong:

- **`orphaned: "0s"` is required.** Orphan detection watches the workshop dashboard,
  which a console-lab learner never opens — leave the default and Educates reclaims
  the session out from under them mid-lab. `expires` remains the real bound. The CRD
  pattern is `^\d+(s|m|h)$`, so the value needs its unit: `"0s"`, never `"0"`.
- **`ns` is never declared.** The portal injects the allocated session namespace.
  `console-lab-params` fills the lab's other `{{placeholders}}`.
- **Pre-deploy with `spec.session.objects`.** The learner is dropped into a ready
  environment; they do not build it by following instructions. Objects are created
  with the session and deleted with it.
- **Name pods explicitly.** A ConsoleLab navigates to exact paths like
  `/k8s/ns/<ns>/pods/lab-app`, so use a bare Pod (or a fixed-name resource) — a
  Deployment's generated pod suffix cannot be templated into the lab.
- **Label lab pods** `training.educates.dev/session.name: $(session_name)` so the
  portal's readiness feed waits for them before redirecting.
- **Real images.** Unlike an image merely *named* in content, an image in
  `session.objects` is actually pulled — take it from `values.workshopImages.*` so
  air-gapped installs repoint it once.

The referenced `ConsoleLab` CR (the step-by-step guidance) lives in the **console
plugin repo** (`labs/`), not here. Both must be synced for the lab to run; the
plugin refuses to start a lab whose parameters are missing rather than half-running.

Example: `tracks/console-track/lab-u01-container-access/resources/workshop.yaml`.

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

## CI pipeline overview

The repo's `.gitlab-ci.yml` defines **two stages**, `test` and `e2e`, and uses
per-job `rules: changes:` plus dynamic child pipelines to keep runs fast:

- **Fast tier (`test`)** — no cluster, blocks merges, all start immediately (`needs: []`):
  - `portal-tests` — portal pytest/coverage (fires when `images/dcs-academy-portal`,
    `test/portal`, `test/ci`, or `.gitlab-ci.yml` change).
  - `workshop-static` — link/coverage/label checks via `test/ci/run-workshops.sh` (fires on
    `tracks/**`, `test/workshops/**`, `test/ci/**`, `.gitlab-ci.yml`). This is the job that
    drives `curl --proxy-ntlm` through `link_check.py` when `HTTPS_PROXY` is set.
  - `fix-examiner-perms` — on pushes, re-asserts `+x` on examiner test scripts and pushes a
    `[skip ci]` fix commit.
  - `generate-image-spec` — (see image-builder below; the fragment is imported from the
    `pipeline-library` repo) decides which images changed and emits one `build-<img>` job
    per image into a child spec.
  - `generate-smoke-spec` — decides which labs changed and emits one `<lab>` smoke job per lab
    into a child spec (all labs on `schedule`, or when `SMOKE_ALL=true`).
  - `generate-smoke-spec-all` / `cluster-smoke-manual` — an optional **manual** full-tracks
    smoke (all labs, `--all`), non-blocking outside MRs.
- **e2e tier (`e2e`)** — cluster/OpenShift work, on `$CI_BASE_IMAGE` and logged in via the
  `CI_OC_*` vars (no dedicated runner tag):
  - `build-images` — triggers the generated image-build child pipeline (`strategy: depend`).
  - `run-workshops-smoke` — triggers the generated smoke child pipeline.
  - `user-flow` — `flow_test.py --mode both`.
  - `cleanup-orphans` — (image-builder) deletes BuildConfigs/tags whose branch no longer exists.

### Image builds (BuildConfig per image)

Container-image builds are driven by the **image-builder component from the `pipeline-library`
repo** (self-contained: `build.sh`, a `gitlab-ci.yml` fragment, a child-spec generator, and
deploy manifests). This repo only keeps the images themselves under `images/`. Each pipeline,
the imported fragment clones `pipeline-library` (so its jobs can run `build.sh` /
`gen-image-child.py` / `version.sh`) and runs them against this repo's checkout as the working
directory. `generate-image-spec` writes a child pipeline with one parallel job per changed/eligible
image; `build-images` runs it. On the default branch (or git-tag pipelines) images are tagged
`v<semver>` — computed from conventional commits by `version.sh` — plus `latest` and the branch
name; on feature/MR branches they keep a branch-name tag. Details live in that component's
`README.md` in the pipeline-library repo.

### Workshop smoke (dynamic per-lab jobs)

`generate-smoke-spec`'s child jobs each run `smoke_test.py <lab> --no-links --ref <branch>
--throwaway` (deploy → run graders → tear down) in a portal-hidden throwaway Workshop. They use
`$CI_BASE_IMAGE` and login via `CI_OC_*`; no runner tag is needed. `SMOKE_ALL=true` (CI var)
forces the full suite on every pipeline instead of only changed labs / schedule.

## GitLab CI — intended variables

The pipeline needs a set of CI/CD variables to run the way it's written. Set them
in **Settings → CI/CD → Variables** at the project (or group) level. Mark secrets
**Masked** so they never appear in job logs, and **Protected** if you only want them on
protected branches (`main`). Several (`BUILD_ALL`, `SMOKE_ALL`, `IMAGE_VERSION`, …) are
opt-in tuning knobs the pipeline reads from the environment — set them only when you want
that behaviour.

| Variable | Example | Secret? | Where it's used |
|---|---|---|---|
| `CI_BASE_IMAGE` | `ghcr.io/rummens/dcs-ci:dev` | no | Image for every fast-cluster/fast-tier job; defaulted in `.gitlab-ci.yml` (`variables:`). Carries `python`, `git`, `curl`, `oc`, `jq`, `skopeo`. Point it at your Harbor mirror on an air-gapped runner. |
| `REGISTRY_BASE` | `registry.../dcs-internal-images` | no | Image-build push base. Has **no** YAML default (a YAML default would override the CI var); required for image builds. Used by `build.sh`, the image-builder generator, and the registry SealedSecret. |
| `REGISTRY_SERVER` / `REGISTRY_USER` / `REGISTRY_PASS` | registry host / robot user / token | user+pass yes | Registry login. `REGISTRY_USER`+`REGISTRY_PASS` back the out-of-cluster `skopeo` verify/cleanup and the push secret; the robot needs push+pull on the target project. |
| `GIT_USER` / `GIT_TOKEN` | git user / deploy token | token yes | In-cluster git clone for BuildConfig source (`git-source` basic-auth secret). `GIT_TOKEN` must be durable, not `CI_JOB_TOKEN`. Only needed if the `git-source` secret isn't pre-provisioned. |
| `CI_OC_HOST` / `CI_OC_TOKEN` | API URL / token | token yes | OpenShift login for every cluster/e2e job (and the child image/smoke jobs). |
| `CI_OC_INSECURE` | `true` | no | Set to skip TLS verification on `oc login` (dev clusters with an untrusted CA). |
| `CA_BUNDLE` / `CI_OC_CONTEXT` / `CI_OC_USERNAME` | — | no | Optional overrides. `CA_BUNDLE` (old alias `CI_OC_CA_BUNDLE`) is the internal-CA PEM file used by git (pipeline-library clone) and `oc login`; context/username are `oc login` overrides. |
| `HTTPS_PROXY` / `PROXY_USER` / `PROXY_PASSWORD` | proxy URL / user / pass | user+pass yes | Corp egress proxy for the link check (`curl --proxy-ntlm`). See "Proxy behaviour". |
| `LINK_CHECK_SKIP_EXTERNAL` | `true` | no | Air-gapped runner: count public links, don't fetch them. |
| `DCS_DOCS_BASE_URL` / `DCS_DOCS_CHECK_INTERNAL` | docs host / `true` | no | Real internal docs host for the link check (and whether to fetch internal links). |
| `GIT_PUSH_TOKEN` | scoped token | yes | Write-repo token for `fix-examiner-perms` to push its `chmod +x` fix. |
| `SMOKE_ALL` | `true` | no | Run the **full** smoke suite on every pipeline (instead of only changed labs / schedule). |
| `NO_PROXY` | hosts | no | Hosts the link check fetches directly (bypassing the proxy). |
| `IMAGE_*` / `BUILD_*` / `SCOPE_DIR` | — | no | Tuning knobs for image builds: `IMAGE_VERSION`/`IMAGE_TAGS` (release versioning), `IMAGE_BUILD_TIMEOUT`, `BUILD_ALL`, `SCOPE_DIR`, `BUILD_NAMESPACE`, `PUSH_SECRET`/`GIT_SECRET`, `SOURCE_GIT_URI`, `VERIFY_RETRIES`/`VERIFY_WAIT`. Documented in the image-builder component's `README.md` (pipeline-library repo).

### Proxy behaviour

Only the `workshop-static` job carries the proxy `before_script`. When `HTTPS_PROXY` is set
it exports the proxy vars and builds `NO_PROXY` to keep the internal docs host
(`docs.dcs.common.airbusds.corp`) plus `.corp`, `.svc`, and loopback addresses on a direct
connection — internal links must not go out through the NTLM proxy. `link_check.py` reads
those env vars and adds `-x`/`--proxy-ntlm`/`--noproxy` to each `curl` call, because curl's
automatic env-proxy only does Basic auth and would fail against the corp NTLM proxy.

If the runner has **no** proxy but still cannot reach the internet, leave `HTTPS_PROXY`
unset and set `LINK_CHECK_SKIP_EXTERNAL=true`: the link check counts public links and lists
them without fetching, and the proxy path is simply not used.

## Examiner Permission fix
Windows removes the execution permission from linux files. This causes examiner scripts to fail in the sessions.
To fix this, we can use this command: `git ls-files -z 'tracks/*/*/workshop/examiner/tests/*' | xargs -0 git update-index --chmod=+x`
