Exercise files for "Deploy Your First App on DCS".

- `deployment.yaml` — the sample app Deployment (image via `${DCS_REGISTRY}`)
- `service.yaml` — the Service that gives it a stable in-cluster address

The Deployment image uses the `${DCS_REGISTRY}` environment variable so the manifest is
not tied to a specific registry; apply it with `envsubst` (the instructions do this for you).

The `hello-dcs` sample app is carried across the Developer track — later workshops add
config, probes, and storage to these same manifests.
