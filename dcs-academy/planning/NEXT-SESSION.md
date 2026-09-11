# DCS Academy — Session Handoff

**Last updated:** 2026-09-11 (overnight session). Read this first, then
[tasks.md](tasks.md).

## Where things stand

**Two new tracks are built, live-verified and published.**

| Track | Labs | State |
|---|---|---|
| Core (`core`) | 8 | unchanged — frozen baseline |
| Console (`console`) | 9 | unchanged — frozen baseline |
| **Build & Run (`build`)** | 10 + 3 console companions | **published**, every lab green on CRC |
| **Operate & Observe (`operate`)** | 5 + 2 console companions | **published**, every lab green on CRC |
| Security (`security`) | — | superseded, awaiting a replan |

The old Developer and Security tracks were moved to `workshops-monorepo/_superseded/`
(outside the helm globs, so no CRs are emitted). They remain as a content quarry.

## What needs you

1. **`git push`.** Commit `6f1d457` (OpenSSL ARM cap-probe skipped in every portal-image
   Job) is committed but **not pushed** — the push is the deploy trigger. Until it lands,
   the ArgoCD app `dcs-academy-tracks-and-workshops` stays OutOfSync and the new tracks'
   Workshop/ConsoleLab CRs are not on the cluster. Details below under *The sync blocker*.
2. **Rebuild and push the portal image.** Two learner-visible changes are in the image and
   not yet on the cluster: the **Optional** badge (and its numbering/trophy behaviour), and
   the catalog remembering which tracks were open. `images/build.sh dcs-academy-portal`.
3. **The ConsoleLink** ships with the next ArgoCD sync — nothing to do, just worth knowing it
   will appear in the console masthead.
4. **Durations** are authored estimates, not observed medians. Worth tuning after the first
   real cohort.

## The sync blocker (diagnosed and fixed, awaiting a push)

Symptom: both new tracks were complete and green in git, but `oc get workshops` showed no
`lab-b02`, `lab-b03`, `lab-b10` and none of the five `tour-*` CRs, and the Argo app sat
`OutOfSync` retrying.

Cause: the PostSync hook Job `dcs-academy-workshops-env-reconcile` died with **exit code
132 (SIGILL)**. That is the known Apple-Silicon CRC failure — OpenSSL's aarch64
capability probe crashes under Virtualization.framework. The portal *Deployment* has had
`OPENSSL_armcap=0` for a long time; the three other containers running the same image did
not: both env-guard hooks, the catalog-rescan Job and the session-reaper CronJob (whose
every run had also been failing, unnoticed, for the same reason).

Fix: the env var is now emitted in all of them, gated on `.Values.openssl.armcap`, which
`argocd/envs/platform-crc.yaml` already sets to `"0"` and every other cluster leaves empty
— a no-op off CRC. Verified by running `python3 -m portal.reap` in a one-off pod with the
env set: exit 0, full reconcile output.

## Things learned the hard way (do not re-derive)

- **A tenant may not read what governs them.** Not CRDs, not ClusterPolicies, not SCC objects.
  Labs read through *discovery* (`oc api-resources`, `oc explain`) and through *effects*
  (a refusal naming its rule), never by listing cluster-scoped objects.
- **The Educates session role grants far less than it looks.** No ServiceMonitors, no builds,
  no operator kinds, no routes in peer namespaces. Each lab that needs one grants it in
  `session.objects` — and the subject must be the **ServiceAccount in the workshop namespace**,
  because binding `system:serviceaccounts:<session ns>` matches nothing.
- **Educates' own SCC is not the platform's.** `educates-restricted` uses
  `runAsUser: MustRunAsNonRoot` where `restricted-v2` assigns a UID; the CloudNativePG operand
  cannot exec under it, in any namespace Educates manages.
- **A tenant can query their own metrics with no platform grant** — via the Thanos *tenancy*
  port (9092, `namespace` param), which authorizes on `get pods`. The public route is the
  cluster-wide port and does need a grant. The proxy **caches** decisions, so a refusal from
  before RBAC settles can linger.
- **`smoke_test.py` runs each grader exactly once.** Any check asserting an *eventual* state
  must wait — in the grader, or via a blocking step in the plan. This cost three labs a
  debugging round each.

## Suggested next work

1. **Alerts (o06)** — a `PrometheusRule` is a query with a threshold and a duration. Needs
   nothing o01 did not already teach, and completes the observability story.
2. **Revive the Security track** — and reconcile it with b03, which now owns all
   image-scanning teaching. Security keeps governance, provenance and classification.
3. **o02's LogQL section** becomes hands-on the moment a LokiStack is reachable.

## How to test a lab

```bash
cd test/workshops
export SMOKE_REGISTRY=ghcr.io/rummens          # CRC cannot reach the real Harbor
./smoke_test.py lab-b04-health-resources --throwaway --no-links
```
Always `--throwaway`: it creates its own `<lab>-mr-<ref>` Workshop instead of fighting the
ArgoCD-managed catalog CR. Content is pulled from `origin/main`, so **push before testing**.
