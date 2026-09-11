Exercise files for the Autoscaling workshop.

- `deployment.yaml` — the app the autoscaler will own. Sets `resources.requests.cpu`,
  which is what the HPA's utilisation percentage is measured against.
- `service.yaml`    — a stable address to drive load at.
- `hpa.yaml`        — the HorizontalPodAutoscaler: CPU at 50% of requests, 1 to 6 replicas.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
