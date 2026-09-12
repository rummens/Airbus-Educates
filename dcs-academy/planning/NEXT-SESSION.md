# DCS Academy — Session Handoff

**Last updated:** 2026-09-12. Read this first, then
[tasks.md](tasks.md).

## Where things stand

**Two new tracks are built, live-verified and published.**

| Track | Labs | State |
|---|---|---|
| Core (`core`) | 8 | unchanged — frozen baseline |
| Console (`console`) | 9 | unchanged — frozen baseline |
| **Build & Run (`build`)** | 10 + 3 console companions | **published**; terminal labs green on CRC, console companions rebuilt 2026-09-12 |
| **Operate & Observe (`operate`)** | 5 + 2 console companions | **published**; terminal labs green on CRC, console companions rebuilt 2026-09-12 |
| Security (`security`) | — | superseded, awaiting a replan |

The old Developer and Security tracks were moved to `workshops-monorepo/_superseded/`
(outside the helm globs, so no CRs are emitted). They remain as a content quarry.

## What needs you

1. **`git push`.** Everything below is committed and unpushed. The push is the deploy trigger.
2. **Re-verify on a cluster.** CRC was stopped part-way through this session, so three things
   are written and gate-checked but **not live-verified**:
   - **b03 page 03** (Harbor project via Crossplane) and its `verify-project-requested` check.
     The no-provider branch is the one that will run on CRC.
   - **tour-b04-health**'s paired workshop, which now also creates a bare Pod `lab-probe`
     whose readiness probe points at a closed port. The tour reads its Conditions.
   - **tour-b02 / b05 / o01 / o02** after their last edits. b04, b02, b05 and o02 were walked
     end to end before CRC stopped; o01 was re-edited afterwards.
   `cd test/workshops && ./smoke_test.py lab-b03-harbor` covers the first one.
3. **Clean up the probe leftovers** when CRC comes back. This session created scratch
   namespaces `probe-b02`, `probe-b04`, `probe-b05`, `probe-o01`, `probe-o02` and five
   ConsoleLabs named `zz-*`, none of which are in git:
   `oc delete ns probe-b02 probe-b04 probe-b05 probe-o01 probe-o02` and
   `oc get consolelabs -o name | grep zz- | xargs -r oc delete`.
4. **Rebuild and push the portal image** if the Optional badge and the remembered track state
   are not visible: `images/build.sh dcs-academy-portal`, then restart the portal Deployment
   (`pullPolicy: Always` does not re-pull without one).

## How the console labs are verified

The engine resolves an `href` target with `document.querySelector('a[href="…"]')`, so a step
whose value is not the exact URL the console renders highlights nothing, silently. Two forms
are in play on OpenShift 4.22:

- **sidebar links and details-page tabs** use the GVK path
  (`/k8s/ns/<ns>/core~v1~ResourceQuota`, `/k8s/ns/<ns>/deployments/lab-app/yaml`);
- **table rows** use the legacy plural (`/k8s/ns/<ns>/resourcequotas/compute-resources`).

The nav section ids are `qs-nav-home`, `qs-nav-workloads`, `qs-nav-networking`,
`qs-nav-storage`, `qs-nav-builds`, `qs-nav-monitoring` (labelled **Observe**),
`qs-nav-compute`, `qs-nav-usermanagement`, `qs-nav-administration`. There is no
`qs-nav-observe`.

To check a lab, apply it under a scratch name, create a namespace holding the objects its
paired workshop provisions, and walk it with Playwright from the console-plugin repo
(`tests/e2e`, `CONSOLE_URL` + `CONSOLE_PASSWORD`), asserting `.academy-guidance__spotlight` is
visible on each step before pressing Continue. That harness is what found the breakage.

## The sync blocker (fixed and deployed on 2026-09-12)

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
`argocd/envs/platform-crc.yaml` already sets to `"0"` and every other cluster leaves empty,
so it is a no-op off CRC. After the push, the app synced, all 20 new Workshop CRs and 5
ConsoleLabs reached the cluster, and a manual run of the session-reaper CronJob succeeded
(`our_envs=35 desired_workshops=35 stale=0`).

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
