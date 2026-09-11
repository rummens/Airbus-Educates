Exercise files for the Scaling, Health & Resources workshop.

- `deployment-oversized.yaml` — the app with intentionally large `requests`/`limits`,
  applied on purpose to trigger a namespace quota rejection.
- `deployment-probes.yaml`    — the target, healthy app: right-sized `requests`/`limits`
  plus liveness and readiness probes.

The app itself (`hello-dcs`) is already running when the session starts — there's nothing
to apply until you get to the quota page.
