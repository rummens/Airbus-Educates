Exercise files for the Configuration & Secrets workshop.

- `configmap.yaml` — non-secret settings (env vars + a mounted config file).
- `secret.yaml` — one credential (Opaque). `stringData` is plain text for readability only;
  real secrets are created out-of-band and never committed to git.
- `deployment-configured.yaml` — the hello-dcs Deployment wired to consume both (envFrom +
  secretKeyRef + a mounted ConfigMap volume).

The `hello-dcs` Deployment and Service are already running when the session starts, with config
still baked in — you externalise it here.
