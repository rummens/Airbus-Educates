# DCS Academy — Test Strategy

**Status: implemented.** All test content lives under `test/` (see `test/README.md`).
Three layers, matched to what breaks: **portal code**, **user flow**, **workshop content**.

---

## Layer map

| Layer | Proves | Tool | Cluster? | Blocks MR? |
|---|---|---|---|---|
| **1. Portal unit** | Flask routes, DB, trophies, auth, OAuth, proxy, educates/k8s clients | `test/portal/test_portal.py` (pytest) | no | yes |
| **2. User flow** | real session (namespace + vcluster) comes up, URL 200, basic commands run | `test/workshops/flow_test.py` | yes | no |
| **3a. Coverage** | every workshop command has a smoke test (or explicit exclude) | `test/workshops/coverage_check.py` | no | yes |
| **3b. Links** | every content link resolves 200 / target exists | `test/workshops/link_check.py` | no | yes |
| **3d. Labels** | each lab's dev/prod lifecycle label matches its Route usage | `test/workshops/label_check.py` | no | yes |
| **3c. Smoke** | examiner graders pass end-to-end on a live cluster | `test/workshops/smoke_test.py` | yes | no |

Fast lanes (1, 3a, 3b, 3d) need no cluster and gate merges. Cluster lanes (2, 3c) run
manual-on-MR / automatic-on-schedule and report without blocking (cluster flakiness ≠ code bug).

---

## Layer 1 — portal unit

**90% coverage gate** (`COVERAGE_MIN`, your answer #1). Currently **90.6%**, 66 tests,
deterministic. Hermetic: demo catalog, throwaway sqlite, monkeypatched Educates/k8s/git.
`test/portal/conftest.py` bridges the package path; `.coveragerc` excludes `__main__` demos.

```bash
test/ci/run-python.sh
```

Fixed along the way: stale committed `__pycache__/*.pyc` (broke imports under some orders —
now untracked + gitignored); two tests drifted from the current API (`terminate_session`,
`/session/<n>/end`); demo courses were missing the `vcluster` key the launch template needs.

## Layer 2 — user flow (`flow_test.py`)

Spins up a **real** session and proves a learner gets a working environment: session pod
Running → dashboard + editor answer HTTP 200 → basic terminal commands succeed (identity,
namespace access, a ConfigMap write). Two variants:

- **namespace** (default lab a02) — asserts `oc get nodes` is *denied* (scoped).
- **vcluster** (default lab a03) — asserts `oc get nodes` *works* (isolated cluster).

```bash
test/workshops/flow_test.py --mode both
```

Runs portal-less (the Educates portal SIGILLs on CRC arm64 — your answer #2, CRC is the
only test target; x86 is the final home where the same mechanics front the portal login).

## Layer 3 — per-workshop

**The plan↔workshop linkage** (your requirement: don't hand-maintain plans). `coverage_check.py`
parses each workshop's `examiner:execute-test` blocks and fails if any isn't exercised by a
`smoke-plans/<lab>.json` step (name + args; `$VAR` args are wildcards). Change a check in the
content → coverage goes red until the plan catches up. `--scaffold` bootstraps a plan from
content. Plans support `expect_fail` (CRC-can't, platform-can) and `exclude` (with reason).

**Links** (your requirement: all descriptions 200). `link_check.py` checks external (2xx),
relative (target exists), and air-gapped `dcs_docs_base_url` links (reported; `--check-internal`
+ `--param` to verify on the real network). Bot-blocked 401/403 (docs.openshift.com) are
tolerated, not failed.

```bash
test/workshops/coverage_check.py --all
test/workshops/link_check.py --all
test/workshops/smoke_test.py lab-a02-kubernetes-essentials   # needs cluster
```

Current state: **all 20 workshops** at 100% coverage-accounted; **all links green** (fixed a
real 404 in lab-b04). The 6 dev-track (`lab-b*`) plans are **scaffold drafts** — coverage is
satisfied, but their `run` steps need one CRC pass to tune before the smoke tier is trusted.

---

## CI (`.gitlab-ci.yml`, your answer #3)

Path-gated (`rules: changes:`) so a python-only change skips workshop jobs and vice-versa;
per-workshop smoke narrows to changed workshops via `test/ci/changed.py`.

- **stage `test`** (no cluster, blocks MR): `portal-tests` (changed python) + `workshop-static`
  (changed workshops → coverage + links).
- **stage `e2e`** (runner tag `crc`, manual-on-MR / auto-on-schedule, `allow_failure`):
  `workshop-smoke` (`--changed --smoke`) + `user-flow`.

Output names the **cost of each failure** (untested command / dead link / workshop broken on
platform / no working environment), so a red pipeline is triaged at a glance.

Local equivalents:
```bash
test/ci/run-python.sh
test/ci/run-workshops.sh [--changed] [--smoke]
```

---

## Follow-ups (not blocking)

- Tune the 6 `lab-b*` scaffold plans against a live CRC (run steps: rollout waits, env).
- `cache.start_refresher` thread loop is the one meaningful uncovered path (deliberate;
  90.6% clears the gate).
