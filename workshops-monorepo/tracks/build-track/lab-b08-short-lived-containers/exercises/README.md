Exercise files for the Short-Lived & Helper Containers workshop.

- `job-migrate.yaml`            — a Job that succeeds: runs to completion, retries up to
  `backoffLimit`, then deletes itself after `ttlSecondsAfterFinished`.
- `job-failing.yaml`            — the same shape, failing on purpose, to see a Job give up
  rather than crash-loop forever.
- `cronjob-report.yaml`         — a Job factory on a schedule, with `concurrencyPolicy`,
  history limits and `suspend`. Scheduled for 03:00 so it will not fire during the lab.
- `deployment-with-helpers.yaml` — one Pod with an **init container** (runs first, to
  completion) and a **sidecar** (the same API plus `restartPolicy: Always`, so it keeps
  running beside the app), sharing an `emptyDir` with the app.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
