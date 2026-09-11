Exercise files for the Logs workshop.

- `deployment.yaml` — the app, writing request lines to stdout.
- `crashing.yaml`   — a container that logs a fatal error and exits, so there is something
  whose **previous** logs are worth reading.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
