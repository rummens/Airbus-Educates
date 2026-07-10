# Tasks

Task tracking for the DCS Academy. Priorities: **P1** (blocker), **P2** (important), **P3** (nice-to-have).

## Course-wide

- [ ] **P1** Confirm real values for the param trio: `dcs_registry` (Harbor project), `dcs_docs_base_url` (docs portal), and confirm `product_name`. Currently placeholders in `course-brief.md` / `resources.md`.
- [ ] **P1** Confirm the two base images (`dcs-workshop-base`, `dcs-tools`) exist / are built and mirrored in Harbor, with `oc` and required tooling.
- [ ] **P2** Confirm the DCS docs portal has (or will have) pages for the four DCS concepts (`namespace-types`, `registry`, `tenancy-and-access`, `networking`).
- [ ] **P2** Choose the per-track sample applications (Developer, Security, Architect) — all images Harbor-mirrored.
- [ ] **P2** Validate vcluster is available/sized on DCS for the sessions that need the prod/dev model (A03).
- [ ] **P3** Run `scripts/collect-images.sh` once the first workshops exist and hand the manifest to the Harbor mirroring workflow.

## Module A — Foundations

- [x] **P1** Write per-workshop plans (Step 4) for A01–A06 in `workshop-plans/`. *(Done — 6 plans linked from course-module-a.md.)*
- [x] **P1** A04 auth resolved from customer docs: Harbor **robot accounts**. *(Remaining P2: per-session robot provisioning + target project.)*
- [ ] **P2** A03: confirm the technical mechanism DCS uses to mark DEV vs PROD namespaces (labels / CRD / request objects). Lifecycle + quick-comparison confirmed from customer docs; mechanism not in shared docs.
- [ ] **P2** Consider a dedicated **Network Policies** workshop if A06 runs past 60m (network policies added from customer docs).
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
- [ ] **P2** Verify dashboard **rendering** (markdown + `{{< param >}}`) in a **browser** — headless curl blocked by the dashboard SPA/auth gateway. Session live at https://lab-a02-kubernetes-essentials-01.apps-crc.testing (basic auth educates/educates).
- [ ] **P1** Push local commit `105abef` (the `oc delete` fix + vcluster rule) so the git source serves the corrected A02 (currently origin/main has the buggy delete command; render unaffected).
- [ ] **P2** Implement A03–A06 once A01/A02 pass live.

## Module B — Developer

- [ ] **P2** Write per-workshop plans for B01–B05 after Foundations plans are done (read A0x plans first for continuity).

## Modules C / D / E

- [ ] **P3** Plan after A + B are implemented and the format is proven.
