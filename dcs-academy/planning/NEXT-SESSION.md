# DCS Academy — Session Handoff (Core + Dev rework)

**Last updated:** 2026-07-16. Read this first when resuming, then `planning/tasks.md` for the full task list.

## LATEST (2026-07-16 build session): all Core Module A labs BUILT

All A00–A08 now exist under `workshops-monorepo/tracks/core-track/` (static-checked; `helm template` clean; NOT live-tested — no cluster in authoring env). Built this session: **A00** (env tour), **A06** (2-NS isolation), **A02** (deploy, hybrid), **A03** (config+troubleshoot), **A04** (expose/Route), **A05** (storage), **A07**+**A08** (rough tours). **A01** was built earlier. Old-design labs (`lab-a02-kubernetes-essentials`, `lab-a03-namespace-model`, `lab-a04-harbor-registry`, `lab-a06-networking`, `lab-a07-storage`, `lab-a08-rbac-deep-dive`, `lab-a09-operators`) still coexist in the tree — the new labs are additive (new names/orders 5–80); the old ones need retiring/`git mv` per the tasks.md restructure section.

**hello-dcs image reworked** (`images/hello-dcs/`): dependency-free stdlib server, `GREETING` env var (confirmed the name), `MODE=CLI|UI` (CLI plain text; UI HTML that prints its own Route URL from the request Host header), `/healthz`, non-root, UBI9-python multiarch. Verified locally; container build/push (build.sh, multiarch) is the user's step.

**Key build decisions / deviations from plans:**
- **A04:** made the **session namespace itself PROD-type** via `dcs.airbus.com/lifecycle: prod` (the documented mechanism) instead of provisioning a *separate* PROD namespace — a Route can't point at a Service in another namespace, so app+Service+Route all live in the (prod-typed) session ns. Reused old A06's routes Role+RoleBinding + NetworkPolicy + `ingresses: app` session block.
- **A06:** two peer namespaces via Educates **`session.objects`** (Namespace + RoleBinding, operator-created) — no learner-SA namespace-create right needed, so the plan's provisioning risk is moot.
- **A02/A03/A04/A05:** no `session.objects` app pre-deploy (sessions are independent + avoids hardcoding the registry in workshop.yaml); the learner applies the app on page 1. `${DCS_REGISTRY}` manifests all use `envsubst < f | oc apply -f -`.
- **A05:** folded the author's Flask-counter storage demo's *arc* onto hello-dcs (marker file) — the Flask app wasn't imported (air-gapped/no-new-image). PVCs omit `storageClassName` (bind to cluster default → testable anywhere); SC selection taught conceptually + `dcs_sc_file`/`dcs_sc_block` params.
- **A07/A08 = rough** (marked in README + workshop.yaml annotation): screenshot placeholders, console-tour approach still open.
- Examiner-per-command honoured 1:1 everywhere except A03 page 05 (3 read-only diagnosis commands share one verify — the plan's sanctioned investigation page) and A07 (pure tour, 0 commands, knowledge-check reveals).

**Next:** retire old-design A0x labs; the queued authoring-skill rule additions (envsubst, screenshot-fallback, DEV/PROD + cluster concepts); then Module B.

## CRC smoke-test results (2026-07-16, commits 374572b + ac18b3a pushed)

Ran all Core A labs on CRC (portal-less `test/workshops/smoke_test.py`, git source origin/main). Wrote 8 smoke-plans (`test/workshops/smoke-plans/lab-a0*.json`). **Image-independent labs GREEN:** A00 2/2 · A04 10/10 (egress XFAIL — CRC has internet) · A05 12/12 · A06 11/11 · A08 6/6 · A07 n/a (content tour). **A02 9/11, A03 11/16** — remaining fails are ONLY the **stale hello-dcs image** (ghcr still serves pre-rework nginx; greeting/config checks can't pass). A03 `deployment-configured` confirmed deploys 1/1 in 6s (manifest sound).

**BLOCKER for A02/A03 green:** rebuild+push `hello-dcs` via `images/build.sh` (multiarch) — reworked GREETING/MODE image not on ghcr yet. Then re-run A02 → 11/11, A03 → 9/9.

**Harness fixes (pushed):** `deploy_workshop.py` now merges authored `session.objects`/`ingresses` (A04/A06 needed it) + waits for env deletion before recreate (Pending-flake fix); `smoke_test.py` 600s wait. Examiner hardening: dropped restricted-SA-forbidden `oc get all`/cluster reads (A02/A06/A08), in-app greeting fetch (A02), rolling-update-safe verify-not-ready (A03), WaitForFirstConsumer-tolerant verify-block-bound (A05). A05 content: deploy consumer before asserting PVC Bound (cross-cluster fix). CRC runs need ArgoCD auto-sync OFF on `dcs-academy-tracks-and-workshops` during the run, re-enabled after (done).

## Where we are

Reworking **Module A (Core / Fundamentals)** and **Module B (Developer)** from an interview redesign. Planning docs rewritten; per-workshop plans rewritten; **implementation of Module A in progress, one lab at a time**.

- **Design locked** (see `course-brief.md`): Core = lean quick-win happy path, theory folded into labs, teaches *terms*; Developer track teaches *mechanisms*.
- **Core A = 8 labs** (target): A01 what-is-dcs · A02 deploy-first-app *(quick win)* · A03 configure-troubleshoot · A04 expose-app *(real Route + session tab)* · A05 storage · A06 terms-namespaces-tenancy *(active 2-NS isolation)* · A07 itsm-console · A08 openshift-console. **Plus A00** (environment tour, ~5m) queued — not yet planned/built. Number it `A00` to avoid renumbering.
- **Dev B = 8 labs** (target, plans written, NOT built): B01 docker-to-k8s · B02 buildconfigs · B03 dev-spaces · B04 harbor-scanning *(all scanning here)* · B05 rbac-tenancy · B06 dev-prod-namespaces *(new)* · B07 scaling-health · B08 operators.

## Done

- All planning docs rewritten: `course-brief.md`, `course-topics.md`, `course-module-a.md`, `course-module-b.md`, `tasks.md`.
- **16 per-workshop plans** written in `workshop-plans/` (A01–A08, B01–B08). 14 old plans archived to `workshop-plans/_superseded-old-design/`.
- Plan refinements folded in: **A01** = DCS cluster model (Sandbox/PROD); **A06** = active two-namespace isolation demo + why-split reasons.
- **A01 BUILT** in `workshops-monorepo/tracks/core-track/lab-a01-what-is-dcs/` (static-checked, not live-tested). Console removed → A08.

## Next steps (in order, one lab per turn)

1. **A00** — write its plan (`workshop-plans/lab-a00-environment-tour.md`), then build. 5m tour of the workshop UI: split terminals, the **Kubernetes Dashboard console tab (NOT OpenShift console)**, editor, feedback widget. Reference `docs/dcs-academy/environment-guide.md` + `docs/dcs-academy/img/dashboard-layout.svg`.
2. **A06** — build (plan ready, active 2-NS). Needs Educates to pre-provision two namespaces via `session.objects` + RoleBindings; validate session SA can create namespaces on the target cluster (fallback in plan).
3. **hello-dcs image rework** (`images/hello-dcs/`) — BLOCKS A02/A03/A04. Reads customisation from **env vars** (confirm var name, plan assumes `GREETING`); add **`MODE` flag: CLI** (plain text for `curl`) **vs UI** (HTML + prints its own Route host/URL into the page). Non-root, Harbor-mirrorable, multiarch.
4. **A02 → A03 → A04** — build (depend on the reworked image + its env-var/MODE contract).
5. **A05** — build from the storage demo the author supplied: `workshop-plans/Lightning Talk Demo_ OpenShift Storage 101 v2 .docx` (read it, fold into the A05 plan's TODO slot first).
6. **A07, A08** — **rough content only** (author still deciding how to do the console tour nicely).
7. After Module A labs: remaining Module A tasks (see `tasks.md`) + the authoring-skill rule additions (envsubst pattern, screenshot-fallback, DEV/PROD + cluster concepts).

## Key gotchas / rules (don't re-learn)

- **All A/B built workshops still reflect the OLD design** (`workshops-monorepo/tracks/core-track|dev-track/lab-*`). The rework redraws them; renames carry **deploy impact** (workshop.yaml `metadata.name`, Track CRs, TrainingPortal, URLs). `git mv`, batch, re-sync ArgoCD deliberately.
- **envsubst bug:** apply `${DCS_REGISTRY}`/`${VAR}` manifests with `envsubst < f.yaml | oc apply -f -`, never plain `oc apply` (old A04/A06/A09 have this bug → ImagePullBackOff).
- **Security scanning** now consolidated in Dev **B04**; overlaps built Security C01/C04 — reconcile later, C out of this rework's scope.
- **Console distinction:** A00 = k8s Dashboard (session tab); A08 = real OpenShift web console (embedding-limited, see `[educates-openshift-console-limitation]` memory).
- Use the **airbus-educates-workshop-authoring** skill (`airbus-educates-workshop-authoring-skill/SKILL.md`) to build; **airbus-educates-course-design** to touch plans.
- No live cluster in the authoring env — static-check only; deploy to CRC via `test/workshops/` to smoke-test (portal-less, push to origin/main first).

## File map

- This handoff: `dcs-academy/planning/NEXT-SESSION.md`
- Tasks: `dcs-academy/planning/tasks.md` (restructure sections near the bottom)
- Plans: `dcs-academy/planning/workshop-plans/lab-{a,b}0N-*.md`
- Built workshops: `workshops-monorepo/tracks/core-track|dev-track/lab-*/`
- Storage source: `dcs-academy/planning/workshop-plans/Lightning Talk Demo_ OpenShift Storage 101 v2 .docx`
