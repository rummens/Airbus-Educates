# Workshop Plan: lab-b02-image-buildconfigs

## 1. Workshop Metadata

- **Name:** `lab-b02-image-buildconfigs`
- **Title:** Building Images with BuildConfigs
- **Description:** Get *your* code into an image without a local Docker — point a BuildConfig at a git repo, build the image on-cluster (S2I or Dockerfile), push it to Harbor, deploy it, and trigger a rebuild on change.
- **Duration:** 45m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B01 (From Docker to Kubernetes on DCS)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split` (watch the build in one pane, run commands in the other)
- Editor: enabled (view the BuildConfig / app source)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (Builds view, ImageStreams)
- Examiner: `enabled: true`
- Budget: `medium` (a build Pod plus the deployed app — mind quota)
- **vcluster decision:** `false` — native OpenShift session namespace. BuildConfig/Build/ImageStream are all namespaced; no cluster-scoped objects needed.
- Workshop image: `dcs-workshop-base`
- **Git build source:** a small provided git repo (mirrored/reachable in-cluster) containing the app source + a Dockerfile; the learner may substitute their own repo where the platform allows. **No external git** — the repo is reachable air-gapped (see Design Notes).
- **Build output:** an image pushed to `{{< param dcs_registry >}}` (Harbor) via a push-capable robot account / pipeline secret provisioned to the session.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain how DCS builds images *on the cluster* (BuildConfig + Build Pod) instead of on a laptop.
- Connect a git repo as a **build source** and choose a strategy (S2I vs Dockerfile).
- Build an image and watch it push to Harbor (`{{< param dcs_registry >}}`).
- Deploy the built image with the Core A02 skills.
- Trigger a rebuild when the source changes.

## 4. Connection to Previous Workshop

**Already known (from B01 + Core):** Deployment/Service/ConfigMap and `oc apply` (A02, reinforced in B01); the Harbor-only / non-root / no-`latest` constraints (B01); the sample app.

**New here:** the *build* step — BuildConfig as git-as-a-build-source, S2I and Dockerfile strategies, ImageStream, on-cluster build Pods, and pushing a *built* image into Harbor (B01 only migrated an image someone else built).

**Do NOT re-teach:** how to write/apply a Deployment or reach a Service (A02/B01) — reuse them to deploy the built image; the Harbor constraints (B01) — reference as established.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder + note on the provided git repo URL (param/placeholder).
- `exercises/buildconfig-s2i.yaml` — a BuildConfig, **S2I strategy**: `source.git.uri` = the provided repo, `strategy.sourceStrategy` referencing a Harbor-mirrored S2I builder image via `${DCS_REGISTRY}`, `output.to` an ImageStreamTag.
- `exercises/buildconfig-dockerfile.yaml` — a BuildConfig, **Dockerfile strategy** (same git source, `strategy.dockerStrategy`), output to Harbor. Learner picks one strategy; the other is read as contrast.
- `exercises/imagestream.yaml` — the ImageStream the build outputs to.
- `exercises/deployment.yaml` — Deployment referencing the **built** image (`${DCS_REGISTRY}/<project>/<app>:latest-built` by digest/tag) — deployed with the A02 skills.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note. Frame: "How do I get *my* code into an image without a local Docker?" Objectives; open `buildconfig-s2i.yaml` (`editor:open-file`).
- **`01-builds-on-dcs.md`** — concept. No laptop Docker on an air-gapped platform → the cluster builds for you. BuildConfig → Build Pod → image → Harbor. S2I (source + builder image, no Dockerfile) vs Dockerfile strategy. BuildConfig/S2I → upstream ([Builds](https://docs.openshift.com/container-platform/latest/cicd/builds/understanding-image-builds.html)); air-gapped builder images + Harbor output → `{{< param dcs_docs_base_url >}}/services/registry` + blurb. No command → no examiner.
- **`02-buildconfig-from-git.md`** — read the BuildConfig: `editor:open-file`, `editor:select-matching-text` the git `source`, the `strategy`, the Harbor `output.to`. Emphasise the builder image comes from Harbor via `${DCS_REGISTRY}`. Apply: `envsubst < buildconfig-s2i.yaml | oc apply -f -` (+ `imagestream.yaml`). Check: BuildConfig + ImageStream exist.
- **`03-run-the-build.md`** — `oc start-build <bc> --follow` (split terminal: build log in one pane). Watch it push to Harbor. `oc get builds`; `oc get istag`. Checks (polling): build phase `Complete`; ImageStreamTag populated (image landed in Harbor).
- **`04-deploy-the-built-image.md`** — deploy the built image with A02 skills: `envsubst < deployment.yaml | oc apply -f -`; confirm the app runs *from the image you built*. Checks: 1 ready replica; app responds 200.
- **`05-rebuild-on-change.md`** — change the source (a greeting string) — narrate/trigger a rebuild (`oc start-build`; note webhook/ImageChange triggers as the automated path), redeploy, see the change. Concept: build triggers (webhook/config/image-change). Examiner: a second successful build (phase `Complete`).
- **`99-workshop-summary.md`** — recap BuildConfig / S2I vs Dockerfile / ImageStream / build-to-Harbor / rebuild. **Check Your Understanding** (3–4 Q). **Contrast explicitly with B03:** "B02 connected git as a **build source** (code → image in Harbor); next, B03 connects git as an **in-cluster IDE** (Dev Spaces) — same git, different purpose." Bridge to **B04** (where your built image lives + gets scanned).

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`; split pane used for `oc start-build --follow`. Manifests by relative name. No `cd`.
- **Carry-forward bug:** every `${DCS_REGISTRY}` manifest applied via `envsubst < file.yaml | oc apply -f -`, never plain `oc apply`.

## 8. Design Notes

- Covers **course-topics idea 7c** (building images with BuildConfigs). First of the two "connect my git" labs — **git as a build source** (B03 = git as an in-cluster IDE); sequenced adjacently on purpose.
- **Air-gapped build source (open question → validate):** the git repo and the S2I builder image must be reachable in-session without external egress. Options: a repo mirrored into the tenant's GitLab (Module F territory) or a small in-cluster git service seeded for the session; builder image mirrored to Harbor. Spike feasibility in `tasks.md`.
- **Push capability:** unlike A04/B04's read-only robot, this lab needs a **push-capable** credential to a session-scoped Harbor project. Provisioning this per session is the main setup cost — flag in `tasks.md`; fallback is a pre-created project + scoped robot secret mounted to the session.
- **Strategy choice:** teach S2I as the DCS-default "no Dockerfile needed" path; show the Dockerfile strategy as the escape hatch for teams that already have one. Don't drown the learner — pick one to run, read the other.
- Produces the artifact **B04** consumes: the image built here is the one the learner pushes/inspects/scans in Harbor next.
