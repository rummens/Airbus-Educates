Exercise files for "Secrets Management on DCS".

- `deploy-leaky.yaml` — the **bad pattern**: a Deployment (`leaky-app`) with the credential
  hard-coded as a plaintext `env` value (`API_TOKEN`). Anyone who can read the Deployment can
  read the secret — and it would land in git if this manifest were committed.
- `secret.yaml` — a `Secret` (`app-secrets`) holding the credential under `stringData`
  (author-friendly plaintext on write; stored base64-encoded).
- `deploy-fixed.yaml` — the **fixed pattern**: the same Deployment (`fixed-app`) sourcing the
  credential via `valueFrom.secretKeyRef` instead of a literal.

Images use the `${DCS_REGISTRY}` environment variable so the manifests aren't tied to a
specific registry; the instructions apply them with `envsubst` for you.
