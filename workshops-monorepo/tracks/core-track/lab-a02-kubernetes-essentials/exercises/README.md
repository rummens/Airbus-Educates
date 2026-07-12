Exercise files for "Kubernetes Essentials on DCS".

- `deployment.yaml` — the sample app Deployment (image via `${DCS_REGISTRY}`)
- `service.yaml` — the Service that fronts it

The Deployment image uses the `${DCS_REGISTRY}` environment variable so the manifest is
not tied to a specific registry; apply it with `envsubst` (the instructions do this for you).
