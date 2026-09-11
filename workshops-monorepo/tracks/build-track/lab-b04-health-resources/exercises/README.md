Exercise files for the Health & Resources workshop.

- `deployment-base.yaml`      — the starting point: one replica, no probes, no explicit
  resources, so its Pods take the namespace LimitRange defaults.
- `service.yaml`              — a stable address for the app, so readiness has an endpoint
  list you can watch.
- `deployment-oversized.yaml` — the same app with intentionally large `requests`/`limits`,
  applied on purpose to trigger a namespace quota rejection.
- `deployment-probes.yaml`    — the target, healthy app: right-sized `requests`/`limits`
  plus liveness and readiness probes.

Every manifest carrying `${DCS_REGISTRY}` is applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
