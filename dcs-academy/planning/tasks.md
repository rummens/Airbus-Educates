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
