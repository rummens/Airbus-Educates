# Local workshop testing on OpenShift (portal-less)

Deploy, run examiner graders, and tear down one lab against the real dev OpenShift cluster — no CRC required. Two helpers automate the flow (stdlib Python only):

```bash
# deploy a workshop from git (portal-less; drops the custom base image so it
# runs on the stock base-environment). --vcluster / --delete.
./deploy_workshop.py lab-a02-kubernetes-essentials

# list every deployed session (name, phase, URL):
./deploy_workshop.py --list

# run the workshop's smoke test (setup steps + every examiner check) in the
# live session pod.
./smoke_test.py lab-a02-kubernetes-essentials

# run a whole track in one go (sequential, with logs + a pass/fail summary):
./run_track.sh tracks/core-track

# run only changed labs vs base:
./run_track.sh --dry-run tracks/core-track
```

### What runs in CI

| Stage | What |
|---|---|
| `test` (fast) | portal pytest + workshop coverage / link / label checks. Required on MRs. |
| `e2e` (cluster) | `smoke_test.py` for changed labs + `flow_test.py --mode both`. Required on MRs. |

The cluster smoke jobs run on any available runner: they use `$CI_BASE_IMAGE` (which carries `oc`) and log into the dev OpenShift cluster via the `CI_OC_*` variables (`CI_OC_HOST`, `CI_OC_TOKEN`, `CI_OC_INSECURE`, …). No dedicated runner tag is required.

### TLS: routes auto-terminate with the cluster's managed cert

On OpenShift, Educates routes get the standard cluster wildcard cert, so every `<session>` host resolves and serves TLS automatically. No self-signed cert ceremony — the `curl -k` flag isn't needed for browser access.

### Why portal-less

`session-manager` reconciles `WorkshopSession` CRs directly, so one lab comes up in seconds without a catalog, a login, or the capacity limits of a TrainingPortal. Use the portal when the thing under test *is* the portal path (catalog, launch, oauth).

### Prerequisites

- An `oc` login to the dev OpenShift cluster (context `logged-user` by default).
- The Educates operator installed (CRDs `Workshop`, `WorkshopEnvironment`, `WorkshopSession`).
- The `Workshop` CR you want exists: `oc get workshops.training.educates.dev`.

### Run a whole track in one go

`run_track.sh` points at a folder, discovers every workshop under it, runs `smoke_test.py` for each one at a time, and prints a pass/fail summary. It also pauses ArgoCD auto-sync on the app that manages the Workshop CRs for the duration and always restores it on exit — the portal-less deploy rewrites those shared CRs, so selfHeal must be off while testing.

```bash
./run_track.sh tracks/core-track                 # a whole track
./run_track.sh tracks/core-track/lab-a03-expose-app  # one lab
./run_track.sh --dry-run tracks/core-track       # list what would run, touch nothing
```

Labs with no smoke-plan (or a plan with no checks, e.g. a content-tour lab) are skipped and listed. Env overrides: `CTX` (oc context), `ARGO_APP`/`ARGO_NS`, `SMOKE_ARGS` (default `--no-links`).

### Smoke plans and coverage

A `smoke-plan/<lab>.json` lists `run` steps (set up learner state) and `check` steps (invoke the workshop's examiner graders). `coverage_check.py` enforces that every `examiner:execute-test` block is either in a plan or explicitly excluded, so an author can't add a check and forget to wire a plan.

Plans have two extras:
- `"expect_fail": true` on a step — it's expected to FAIL here (platform-only features)
  but pass on the real DCS platform; the runner inverts the verdict.
- `"exclude": [{"check": …, "args": […], "reason": …}]` — a content check the runner can't
  run (interactive, or platform-only). Coverage counts it as consciously accounted for.

Bootstrap a plan for a new workshop from its content:

```bash
python3 test/workshops/coverage_check.py <lab> --scaffold > test/workshops/smoke-plans/<lab>.json
# then tune the run steps (rollout waits, env) — scaffold marks itself a draft
```

> The `lab-b*` (dev-track) plans are currently scaffold drafts: coverage is satisfied,
> but their `run` steps need one real-cluster pass to tune before the smoke tier is trustworthy.
