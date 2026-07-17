# DCS Academy — tests

All test content lives here, in three layers (see `../TEST_STRATEGY.md` for the rationale).

```
test/
  portal/        Layer 1 — portal unit tests (pytest, hermetic, no cluster)
  workshops/     Layer 3 — per-workshop tests + the deploy/smoke/flow tooling
  ci/            scripts the GitLab pipeline (and you, locally) run
```

## Layer 1 — portal unit (`test/portal/`)

Hermetic pytest suite for the Flask portal (`images/dcs-academy-portal/portal`). Demo
catalog + throwaway sqlite; Educates REST, k8s API and git are monkeypatched. No cluster.

```bash
test/ci/run-python.sh                 # pytest + 90% coverage gate
```

`conftest.py` puts the portal source on `sys.path` (the suite lives here, the package
lives under `images/`). Coverage gate is `COVERAGE_MIN` (default 90).

## Layer 3 — workshops (`test/workshops/`)

| Tool | Cluster? | What |
|---|---|---|
| `coverage_check.py` | no | every content `examiner:execute-test` is exercised by the smoke plan (or explicitly `exclude`d). This is what keeps a plan honest when a workshop command changes. |
| `link_check.py` | no | every link in the workshop content resolves (external 2xx; relative target exists; air-gapped `{{< param … >}}` links reported, checked with `--check-internal`). |
| `label_check.py` | no | each lab's dev/prod lifecycle label matches its Route usage (a Route needs a PROD namespace). |
| `deploy_workshop.py` | yes | deploy one workshop to CRC/OpenShift, portal-less, from git. |
| `smoke_test.py` | yes | deploy → run the examiner graders (`smoke-plans/<lab>.json`) → link-check → teardown. |
| `flow_test.py` | yes | spin up a real session (namespace + vcluster variants), assert it's reachable + basic commands run, teardown. |

```bash
# no cluster (fast, blocks merges):
python3 test/workshops/coverage_check.py --all
python3 test/workshops/link_check.py --all
python3 test/workshops/label_check.py --all

# cluster (CRC):
python3 test/workshops/smoke_test.py lab-a02-kubernetes-essentials
python3 test/workshops/flow_test.py --mode both
```

### Smoke plans and coverage — how they stay linked

A `smoke-plans/<lab>.json` lists `run` steps (set up learner state) and `check` steps
(invoke the workshop's examiner graders). You do **not** hand-audit them: `coverage_check.py`
parses the workshop content's `examiner:execute-test` blocks and fails if any is not
covered by a plan step (matching test name + args; `$VAR` args are treated as wildcards
since Educates expands them at runtime). Change a check in the content and coverage goes
red until the plan is updated.

Plan extras:
- `"expect_fail": true` on a step — it's expected to FAIL on CRC (Kyverno/SCC not present)
  but pass on the real platform; the runner inverts the verdict so CRC stays green.
- `"exclude": [{"check": …, "args": […], "reason": …}]` — a content check CRC can't run
  (interactive, or platform-only). Coverage counts it as consciously accounted for.

Bootstrap a plan for a new workshop from its content:

```bash
python3 test/workshops/coverage_check.py <lab> --scaffold > test/workshops/smoke-plans/<lab>.json
# then tune the run steps (rollout waits, env) — scaffold marks itself a draft
```

> The 6 `lab-b*` (dev-track) plans are currently scaffold drafts: coverage is satisfied,
> but their `run` steps need one CRC pass to tune before the smoke tier is trustworthy.

## CI (`test/ci/`)

`.gitlab-ci.yml` wires these. Path-gated so a python-only change skips workshop jobs.

```bash
test/ci/run-python.sh                  # Layer 1
test/ci/run-workshops.sh               # Layer 3 fast tier (coverage + links), all workshops
test/ci/run-workshops.sh --changed     # …only workshops changed vs the base ref
test/ci/run-workshops.sh --changed --smoke   # + cluster smoke (needs oc)
python3 test/ci/changed.py             # what changed → PYTHON=… WORKSHOPS="…"
```

CRC notes (portal SIGILLs on arm64, self-signed cert, push-before-redeploy) are in
[workshops/README.md](workshops/README.md).
