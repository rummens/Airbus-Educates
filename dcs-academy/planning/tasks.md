# Tasks

Task tracking for the DCS Academy. Priorities: **P1** (blocker), **P2** (important), **P3** (nice-to-have).

## Course-wide

- [ ] **P1** Confirm real values for the param trio: `dcs_registry` (Harbor project), `dcs_docs_base_url` (docs portal), and confirm `product_name`. Currently placeholders in `course-brief.md` / `resources.md`.
- [ ] **P1** Confirm the two base images (`dcs-workshop-base`, `dcs-tools`) exist / are built and mirrored in Harbor, with `oc` and required tooling.
- [ ] **P2** Confirm the DCS docs portal has (or will have) pages for the DCS concepts (`namespace-types`, `registry`, `tenancy-and-access`, `networking`, `storage`, `rbac`, `operators`).
- [x] **P2** Feedback capture (see `planning/feedback-capture.md`) — **BUILT (Option A+B)**: `feedback-collector` service (stdlib Python + SQLite on a PVC; CNPG swap seam via `DATABASE_URL`) storing both Likert ratings + comments; endpoints `/form`, `/feedback`, `/analytics` (portal webhook sink), token-gated `/admin`, `/metrics`, `/healthz`. Chart templates `60/61-feedback-*.yaml` + `values.feedback`; TrainingPortal `analytics.webhook.url` wired. Grafana dashboard `dcs-academy-platform/dashboards/feedback.json`. `98-your-feedback.md` on A01–A09 + authoring-skill template + review rubric. **Verified end-to-end on CRC** (form/POST/webhook/metrics/admin + persists across restart).
  - [ ] **P2** Make the `ghcr.io/rummens/feedback-collector` package **public** (first push is private → ImagePullBackOff otherwise), or set a pull secret via `global.registry.pullSecret`. Set `feedback.adminToken` (or `existingSecret`) in the prod values. Ensure user-workload monitoring is enabled for the ServiceMonitor. Import the Grafana dashboard.
- [ ] **P2** Choose the per-track sample applications (Developer, Security, Architect) — all images Harbor-mirrored.
- [ ] **P2** Validate vcluster is available/sized on DCS for the sessions that need the prod/dev model (A03).
- [ ] **P3** Run `scripts/collect-images.sh` once the first workshops exist and hand the manifest to the Harbor mirroring workflow.

## Tooling

- [x] **P2** `crc-local-testing/deploy_workshop.py` — deploy any workshop to CRC from git (portal-less). Verified green (A02 session Running).
- [x] **P2** `crc-local-testing/smoke_test.py` + `smoke-plans/*.json` — run setup + all examiner checks in the live session pod, with `--oc-shim`. Verified running; A02 = 6 pass / 9 fail (the 9 need the `hello-dcs` app image — unblocks with the image step).

## Module A — Foundations

- [x] **P1** Write per-workshop plans (Step 4) for A01–A06 in `workshop-plans/`. *(Done — 6 plans linked from course-module-a.md.)*
- [x] **P1** A04 auth resolved from customer docs: Harbor **robot accounts**. *(Remaining P2: per-session robot provisioning + target project.)*
- [ ] **P2** A03: confirm the technical mechanism DCS uses to mark DEV vs PROD namespaces (labels / CRD / request objects). Lifecycle + quick-comparison confirmed from customer docs; mechanism not in shared docs.
- [ ] **P2** Consider a dedicated **Network Policies** workshop if A06 runs past 60m (network policies added from customer docs).
- [ ] **P2** A04: add **`skopeo`** to `dcs-workshop-base` (no docker/podman in-container); **spike** whether the Harbor UI can be embedded as a session dashboard tab (auth/reverse-proxy) — fallback is `skopeo`/API output + screenshots.
- [ ] **P2** A06: provision a **PROD-type namespace** for the Route exercise; source a **pre-provisioned NetworkPolicy** to inspect (tenant self-create not yet available).
- [ ] **P2** A07: confirm real **storage-class names** for File + Block with the storage team (set `dcs_sc_file`/`dcs_sc_block`); confirm the S3-via-ITSM flow.
- [ ] **P1** Write per-workshop plans done for A07/A08/A09 (this session). Implement A07–A09 after A03–A06.
- [ ] **P2** A09/Module F: confirm a lightweight operator (CloudNativePG) can be pre-installed + operand images Harbor-mirrored for the hands-on CR.

## Module F — Operators / Platform Services

- [x] **P2** Module planned (`course-module-f.md`): F01 GitLab, F02 Argo CD, F03 CloudNativePG — operator model (platform owns operator, tenant owns instance). Prereq A09.
- [ ] **P2** Write per-workshop plans for F01–F03 after A09 is built; confirm each operator + operand images are mirrored and pre-installable.
- [ ] **P3** Fold newly-surfaced DCS topics into later tracks: costing/recharging + why-OpenShift (Architect D), data classification/RACI/security-exception (Security C), Helm charts (Developer).
- [ ] **P2** Produce the `hello-dcs` sample image (OpenShift-friendly, non-root) and a Harbor-mirrored base for A04's Containerfile.
- [ ] **P2** Produce the DCS architecture diagram asset for A01.
- [x] **P3** Implement A01 and A02 (with the authoring skill) — done, under `workshops/`. Validated (bash + YAML parse). Not yet run on a live cluster.
- [x] **P2** Rebuild A02 to the new content-depth standard (10 concept pages, one per page, what/why/how + expected output + flags; imperative/declarative, dry-run, ReplicaSet/Pod ownership, labels/selectors, querying, scaling+self-healing, logging, exec, Services/DNS). 9 examiner tests, all referenced.
- [ ] **P2** Depth pass on A01 (orientation — lighter by design, but review) and apply the content-depth standard when implementing A03–A06.
- [~] **P1** Live smoke test on local **kind** Educates (vanilla k8s) via a kubectl/public-image variant: both workshops deployed to the portal, environments Running, a real session started 1/1; **all A01 + A02 examiner tests pass**, manifests deploy, scaling/self-heal/logs/exec/service/in-cluster-curl all work. **Bug found + fixed**: `oc delete pod $(… -o name)` → `oc delete $(… -o name)` in A02 page 06. Remaining: (a) visual render check in a browser (auth-gated proxy blocked headless capture); (b) real **OpenShift/DCS** run — kind can't validate oc/Routes/SCC/vcluster or DCS images.
- [~] **P1** Real-OpenShift test on CRC (portal-less, kubectl/httpd variant): Workshop/Env/Session reconcile; session pod + dashboard/editor/console routes up; **httpd deploys under restricted SCC**; A02 examiner tests 8/9 PASS + scale/self-heal (fixed delete cmd)/challenge PASS. The 1 non-pass was the substitute image (`ubi9/httpd-24` returns 403 on `/`, empty docroot) not a workshop bug — real `hello-dcs` returns 200.
  - **Blocker found (content delivery):** the session's `vendir` x509-rejects CRC's registry cert (`image-registry…svc:5000` / route both self-signed) → workshop files don't download, dashboard content empty. Fix options: set Educates `caCertificateRef` to the service-ca/ingress CA (platform override), OR use a git source with trusted TLS, OR the real Harbor with a trusted cert. Ran the flow by `oc cp`-ing manifests+tests into the pod to bypass this.
- [ ] **P1** Real DCS flow still needs: build **`dcs-workshop-base`/`dcs-tools` with `oc`** (CRC base image has only kubectl) + push to a registry the session trusts; then run A01/A02 unmodified (oc) end-to-end incl. dashboard render.
- [x] **P1** Content delivery on CRC solved via **git source** (public repo) with the monorepo `newRootPath` + full-path `includePaths` pattern. Confirmed: A02 session pulls all 11 content pages + exercises into the pod. (Image/OCI delivery blocked by CRC self-signed registry cert.)
- [x] **P2** Rendering **CONFIRMED** on CRC (fresh pod after the config.yaml fix): `/workshop/content/*` pages return 200, `{{< param product_name >}}` → "Digital Container Service (DCS)", `product_short` DCS resolves, no leaked shortcodes, depth page 01-creating-resources renders. (The "Cannot GET /workshop/content/" was the stale live-patched pod; deleting it and re-pulling fixed config from git resolved it.)
- [ ] **P1** Push local commit `105abef` (the `oc delete` fix + vcluster rule) so the git source serves the corrected A02 (currently origin/main has the buggy delete command; render unaffected).
- [x] **P2** Implement A03–A09 (built under `workshops/`; static-validated + **live-tested on CRC** portless via `crc-local-testing/`). Live smoke results (examiner checks):
  - **A04 Harbor 5/5**, **A05 Access 11/11**, **A07 Storage 8/8** (incl. persistence across restart), **A08 RBAC 9/9** — all green.
  - **A03 Namespaces 9/11** — DEV path + namespace types green; the 2 Kyverno checks fail only because Kyverno isn't installed on CRC (real DCS PROD enforces it).
  - **A06 Networking 6/7** — deploy/Service/Route/NetworkPolicy-observe green; `egress-blocked` fails only because CRC has internet egress (real DCS is air-gapped).
  - **A09 Operators 1/5** — deploys/renders; CRD/CR checks fail only because the CloudNativePG operator isn't installed on CRC (screenshot fallback per plan).
  - **Findings fixed:** (a) **A06 real bug** — Educates' `educates-admin-session-role` excludes routes+networkpolicies, so a learner couldn't create the Route; added a Role+RoleBinding to A06 `session.objects` granting routes (manage) + networkpolicies (read). (b) **A07** — non-root container couldn't write the PVC; standard OpenShift restricted-v2 auto-assigns an in-range fsGroup (works on DCS), CRC's portless session SCC is RunAsAny (doesn't), so the CRC smoke patches fsGroup — workshop manifest left portable.
  - **Bonus:** `skopeo` is **already in `dcs-workshop-base`** (verify-skopeo passed) — the "add skopeo" task is done.
- [ ] **P3** For full A03/A09 live green on a lab cluster: install Kyverno (A03) and the CloudNativePG operator + mirrored operand images (A09). A07 File-RWX needs a real RWX storage class (CRC hostpath sufficed here). Confirm DCS session SCC assigns fsGroup (else add fsGroup to A07 manifest).

## Module B — Developer

- [x] **P2** Write per-workshop plans for B01–B06 — done (`workshop-plans/lab-b0*.md`), continuity with A0x checked.
- [x] **P2** Sample app decided: **hello-dcs** (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`), carried across B01–B05.
- [ ] **P2** Confirm a **Dev Spaces** instance can be pre-installed on DCS + the **UDI/dev images Harbor-mirrored** for B06; else deliver B06 as a screenshot-driven concept lab (plan supports both).
- [ ] **P2** Add a **`dcs_storage_class`** param placeholder (used by B05 `pvc.yaml`) to the workshop `config.yaml` param set when authoring.
- [ ] **P3** Author B01–B06 workshops from these plans (workshop-authoring skill), reusing the hello-dcs manifests progressively (config → probes → fault → PVC).

## Module C — Security & Compliance

- [x] **P1** Write per-workshop plans C01–C05 — done (`workshop-plans/lab-c0*.md`, 2026-07-13). All run in the native OpenShift session namespace (no vcluster); all reuse `samples/hello-dcs:1.0` + static fixtures (no new sample images).
- [~] **P1** Author C01–C05 from the plans (workshop-authoring skill) into `workshops-monorepo/tracks/security-track/`; new `security-track/track.yaml` (id `security`, order 30) added. Static authoring in progress this session; NOT yet live-smoke-tested.
- [ ] **P1** Live smoke test C01–C05 on CRC (portal-less, kubectl/httpd variant) once authored — mirror the A03–A09 pass. Expected env-specific non-passes: C01 gate is observe-only (no live scanner); C04 cosign verify modelled from fixture; C05 `verify-node-topology` tolerant (CRC lacks region labels).
- [ ] **P2** C01/C04 use **static scan/provenance fixtures** (`scan-report*.json`, `provenance.json`) because a live Harbor scanner + cosign trust policy aren't guaranteed reachable in-session. Wire live Harbor scan-API reads (C01) and real `cosign verify` (C04) once a scanner-backed Harbor + signed images + trust policy exist on the target cluster.
- [ ] **P2** C05 `workload-classified.yaml` is *read* (yq), not scheduled — region nodes may be absent on test clusters. Tighten `verify-node-topology` / add a real scheduling step once the target cluster exposes `topology.kubernetes.io/region` labels.
- [ ] **P3** Governance fixtures (data-classification matrix, RACI) in C05 are samples — align them to the real DCS governance docs when the docs portal is wired (`dcs_docs_base_url`).

## Modules D / E

- [ ] **P3** Plan after A + B + C are implemented and the format is proven.

---

# Restructure (2026-07-16): Core + Developer rework

Planning docs (`course-brief.md`, `course-topics.md`, `course-module-a.md`, `course-module-b.md`) rewritten to the new target design: lean quick-win Core, build/integration Developer track. The **built workshops still reflect the old design** — the work below closes the gap. See the old→new mapping tables in the module files.

> **Deploy impact (read before renaming):** renaming workshop directories changes `metadata.name` in every `resources/workshop.yaml`, the Track CRs (`tracks/*/track.yaml`), TrainingPortal workshop references, and session URLs. Existing deployments break on rename. Batch the renames, update all cross-references, and re-sync ArgoCD deliberately. `git mv` to preserve history.

## Module A — Core / Fundamentals restructure

- [x] **P1** A01: **built** (2026-07-16). Trimmed console tour → A08 (console app disabled, forward-pointer note added); added `02-dcs-clusters` (Sandbox/PROD cluster model), `03-containers-and-images`, `04-why-kubernetes-not-just-docker`; renamed session page → `05-your-session`; 4-Q knowledge check; 20m. Static-checked only — **not yet live-smoke-tested** on a cluster.
- [x] **P1** **ALL Core A labs BUILT (2026-07-16)** in `workshops-monorepo/tracks/core-track/`: A00 env-tour, A02 deploy-first-app, A03 configure-troubleshoot, A04 expose-app, A05 storage, A06 terms-namespaces-tenancy, A07 itsm-console *(rough)*, A08 openshift-console *(rough)* — plus A01 (earlier). hello-dcs image reworked (GREETING env + MODE=CLI/UI + /healthz, non-root UBI9-python multiarch, verified locally). `helm template` clean; examiner-per-command 1:1 (except A03 investigation page + A07 pure-tour). Static-checked only — **not yet live-smoke-tested** (no cluster in authoring env; push to origin/main then CRC portal-less). Old-design A0x labs still coexist → retire per restructure section below. See NEXT-SESSION.md for per-lab decisions/deviations.
- [ ] **P1** A02: build the quick-win lab — **merge old A02 (K8s essentials) + old B01 (deploy first app)** into `lab-a02-deploy-first-app`. Hybrid style: imperative (`oc create deployment`/`set env`/`expose` + curl + edit env + redeploy) then reveal the generated YAML. Preserve the validated old-A02 examiner coverage where it still applies.
- [ ] **P1** A03: new `lab-a03-configure-troubleshoot` — **fold old B02 (config/secrets) + old B04 (debugging/logs)**: ConfigMap/Secret rollout, then a pre-seeded fault the learner diagnoses (logs/events/describe) and fixes.
- [ ] **P1** A04: `lab-a04-expose-app` from old A06 — **expose properly**: real Route in a PROD-type namespace (DCS DNS/LB, reachable outside the session) **and** surface the app as a **new session dashboard tab**. Keep the routes Role+RoleBinding fix from old A06. Add the "Routes need PROD — see Developer B06" hook.
- [ ] **P1** A05: `lab-a05-storage` from old A07 (+ absorb old B05 stateful) — PVC, File vs Block, persistence across restart. **Author supplied the storage demo source: `workshop-plans/Lightning Talk Demo_ OpenShift Storage 101 v2 .docx`** — read it and fold into the A05 plan's TODO slot *before* building.
- [ ] **P1** A06: `lab-a06-terms-namespaces-tenancy` — **vocabulary only** from old A03 + A05 (Namespace/Tenant/DEV-PROD terms + what makes a namespace active). Deep model → B05/B06.
- [ ] **P2** A07: `lab-a07-itsm-console` — new; consolidate the ITSM self-service material (quota/mirroring/repos/S3/exceptions = ticket vs self-service). Likely screenshot-driven (air-gapped); spike embeddability.
- [ ] **P2** A08: `lab-a08-openshift-console` — the console tour split out of old A01, with `oc`↔console parity against the app deployed in A02 / exposed in A04. Deliver per [educates-openshift-console-limitation].
- [ ] **P2** Retire/redirect old built Core workshops no longer in Core: old A03 (→ B06), A04 (→ B04), A05 (→ B05), A08 (→ B05), A09 (→ B08). `git mv` + rewrite, don't delete blindly.
- [ ] **P2** Rewrite the per-workshop plans in `workshop-plans/` to match the new A01–A08 (currently `lab-a01…a09` reflect the old design).
- [ ] **P3** Confirm Core final count = 8 and the numbering (A01–A08) before renaming, to avoid a second rename pass.

## Module B — Developer restructure

- [ ] **P1** B01: new `lab-b01-docker-to-k8s` (Intermediate) — compose/`docker run` → Deployment/Service/ConfigMap; what doesn't translate on DCS (SCC/non-root, Harbor, no `latest`).
- [ ] **P1** B02: new `lab-b02-image-buildconfigs` — git as build source; BuildConfig (S2I/Dockerfile) → image in Harbor → deploy → rebuild.
- [ ] **P1** B03: `lab-b03-dev-spaces` from old B06 — git as in-cluster IDE (devfile); Harbor-mirrored UDI.
- [ ] **P1** B04: `lab-b04-harbor-scanning` — old A04 (Harbor) **+ all image-scanning merged here**. Read the scan, pass the gate, push the B02 image.
- [ ] **P1** B05: `lab-b05-rbac-tenancy` — consolidate old A05 (access/tenancy) + old A08 (RBAC deep dive).
- [ ] **P1** B06: **new** `lab-b06-dev-prod-namespaces` (the missing lab) — DEV vs PROD by policy posture: PROD = harsher Kyverno + **can** create Routes; DEV = looser + **cannot** create Routes; promotion. Uses **vcluster** (deep model from old A03). Kyverno required to demo enforcement (screenshot fallback).
- [ ] **P2** B07: `lab-b07-scaling-health` from old B03.
- [ ] **P2** B08: `lab-b08-operators` from old A09 (Advanced) — keep as Module F prerequisite.
- [ ] **P2** Write/rewrite per-workshop plans for B01–B08 (B01/B02/B06 are new; the rest are moves).
- [ ] **P2** Update the sample-app note: `hello-dcs` still carried; build labs (B02/B03) also use the learner's own / a provided git repo — confirm a Harbor-mirrorable buildable source repo exists.
- [ ] **P3** Update Module F prereq references: A09 → **B08** in `course-module-f.md` and `course-brief.md` (brief done).
- [ ] **P1** B02/B04 need a **session-scoped, push-capable Harbor project + robot account** (B02 builds→pushes; B04 pushes the built image). Riskiest new provisioning dependency — B04 degrades to inspect-only, but **B02 has no clean fallback** for build-and-push. Confirm before authoring.
- [ ] **P2** B02 needs an **air-gapped-reachable git build source** + S2I builder image (mirrored GitLab vs an in-cluster seeded git repo). Unresolved.
- [ ] **P2** Confirm the **hello-dcs env var name** the sample reads for the A02 "customise with `oc set env`" step (plans assumed a `GREETING`-style var). Drives A02 + A03 config steps.
- [ ] **P2** Produce screenshot assets: **A07** (ITSM console request flow) + **A08** (OpenShift console Route/PVC/Topology views) — both screenshot-driven since neither embeds cleanly in an air-gapped session.
- [ ] **P3** Confirm DCS docs paths used across the new plans resolve on the real portal (`/concepts/*`, `/services/*`, `/getting-started/requests`).
- [x] **P3** 14 old per-workshop plans **archived** to `workshop-plans/_superseded-old-design/` (git mv, history preserved) with a README explaining the supersession — kept as refactor reference; delete once the built workshops are migrated.

## Follow-ups from 2026-07-16 review (queued — details not yet authored, author still reviewing)

- [x] **P1** **Lab A00 — Workshop environment tour** — **PLAN + BUILT** (2026-07-16) in `workshops-monorepo/tracks/core-track/lab-a00-environment-tour/` (7 pages: layout+SVG, split terminal w/ 2 examiner-checked `oc` cmds, editor, k8s-Dashboard Console tab, feedback, summary+3Q). order `5` (before A01), lifecycle `dev`, console enabled (+token), vcluster false. helm renders clean; static-checked only (no live cluster in authoring env). (NEW, ~5m→10m, first in Core): tour the *workshop session UI* — the split terminals, the **Kubernetes Dashboard console tab (NOT the OpenShift web console)**, the VS Code editor, and the feedback mechanism. Reference `docs/dcs-academy/environment-guide.md` + `docs/dcs-academy/img/dashboard-layout.svg`. **Number it `A00`** (not a renumber of A01–A08) to avoid a second rename pass. Distinct from A08 (which tours the real OpenShift web console) — A00 is the session chrome + k8s Dashboard.
- [ ] **P1** **Rework the `hello-dcs` sample image** (`images/hello-dcs/`) to serve the new Core arc:
  - Read customisation from **env vars** so A02's `oc set env` step visibly changes the response (confirms the `GREETING`-style var name and wires it end to end).
  - Add a **`MODE` flag: CLI vs UI**. **CLI** = plain-text response (basic, unformatted) for the `curl` steps in A02. **UI** = fancier HTML for when the app is exposed via a Route (A04), and in UI mode **print the app's own Route host/URL into the rendered page** so learners see the DCS DNS/Route format live.
  - Keep non-root / Harbor-mirrorable / multiarch. Update the A02/A03/A04 plans to reference the flag once the image is reworked.
- [ ] **P2** **Promote general rules into the authoring skill** (proposed — confirm before editing `airbus-educates-workshop-authoring-skill/references/`):
  - `openshift-reference.md` / `air-gapped-images-reference.md`: mandate `envsubst < f.yaml | oc apply -f -` for any manifest carrying a `${VAR}` (registry/host) — this is the recurring ImagePullBackOff bug, a house correctness rule, not course-specific.
  - A delivery note (dashboard/console references): when a component can't embed in an air-gapped session (OpenShift console, ITSM console), deliver as an annotated screenshot-driven tour with a knowledge-check checkpoint. (Ties to [educates-openshift-console-limitation].)
  - `dcs-concepts-reference.md`: record the **DEV/PROD Route-capability fact** (PROD = Kyverno-enforced + can create Routes; DEV = looser + cannot) as a first-class DCS concept.
  - `dcs-concepts-reference.md`: add the **DCS cluster model** (Sandbox vs PROD — identical except feature-rollout timing DEV/QA→Sandbox→PROD monthly, Sandbox 1 month ahead, + maintenance-notice/SLA) as a new concept with a doc path. A01 currently links `{{< param dcs_docs_base_url >}}/concepts/clusters` (assumed); the existing ref lists shared-vs-dedicated at `/clusters/types` — reconcile the path.
  - **Keep course-pedagogy** (quick-win-first, theory-folded-into-labs) in `course-brief.md`, not the authoring skill — it's a course design choice; optionally cross-reference it as an available style in `content-depth-reference.md`.

## Security track scanning overlap

- [ ] **P2** Per the 2026-07-16 decision, **all image-scanning teaching consolidates in Developer B04**. Built Security workshops **C01 (image-scanning)** and **C04 (supply-chain)** now overlap. Reconcile when the Security track is next revised: keep C's **governance/policy/provenance** angle (cosign trust, data classification, supply-chain), move the developer-facing "read the scan / pass the gate" flow to B04, and remove the duplication. Do **not** edit C now — out of scope for this rework.

## Known pre-existing bug (carry forward)

- [ ] **P1** `${DCS_REGISTRY}` manifests applied with plain `oc apply` (no `envsubst`) in old A04/A06/A09 → real learners hit ImagePullBackOff (CRC smoke masked it). Correct pattern: `envsubst < f.yaml | oc apply -f -` (as in validated A02). Fix as these labs are refactored/moved (A06→A04, A04→B04, A09→B08).
