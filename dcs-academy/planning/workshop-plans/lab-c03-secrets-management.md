# Workshop Plan: lab-c03-secrets-management

## 1. Workshop Metadata

- **Name:** `lab-c03-secrets-management`
- **Title:** Secrets Management on DCS
- **Description:** Spot secrets leaking through images, logs, and env dumps; move a credential into a Kubernetes Secret sourced by reference; and verify it is no longer exposed.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module C — Security & Compliance)
- **Prerequisites:** Module A (esp. A02 — Deployments, env; B02 config/secrets is complementary but not required).
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- Console: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Run location: **native OpenShift session namespace** (vcluster `enabled: false`). No admin ops. `budget: medium`.
- Workshop image: **`dcs-workshop-base`**.
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Identify the three common secret-leak paths: **baked into the image**, **printed to logs**, and **inline in a manifest / env dump**.
- Explain that a Kubernetes **Secret** is base64-encoded (not encrypted) and that its protection comes from **RBAC** + platform **etcd encryption**, not obscurity.
- Move a plaintext credential into a Secret and consume it via `secretKeyRef` (env) rather than a literal value.
- Verify a secret is not exposed — not in `oc describe`, not in the pod's rendered manifest as a literal, not in logs.
- Describe stronger options DCS offers (sealed/external secrets) at a concept level.

## 4. Connection to Previous Workshop

Elective — assumes Module A. **Already known:** Deployments, setting env, `oc apply`, reading logs. **New here:** the leak paths, `Secret` objects, `secretKeyRef`, base64-vs-encryption, RBAC on secrets. **Do NOT re-teach:** how to deploy/inspect a workload.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/deploy-leaky.yaml` — a Deployment (`$DCS_REGISTRY/samples/hello-dcs:1.0`) with a **plaintext** `env` value `API_TOKEN: "s3cr3t-plaintext-token"` — the bad pattern.
- `exercises/secret.yaml` — a `Secret` (`stringData: { api-token: ... }`) the learner creates/applies. *(Or created via `oc create secret generic` in-terminal; plan uses the manifest so it's inspectable in the editor.)*
- `exercises/deploy-fixed.yaml` — the same Deployment but `env` uses `valueFrom.secretKeyRef` (no literal). Ends the leak.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — overview + first-time note. DCS blurb: **Governance & compliance** (T&Cs cover data/secret handling) → `{{< param dcs_docs_base_url >}}/governance/overview`; [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) → upstream.
- **`01-how-secrets-leak.md`** — concept. The three leak paths (image env/ARG, stdout logs, inline manifest / `oc set env --list`). **base64 ≠ encryption** — a Secret is encoded, protected by RBAC and (platform-side) etcd encryption at rest. Least-privilege on `get secret`. *(Concept page.)*
- **`02-spot-the-bad-pattern.md`** —
  - `editor:open-file` `deploy-leaky.yaml`; highlight the plaintext `API_TOKEN`.
  - `terminal:execute` `oc apply -f deploy-leaky.yaml`; wait for rollout (`oc rollout status deploy/leaky-app --timeout=60s`) → examiner `verify-leaky-running` (available; polling).
  - `terminal:execute` `oc set env deploy/leaky-app --list | grep API_TOKEN` → examiner `verify-leak-visible` (the plaintext value is visible — proving the leak). Explain anyone with `get deploy` sees it; it would also land in git if this manifest were committed.
- **`03-move-to-a-secret.md`** —
  - `editor:open-file` `secret.yaml`; explain `stringData` (author-friendly; stored base64).
  - `terminal:execute` `oc apply -f secret.yaml` → examiner `verify-secret-exists` (secret `app-secrets` present with key `api-token`).
  - `editor:open-file` `deploy-fixed.yaml`; show `valueFrom.secretKeyRef`.
  - `terminal:execute` `oc apply -f deploy-fixed.yaml`; `oc rollout status deploy/fixed-app --timeout=60s` → examiner `verify-fixed-running` (available; polling).
- **`04-verify-no-leakage.md`** —
  - `terminal:execute` `oc set env deploy/fixed-app --list | grep API_TOKEN` → examiner `verify-no-literal` (shows the *reference* to the secret, NOT the literal value). Contrast with page 02's output.
  - `terminal:execute` `oc get secret app-secrets -o jsonpath='{.data.api-token}' | base64 -d` → show it's retrievable *only* with secret-read RBAC; teach that this is why `get secret` is a privileged verb. Examiner `verify-secret-decodable` (decode returns the token) — demonstrates base64, not encryption.
  - Concept: DCS stronger options — **Sealed Secrets / external secret store** (so secrets never sit in plaintext in git) → concept + DCS docs; cleanup note.
- **`98-your-feedback.md`** — standard (workshop=lab-c03-secrets-management).
- **`99-workshop-summary.md`** — recap; **Check Your Understanding** (3 Q): the three leak paths; base64 vs encryption + what actually protects a Secret; why `secretKeyRef` beats an inline env value. Final examiner (`verify-no-literal`-style) as the knowledge-check action.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. All `oc`/`editor` on local manifests — no `cd`.

## 8. Design Notes

- **No new image:** the leak is in the *manifest/env*, using `hello-dcs`. Fully testable air-gapped.
- The `verify-secret-decodable` step is deliberately the "aha": base64 is trivially reversible, so the security is RBAC + etcd-encryption, not the encoding. This is the most common tenant misconception.
- Runtime-hardening trio with **C01**/**C02**. Sealed/external secrets kept as concept (platform-owned); could become a future dedicated lab (note in expansion ideas).
