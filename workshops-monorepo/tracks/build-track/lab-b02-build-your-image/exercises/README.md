Exercise files for the Build Your Image workshop.

- `buildconfig.yaml`  — the recipe: a binary source, the Docker strategy pointed at `Containerfile`,
  and an ImageStream for the output.
- `app/Containerfile` — what gets built: a small change on top of the sample image.
- `app/README.txt`    — stands in for application source.
- `deployment.yaml`   — deploys the image **you** built, by its ImageStream tag.

Manifests carrying `${DCS_REGISTRY}` or `${SESSION_NAMESPACE}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
