# Workshop Plan: lab-b04-harbor-scanning

## 1. Workshop Metadata

- **Name:** `lab-b04-harbor-scanning`
- **Title:** Harbor & Image Scanning
- **Description:** Where your images live and what guards them — navigate DCS Harbor catalogs and robot accounts, pull/inspect with `skopeo`, push the image you built in B02, read a vulnerability/compliance scan report and understand the scan gate, remediate a finding, and know how mirroring/quota happen via ITSM.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B02 (Building Images with BuildConfigs)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (read the scan-report JSON / manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- **vcluster decision:** `false` — native OpenShift session namespace. All work is `skopeo`/`jq`/`oc` against Harbor + local fixtures; no cluster-scoped objects. `budget: medium`.
- Workshop image: **`dcs-workshop-base`** — image work is **`skopeo`** (daemonless) + `jq`; **no `docker`/`podman`** inside the container. `skopeo` is already in `dcs-workshop-base`.
- Registry auth: a read-only Harbor **robot account** for pull/inspect (provided via `REGISTRY_*` env / mounted secret); the **push** step reuses the push-capable credential from B02's session-scoped project (see Design Notes).
- Harbor UI: attempt to embed the Harbor registry UI as a dashboard tab so learners browse projects, tags, and scan results visually (feasibility flagged — see Design Notes).
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.
- **Scan reports:** live scan-API read **if** a scanner-backed Harbor is reachable in-session, **else** a static fixture shipped in `exercises/` (both paths documented — see Design Notes).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Navigate DCS Harbor catalogs (DCS Catalogs / Allowed External Registries / Proxy-Cached Catalog) and explain robot accounts.
- Pull and inspect an image with `skopeo` using a read-only robot account.
- Push the image built in B02 to Harbor.
- Distinguish **vulnerability** scanning from **compliance** scanning, and read a scan report (severities, CVE IDs, fixed-in versions) with `jq`.
- Explain what a **scan gate** does (blocks pull/deploy above a severity threshold) and its per-image / per-project scope.
- Remediate a flagged image (patched tag / rebuild on a patched base) and confirm the replacement passes.
- Explain how mirroring and quota increases happen via **ITSM**.

## 4. Connection to Previous Workshop

**Already known (from B01/B02):** the Harbor-only / air-gapped image posture and no-`latest` rule (B01); building an image on-cluster and pushing it to `{{< param dcs_registry >}}` (B02).

**New here:** Harbor itself — catalogs, robot accounts, `skopeo inspect`/pull; the *content* of a scan report; the vuln-vs-compliance distinction; the gate and its thresholds; remediation; and the mirroring/quota-via-ITSM model.

**Do NOT re-teach:** how the image got built (B02) — the push here reuses B02's artifact; deploy/Service basics (A02) — reference only when a manifest references a Harbor image.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder + note on live-scan vs fixture delivery.
- `exercises/pod-from-catalog.yaml` — a Pod/Deployment referencing a catalog image by digest, to show a catalog pull landing on the cluster (`${DCS_REGISTRY}` ref).
- `exercises/scan-report.json` — a clean-ish Harbor/Trivy-style report for `hello-dcs:1.0`: a vulnerabilities array (Low/Medium) + a summary severity-count block, structured for `jq`. Used when a live scanner is not reachable.
- `exercises/scan-report-flagged.json` — same schema, 2 Critical + several High findings (each with a `FixedVersion`) — the image the gate would block.
- `exercises/deploy-flagged.yaml` — a Deployment referencing a would-be-blocked tag, used to *narrate* the gate blocking a pull (observe/concept; not asserted to fail on a scanner-less cluster).

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note. DCS blurb: **Harbor registry** + scan gates → `{{< param dcs_docs_base_url >}}/services/registry`. Frame: "Where do my images live and what guards them?"
- **`01-catalogs-and-robots.md`** — concept. Air-gapped → a single trusted registry. **Catalogs**: DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog (+ its PROD restriction). Projects, robot accounts (pull vs push), that Harbor also stores Helm charts. Upstream: [OCI images](https://kubernetes.io/docs/concepts/containers/images/), [Harbor](https://goharbor.io/docs/); DCS specifics → DCS docs. No command → no examiner.
- **`02-inspect-and-pull.md`** — `skopeo inspect docker://{{< param dcs_registry >}}/samples/hello-dcs:1.0` (read-only robot) → check: manifest/digest returned. `envsubst < pod-from-catalog.yaml | oc apply -f -` → polling check: pod running from the catalog pull. Explain why `skopeo` (daemonless, no docker/podman) and read-only pull.
- **`03-push-your-image.md`** — push the **B02-built** image to its Harbor project with `skopeo copy` (using the push-capable credential). Verify it landed: `skopeo inspect` the pushed ref. Check: pushed tag/digest present in Harbor. Contrast pull-only robot vs push-capable robot.
- **`04-read-a-scan-report.md`** — the scanning core. Vulnerability (CVEs in layers) vs compliance (policy/config) scanning; per-image / per-project scope. `editor:open-file` `scan-report.json`; `jq '.summary.severityCount' scan-report.json` → examiner `verify-report-summary` (non-empty count object); `jq -r '.vulnerabilities[] | "\(.severity)\t\(.id)\t\(.package)"' scan-report.json` → examiner `verify-report-cves` (≥1 CVE line). Upstream: [Trivy](https://trivy.dev/), [CVE](https://www.cve.org/); DCS gate → DCS docs. *(Live path: swap the fixture for a Harbor scan-API read when reachable.)*
- **`05-the-gate.md`** — `editor:open-file` `scan-report-flagged.json`; `jq '[.vulnerabilities[]|select(.severity=="Critical")]|length' scan-report-flagged.json` → examiner `verify-flagged-criticals` (≥1) — *why* the gate trips. Open `deploy-flagged.yaml`; narrate that applying it is blocked at pull time (`ImagePullBackOff`); `{{< note >}}` observe/concept (no live-scanner assertion). Concept: gate threshold (block ≥ High), per-project override.
- **`06-remediation-and-itsm.md`** — remediate: pick a **patched tag** or **rebuild on a patched base** (ties back to B02), re-scan. `skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0` → examiner `verify-clean-image` (digest returned); `jq '.summary.severityCount.Critical // 0' scan-report.json` → examiner `verify-no-criticals` (0). Concept: **mirroring** an external image = an ITSM request (External→Harbor / Harbor→Harbor); **quota** increases = ITSM; the **Security Exception Process** as the escape hatch when a fix isn't yet available. DCS docs links.
- **`98-your-feedback.md`** — standard feedback page (workshop=lab-b04-harbor-scanning).
- **`99-workshop-summary.md`** — recap catalogs/robots/`skopeo`/push/scan/gate/remediate/ITSM. **Check Your Understanding** (4 Q): why a single registry; vuln vs compliance; what a gate does + threshold; two remediation paths + the exception process. A final examiner (repeat `verify-report-summary`-style) as the knowledge-check action.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. Commands are `skopeo`/`jq`/`oc` against remote refs or local fixtures — no `cd`.
- **Carry-forward bug:** every `${DCS_REGISTRY}` manifest applied via `envsubst < file.yaml | oc apply -f -`, never plain `oc apply`.
- Dashboard-tab focus: after the Harbor UI tab is shown, any later `terminal:execute` switches focus back to Terminal — guide the learner back to the Harbor tab when needed.

## 8. Design Notes

- Covers **course-topics ideas 4 (Harbor) + 12 (scanning)**. **Merged source:** old A04 (Working with Harbor) + **all image-scanning teaching** consolidated here per the 2026-07-16 decision (pulled from the built Security C01).
- **Overlap note:** this now overlaps built Security **C01** (image-scanning) and **C04** (supply-chain). **Security keeps the governance / policy / provenance angle; the developer-facing "read the scan, pass the gate" flow lives here.** Reconcile when the Security track is next revised — tracked in [tasks.md](tasks.md#security-track-scanning-overlap).
- **Live scan vs fixture:** prefer a live Harbor scan-API read when a scanner-backed Harbor is reachable in-session; otherwise ship the static `scan-report*.json` fixtures so every step stays examiner-verifiable and deterministic air-gapped. Both paths documented; the page flow is identical.
- **No double-virtualization:** all image work uses `skopeo` (daemonless, already in `dcs-workshop-base`); no `docker`/`podman`. Drop `dcs-tools` — runs on `dcs-workshop-base`.
- **Push credential:** the push step depends on B02's session-scoped Harbor project + push-capable robot; if unavailable, degrade `03-push-your-image.md` to a narrated/inspect-only concept (pull-only robot), same as A04's original pull-only posture. Flag in `tasks.md`.
- **Harbor UI embedding (open question → validate):** embed the Harbor UI as a dashboard tab; feasibility depends on Harbor auth (SSO/robot) + reverse-proxy through the session. Fallback: `skopeo`/`jq` output + annotated screenshots.
- **No new sample image:** clean case = `samples/hello-dcs:1.0` (proven); flagged case = a report *fixture* + a narrated (non-asserted) blocked deploy — avoids inventing an untestable vulnerable image.
