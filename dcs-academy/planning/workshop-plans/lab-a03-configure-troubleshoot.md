# Workshop Plan: lab-a03-configure-troubleshoot

## 1. Workshop Metadata

- **Name:** `lab-a03-configure-troubleshoot`
- **Title:** Configure & Troubleshoot Your App
- **Description:** Move your app's configuration out of ad-hoc env vars into a ConfigMap and a Secret, roll out the change — then, when it breaks, diagnose the fault from logs, events and `describe`, fix it, and confirm recovery.
- **Duration:** 30m
- **Difficulty:** intermediate
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A02 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view/edit ConfigMap, Secret, and the broken manifest)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: **not** enabled — CLI-first diagnosis; console is A08.
- Examiner: `enabled: true`
- Budget: `medium`
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs Deployment, **pre-deployed via `session.objects`** so the learner starts where A02 ended (a running, env-customised app).
- **vcluster decision:** `false` — plain session namespace; continues A02's app.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:
- Externalise app configuration into a **ConfigMap** and consume it (env + mounted file).
- Store a credential in a **Secret** and inject it without printing its value.
- Trigger and observe a **rollout** when configuration changes.
- Diagnose a failing workload with `oc logs`, `oc describe` and `oc get events`, identify the root cause, **fix it, and verify recovery**.

## 4. Connection to Previous Workshop

**Already known** (from A02): the hello-dcs Deployment; `oc set env`; `oc rollout status`; that a rollout replaces pods; the Deployment→ReplicaSet→Pod chain and labels/selectors; reaching the app locally. The app is pre-deployed for you.

**What is new here:**
- **ConfigMap** and **Secret** objects — the scalable replacement for the ad-hoc `oc set env` from A02.
- Wiring config as env (`envFrom`/`valueFrom`) and as a mounted volume.
- The **observe → hypothesise → fix → verify** debugging loop against a real fault.
- Reading events and previous-container logs.

**What should NOT be re-taught:** what a Deployment/rollout is (A02 — reference it); basic `oc get`/`describe` syntax (used here as a *method*, not introduced from scratch).

## 5. Exercise Files to Create

- `exercises/configmap.yaml` — ConfigMap `hello-dcs-config` with a couple of keys the app reads (e.g. a greeting/message + a feature flag).
- `exercises/secret.yaml` — Secret `hello-dcs-secret` (Opaque), one credential-shaped key; values as `stringData` for readability, with an explicit note that real secrets never live in git.
- `exercises/deployment-configured.yaml` — the A02 Deployment expressed declaratively, extended with `envFrom` (ConfigMap) + `env.valueFrom.secretKeyRef` (Secret) and a mounted ConfigMap volume. **This is also the first manifest the learner applies** — the A02→A03 imperative→declarative handoff.
- `exercises/broken-deployment.yaml` — the configured Deployment with **one seeded, deterministic fault** (recommended: a ConfigMap key rename / missing key referenced by `envFrom`, or a wrong image tag → `ImagePullBackOff`). One fault, one edit to fix. Applied via `session.objects` or in the lab step so the learner lands on a failing app for the troubleshoot arc.
- `exercises/README.md` — placeholder.

Note: manifests reference `{{< param dcs_registry >}}` for the image. If any manifest uses `${DCS_REGISTRY}`-style env substitution rather than a ytt param, apply with `envsubst < file.yaml | oc apply -f -`, never plain `oc apply` (carry-forward bug).

## 6. Workshop Instruction Pages

Arc: config doesn't scale → externalise → roll out → **it breaks** → diagnose → fix → verify.

- **`00-workshop-overview.md`** — intro + first-time note. Recap the A02 gap: "you set config with `oc set env` — fine for one value, but real apps have many settings and secrets." Objectives; open `configmap.yaml` (`editor:open-file`).
- **`01-config-in-a-configmap.md`** — why externalise: same image → many environments; no rebuild to change a setting; air-gapped promotion moves config, not new images (VM-world analogy, tapering: "like an answer file / config drive attached to a template VM"). Apply `configmap.yaml`; apply `deployment-configured.yaml` (wired via `envFrom` + a mounted file); `oc rollout status`; re-reach the app to show the configured value served. Examiner: ConfigMap exists **and** the app responds with the configured value.
- **`02-a-secret.md`** — why Secrets differ from ConfigMaps (base64 ≠ encryption; RBAC-guarded; keep out of logs/manifests). Apply `secret.yaml`; it's already referenced by the Deployment via `secretKeyRef`. Prove the key is set **without echoing the value**: `oc exec deploy/hello-dcs -- printenv | grep <KEY_NAME>` (page shows the key name, not the value). Examiner: Secret exists and is referenced by the Deployment.
- **`03-roll-out-a-change.md`** — change a ConfigMap value (`editor:replace-matching-text`), `oc apply`, `oc rollout restart deploy/hello-dcs`; in the **lower split terminal** `watch oc get pods` (`execute-2`) to see old→new pods; confirm the new value served (upper, `execute-1`). Examiner: app serves the updated value; rollout complete.
- **`04-then-it-breaks.md`** — the pivot. Apply (or the session pre-applies) `broken-deployment.yaml`; `oc get pods` shows the bad state. Name the signature (`ImagePullBackOff` / `CreateContainerConfigError` / never-Ready). **Observe only, no fixing yet.** Examiner: the app is currently **not** ready (confirms the fault is live).
- **`05-diagnose-it.md`** — the three lenses, used together: `oc describe pod <p>` (events + reasons), `oc get events --sort-by=.lastTimestamp`, `oc logs <p>` (+ `--previous` for crashes). Walk to the root-cause line and state the fix. VM-world analogy (very light): "read the boot console before rebuilding the VM." Examiner: none (investigation page).
- **`06-fix-and-verify.md`** — correct the fault (`editor:replace-matching-text` in `broken-deployment.yaml` — e.g. fix the key name or image tag), `oc apply`, `oc rollout status`, confirm Running/Ready and serving. Examiner: app Running, Ready, responds 200 with the expected value (confirms **both** the recovery and that config still applies).
- **`99-workshop-summary.md`** — recap ConfigMap vs Secret, env vs volume, rollout-on-change, and the observe→hypothesise→fix→verify loop with a short common-signatures table. Deliberate gap: the app is still only reachable *locally* (port-forward from A02) — no stable in-cluster address, no external URL → motivates **A04 (Expose Your App)**. **Check Your Understanding** (5 Q): ConfigMap vs Secret; why base64 isn't encryption; what triggers a rollout; where to look first when a pod won't start; what `--previous` gives you.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`. No `cd`.
- **Split terminal:** upper `execute-1` = apply/inspect/`curl`; lower `execute-2` = `watch oc get pods` during rollouts.
- Patterns: `oc apply -f <file>` (or `envsubst < f | oc apply -f -` if `${VAR}` present), `oc rollout restart/status deploy/hello-dcs`, `oc exec deploy/hello-dcs -- printenv`, `oc describe pod <p>`, `oc get events --sort-by=.lastTimestamp`, `oc logs <p> [--previous]`, `oc get configmap/secret`.

## 8. Design Notes

- Covers **course-topics ideas 8 and 10** — folds old **B02 (Config & Secrets)** + old **B04 (Debugging & Logs)** into one Core lab. The union works because a config mistake *is* the most natural way to break the app, so the fault flows straight out of the config exercise instead of feeling bolted on.
- **Difficulty = intermediate** (not beginner): the diagnosis loop is a genuine step up, and picking the higher level per house standard.
- **One deterministic fault** keeps the examiner reliable and the fix a single checkable edit. A config-shaped fault (missing/renamed ConfigMap key) is preferred because it ties the two halves together; an `ImagePullBackOff` variant is a good alternative that reinforces air-gapped reality ("the tag isn't mirrored to Harbor").
- **Security posture:** no secrets in images, no secret values echoed to terminal/logs; base64 explicitly *not* encryption. `stringData` is used in the exercise file for readability only, with a warning that production secrets are created out-of-band. The Developer/Security tracks go deeper.
- **First declarative manifest** of the course lands here (A02 was imperative). `deployment-configured.yaml` is the handoff — reference the A02 reveal page so the learner recognises the shape.
- Deliberate gap for A04: still no Service/Route — the app has no stable address yet.
