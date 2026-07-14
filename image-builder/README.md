# image-builder

Trigger container builds for a **monorepo** on an OpenShift cluster. Each top-level
folder that changed is built via its own `BuildConfig` and pushed to an external
registry (Harbor/Quay). Replaces building images by hand.

- `build.sh` — the whole thing (`build` | `cleanup` | `selftest`).
- `gitlab-ci.yml` — pipeline wiring (`include:` it from repo-root `.gitlab-ci.yml`).
- `build_config.example.json` — per-folder overrides (all optional).

## How it works

1. **Change detection** — `git diff` of the current push (`$CI_COMMIT_BEFORE_SHA..HEAD`),
   or the MR diff vs the target branch. New branches with no before-SHA diff vs the
   default branch. Only the changed top-level folders are considered.
   (`BUILD_ALL=true` builds every folder.)
2. **Eligibility** — a folder builds only if it has a `Dockerfile`, `Containerfile`,
   or `build_config.json`.
3. **BuildConfig per (folder, branch)** — named `<folder>--<branch>` (sanitized).
   Separate branches build in parallel without clobbering each other's output tag,
   because the output tag lives in the BC spec (OpenShift can't retarget it at
   `start-build` time). `oc apply` creates it, or updates it in place if the spec
   changed. Then `oc start-build --follow`.
4. **Output** — `DockerImage` `$REGISTRY_BASE/<folder>:<branch>` by default. `tag`
   defaults to the branch name.
5. **Cleanup** — `build.sh cleanup` reconciles: for every BC whose branch label no
   longer matches a live remote branch (i.e. the source branch was deleted after
   merge), it deletes both the registry tag (`skopeo delete`) and the BC. The default
   branch is never cleaned. `build.sh cleanup <branch>` targets one branch explicitly.

## Per-folder `build_config.json`

Drop it in a folder to override defaults. Everything is optional — see
[`build_config.example.json`](build_config.example.json).

| Field | Default | Meaning |
|---|---|---|
| `destinationRepo` | `$REGISTRY_BASE/<folder>` | Full registry repo (no tag) |
| `tag` | branch name | Image tag |
| `s2iImage` | — | If set → S2I build from this builder image (no Dockerfile needed) |
| `dockerfilePath` | `Dockerfile`, else `Containerfile` | Docker-strategy build file |
| `contextDir` | folder root | Build context, relative to the folder |
| `env` | — | Build-time env (`[{name,value}]`) |
| `buildArgs` | — | Docker `--build-arg`s (`[{name,value}]`) |
| `resources` | — | Build pod resource requests/limits |
| `noCache` | `false` | Disable layer cache (docker strategy) |

`s2iImage` set ⇒ Source/S2I strategy; otherwise Docker strategy.

## Setup

1. **Cluster access** — a `build-bot` ServiceAccount in the build namespace with rights
   to manage `buildconfigs`/`builds`/`secrets`. Its token → CI variable `OC_TOKEN`.
2. **CI variables** — set the ones listed at the top of
   [`gitlab-ci.yml`](gitlab-ci.yml) (mark credentials *masked*). The registry and git
   pull secrets are created/updated in-cluster automatically from those variables on
   each run.
3. **Wire the pipeline** — repo-root `.gitlab-ci.yml`:
   ```yaml
   include:
     - local: image-builder/gitlab-ci.yml
   ```
4. Optional: add a pipeline **schedule** on the default branch so `cleanup-orphans`
   sweeps stragglers even if a branch was deleted without a merge pipeline.

## Local check

```bash
./build.sh selftest   # pure logic, no cluster
```

## Notes / limits

- BC names are capped at 63 chars; very long folder+branch combos get a hash suffix.
- `skopeo delete` requires the registry to allow tag deletion; if disabled, cleanup
  removes the BC and logs the skipped tag (rely on a registry retention policy).
- The BuildConfig clones the git source *in-cluster*, so `GIT_TOKEN` must be a durable
  credential (deploy token / PAT), not the ephemeral CI job token.
