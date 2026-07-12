Exercise files for "Debugging & Logs".

- `broken-deployment.yaml` — the sample app, deployed **broken** on purpose. Your job in
  this workshop is to diagnose why it won't run and fix it (a single edit).

The Deployment image uses the `${DCS_REGISTRY}` environment variable so the manifest is
not tied to a specific registry; apply it with `envsubst` (the instructions do this for you).
