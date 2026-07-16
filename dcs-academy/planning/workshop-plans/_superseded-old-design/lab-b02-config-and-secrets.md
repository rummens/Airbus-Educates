# Workshop Plan: lab-b02-config-and-secrets

## 1. Workshop Metadata

- **Name:** `lab-b02-config-and-secrets`
- **Title:** Configuration & Secrets
- **Description:** Externalise the sample app's configuration into a ConfigMap, inject a credential with a Secret, and roll out a config change without rebuilding the image.
- **Duration:** 35m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B01 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled
- Examiner: `enabled: true`
- Budget: `medium`
- **vcluster decision:** `false` — native session namespace (continues B01's app).
- Workshop image: `dcs-workshop-base`
- Sample app: the B01 hello-dcs Deployment (pre-deployed via `session.objects` so the learner starts where B01 ended).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Move app configuration out of the image into a ConfigMap and consume it (env + mounted file).
- Store a credential in a Secret and inject it without printing it into logs or manifests.
- Trigger and observe a rollout when configuration changes.
- Explain why config/secrets are externalised (12-factor, air-gapped promotion, no rebuild to reconfigure).

## 4. Connection to Previous Workshop

**Already known** (B01): the hello-dcs Deployment/Service, `oc apply`, `oc rollout status`, the DEV namespace.

**New here:** ConfigMap and Secret objects; wiring them as env vars and mounted volumes; how a config change drives a new rollout.

**Do NOT re-teach:** deploying/exposing the app (B01); Deployment/Service structure (A02).

## 5. Exercise Files to Create

- `exercises/configmap.yaml` — ConfigMap `hello-dcs-config` with a couple of keys (e.g. a greeting/message + a feature flag) the app reads.
- `exercises/secret.yaml` — Secret `hello-dcs-secret` (Opaque) with one credential-shaped key; values shown as `stringData` for readability, with a note that real secrets never live in git.
- `exercises/deployment-configured.yaml` — the B01 Deployment extended with `envFrom`/`env.valueFrom` (ConfigMap + Secret) and a mounted ConfigMap volume.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; recap "config is baked in" from B01 as the problem to solve; objectives; open `configmap.yaml`.
- **`01-why-externalise-config.md`** — what/why: same image → many environments; no rebuild to change a setting; air-gapped promotion moves config, not new images. VM-world analogy (light, tapering): "like answer files / a config drive attached to a template VM." Check: none (concept).
- **`02-a-configmap.md`** — create `hello-dcs-config` (`oc apply`); wire it as `envFrom` **and** a mounted file; re-apply the Deployment; `oc rollout status`; show the app picking up the value. Examiner: ConfigMap exists; app responds with the configured value.
- **`03-a-secret.md`** — why Secrets differ from ConfigMaps (base64 ≠ encryption; RBAC-guarded; keep out of logs); create `hello-dcs-secret`; inject one key as an env var via `secretKeyRef`; prove it's set **without echoing it** (`oc exec -- printenv | grep NAME` shows the key not the value in the page). Examiner: Secret exists and is referenced by the Deployment.
- **`04-roll-out-a-change.md`** — edit a ConfigMap value (`editor:replace-matching-text`), `oc apply`, trigger a rollout (`oc rollout restart deploy/hello-dcs`), watch old→new pods in a split terminal, confirm the new value served. Examiner: app serves the updated value; rollout complete.
- **`99-workshop-summary.md`** — recap ConfigMap vs Secret, env vs volume, rollout on change. Note the app still can't scale safely or report health → motivates **B03**. Check Your Understanding (4–5 Q). Suggest B03 next.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes.
- Patterns: `oc apply -f`, `oc rollout restart/status deploy/hello-dcs`, `oc exec deploy/hello-dcs -- printenv`, `oc get configmap/secret`.

## 8. Design Notes

- Covers **course-topics idea 8** (configuration & secrets).
- **Security posture (align with Module C):** show good practice now — no secrets in images, no secret values echoed to the terminal/logs; C14 (secrets management) goes deeper. Base64 is explicitly *not* encryption.
- Secret handling uses `stringData` **in the exercise file for readability only**, with an explicit warning that production secrets are created out-of-band (never committed).
- **Deliberate limitation:** one replica, no probes, no resource tuning → **B03** adds scaling/health/resources.
