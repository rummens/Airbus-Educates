Exercise files for the Metrics & Monitoring workshop.

- `deployment.yaml`     — the app, serving Prometheus exposition format on `/metrics`.
- `service.yaml`        — with a **named** port, because a ServiceMonitor refers to ports by name.
- `servicemonitor.yaml` — your request to be scraped, in your own namespace.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
