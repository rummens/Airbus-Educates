# Workshop Plan: lab-b01-docker-to-k8s

## 1. Workshop Metadata

- **Name:** `lab-b01-docker-to-k8s`
- **Title:** From Docker to Kubernetes on DCS
- **Description:** Map a Docker / docker-compose mental model onto Kubernetes objects — turn a `docker run` / compose example into an equivalent Deployment + Service + ConfigMap, deploy it, and reconcile what does *not* translate on an air-gapped, non-root DCS.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** Module A (Core) — esp. A02 (Kubernetes Essentials), A03 (Config)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (compose file side by side with the K8s manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (see the Deployment/Pod/Service land)
- Examiner: `enabled: true`
- Budget: `medium`
- **vcluster decision:** `false` — native OpenShift session namespace. A single migrated app needs no cluster-scoped objects; the session namespace *is* the learner's DEV namespace. (DEV vs PROD policy split is B06.)
- Workshop image: `dcs-workshop-base`
- Sample app image: `{{< param dcs_registry >}}/samples/hello-dcs:1.0` (Harbor-mirrored, non-root, port 8080).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Map `docker run` / docker-compose concepts to Kubernetes objects (container → Pod/Deployment, `-p`/`ports` → Service, `-e`/`environment` → env/ConfigMap, `-v` → Volume).
- Produce an equivalent Deployment + Service + ConfigMap from a compose example.
- Identify what does NOT translate on DCS and why: `privileged`/host mounts rejected, no `latest` tag, non-root/SCC, images must come from Harbor.
- Deploy the migrated app and confirm it runs the "K8s way."

## 4. Connection to Previous Workshop

**Already known (from Core, Module A):** deploy a workload with `oc apply` and Deployment/Service objects (A02); ConfigMaps and env config (A03); the `hello-dcs` sample. Core taught the *terms* and the lifecycle basics.

**New here:** the *translation reflex* — coming from a Docker/compose model and mapping it onto those objects; and the DCS constraints that break a naïve lift-and-shift (SCC/non-root, Harbor-only images, no `latest`, no privileged/host mounts).

**Do NOT re-teach:** what a Deployment/Service/ConfigMap is or how `oc apply` works (A02/A03) — reference as established; this lab is about the *mapping*, not the objects.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/docker-compose.yml` — the *source of truth to migrate*: a single `hello-dcs` service with `image:`, `ports: 8080`, an `environment:` var (e.g. `GREETING`), and one deliberately un-portable line (a host bind `volumes:` and/or `privileged: true`) to drive the "doesn't translate" discussion.
- `exercises/deployment.yaml` — starter Deployment shell the learner fills in during the migration; image `${DCS_REGISTRY}/samples/hello-dcs:1.0`, non-root, resource requests/limits, port 8080.
- `exercises/service.yaml` — Service `hello-dcs`, port 8080 → targetPort 8080, selector matches Deployment.
- `exercises/configmap.yaml` — ConfigMap holding `GREETING`, wired into the Deployment as env.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note. Frame: "I know Docker — how does this map to DCS?" Objectives; open `docker-compose.yml` (`editor:open-file`).
- **`01-the-mental-model.md`** — concept. Side-by-side table: `docker run`/compose ↔ Deployment/Service/ConfigMap/Volume. Declarative-desired-state vs `docker run` imperative. Container constructs → upstream ([Pods](https://kubernetes.io/docs/concepts/workloads/pods/)); no command → no examiner.
- **`02-container-to-deployment.md`** — translate the compose `service` → Deployment: `editor:open-file` `deployment.yaml`, `editor:select-matching-text` the image/env/port, complete it. Apply with the Harbor ref: `envsubst < deployment.yaml | oc apply -f -`. Check: 1 ready replica.
- **`03-ports-to-service.md`** — compose `ports:` → a Service, not `-p` host publish. `oc apply -f service.yaml`; reach it in-cluster by DNS (`curl`). Checks: service has endpoints; responds 200.
- **`04-env-to-configmap.md`** — compose `environment:` → ConfigMap + env ref. `oc apply -f configmap.yaml`; roll the Deployment; confirm the greeting changed. Standard construct → upstream. Check: pod env / response reflects the ConfigMap value.
- **`05-what-doesnt-translate.md`** — the reconciliation. Walk the un-portable compose lines: `privileged`/host bind mounts (rejected by SCC), `latest` tag (banned — pin a digest/version), run-as-root (non-root SCC), `image:` from Docker Hub (must be Harbor via `{{< param dcs_registry >}}`). *Why* DCS rejects each. DCS-specific → `{{< param dcs_docs_base_url >}}/concepts/security-context-constraints` + blurb. Examiner: knowledge-check style (identify which compose lines are illegal on DCS).
- **`99-workshop-summary.md`** — recap the mapping + the four DCS constraints. **Check Your Understanding** (3–4 Q). Bridge to **B02**: "you migrated an image someone else built — next, build *your own* code into an image on-cluster with a BuildConfig."

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Manifests referenced by relative name. No `cd`.
- **Carry-forward bug:** any manifest with `${DCS_REGISTRY}` is applied via `envsubst < file.yaml | oc apply -f -`, never a plain `oc apply -f file.yaml`.

## 8. Design Notes

- Covers **course-topics idea 7b** (Docker→K8s migration). On-ramp lab — deliberately placed **first** in the Developer track so Docker-native developers get a bridge before the build labs (B02/B03).
- **No app-lifecycle re-teach:** Core (A02/A03) already covers deploy/config; this lab reuses those skills purely as the *target* of the translation. Keep the focus on mapping + constraints.
- The un-portable compose lines are the pedagogical core — they surface the DCS security posture (SCC, non-root, Harbor-only, no `latest`) concretely rather than as a lecture.
- Sets up **B02** (build your own image) and **B06** (the DEV vs PROD policy split that the SCC/Kyverno posture hinted at here).
