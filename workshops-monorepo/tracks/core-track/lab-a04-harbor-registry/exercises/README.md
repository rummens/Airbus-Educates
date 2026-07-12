Exercise files for "Working with Harbor".

- `pod-from-catalog.yaml` — a Pod that runs an image pulled from a DCS catalog
  (image via `${DCS_REGISTRY}`).

The Pod image uses the `${DCS_REGISTRY}` environment variable so the manifest is not tied
to a specific registry; apply it with `envsubst` (the instructions do this for you).
