# Workshop Plan: lab-c01-image-scanning

## 1. Workshop Metadata

- **Name:** `lab-c01-image-scanning`
- **Title:** Image Scanning & Harbor Gates
- **Description:** Read Harbor vulnerability and compliance scan results, understand the gate policy that blocks unsafe images, and remediate a flagged image on air-gapped DCS.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module C — Security & Compliance)
- **Prerequisites:** A04 (Working with Harbor). Assumes `skopeo`, catalogs, robot accounts, and the *idea* of a scan gate (introduced at "read the result" depth in A04).
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- Console: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Run location: **native OpenShift session namespace** (vcluster `enabled: false`). No cluster-admin/CRD ops — same posture as A04. `budget: medium`.
- Workshop image: **`dcs-workshop-base`** — image work is `skopeo` (daemonless) + `jq`; no docker/podman.
- Registry auth: read-only Harbor **robot account** provided to the session (same as A04); `skopeo` needs no `login`.
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.
- **Scan reports are static fixtures** shipped in `exercises/` (a Harbor/Trivy-style report JSON). Rationale in Design Notes — a live Harbor scanner is not guaranteed reachable/deterministic in-session, and fixtures make every step examiner-verifiable air-gapped.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Distinguish **vulnerability scanning** from **compliance scanning**, and explain per-image / per-project / global scan scope on DCS.
- Read a Harbor scan report — severities (Critical/High/Medium/Low), CVE IDs, fixed-in versions — and summarise the risk with `jq`.
- Explain what a **scan gate** does (blocks pull/deploy above a severity threshold) and where it sits in the pull path.
- Remediate a flagged image (pick a patched tag / rebuild on a patched base) and confirm the replacement passes.
- Explain the **Security Exception Process** (ITSM) as the escape hatch when a finding can't be fixed immediately.

## 4. Connection to Previous Workshop

**Already known (from A04):** catalogs, robot accounts (read-only pull), `skopeo inspect`, digests vs tags, that a gate can block an image. **New here:** reading the *content* of a scan report, the vuln-vs-compliance distinction, gate thresholds, and remediation. **Do NOT re-teach:** what Harbor is, catalogs, or why the platform is air-gapped — reference as established.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/scan-report.json` — a clean-ish Harbor/Trivy-style report for `hello-dcs:1.0`: a `Vulnerabilities` array with a handful of Low/Medium entries, a summary block with severity counts. Structured so `jq` can extract counts and CVE IDs.
- `exercises/scan-report-flagged.json` — same schema, but with 2 Critical + several High findings (each with a `FixedVersion`), representing an image the gate would block.
- `exercises/deploy-flagged.yaml` — a Deployment referencing a would-be-blocked tag (e.g. `$DCS_REGISTRY/samples/hello-dcs:flagged`), used to *narrate* the gate blocking a pull (observe/concept; not asserted to fail on a scanner-less cluster).

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — overview + first-time note. DCS blurb: **Registry (Harbor)** scan gates → `{{< param dcs_docs_base_url >}}/registry/overview`. Frame: on an air-gapped platform the registry is the security checkpoint.
- **`01-scanning-on-dcs.md`** — concept. Vulnerability scanning (CVEs in image layers) vs compliance scanning (policy/config). Scan scope: per-image, per-project, global. Where the scan sits (on push/periodic) and what a gate does. Upstream: [Trivy](https://trivy.dev/), [CVE](https://www.cve.org/); DCS gate concept → DCS docs. *(No command → no examiner; pure concept page.)*
- **`02-read-a-scan-report.md`** —
  - `editor:open-file` `scan-report.json`; explain the schema (summary + findings).
  - `terminal:execute` `jq '.summary.severityCount' scan-report.json` → examiner `verify-report-summary` (jq returns a non-empty count object).
  - `terminal:execute` `jq -r '.vulnerabilities[] | "\(.severity)\t\(.id)\t\(.package)"' scan-report.json` → examiner `verify-report-cves` (at least one CVE line printed).
  - Explain severities, `FixedVersion`, and reading the report as a risk summary.
- **`03-the-gate.md`** —
  - Open `scan-report-flagged.json`; `jq '[.vulnerabilities[]|select(.severity=="Critical")]|length' scan-report-flagged.json` → examiner `verify-flagged-criticals` (returns ≥ 1). This is *why* the gate trips.
  - `editor:open-file` `deploy-flagged.yaml`; narrate: applying this would be blocked at pull time by the gate (the node can't pull an image the gate quarantines → `ImagePullBackOff`). `{{< note >}}` framing this as observe/concept (no live scanner assertion). DCS gate → docs.
  - Concept: gate threshold policy (block ≥ High, warn on Medium), per-project override.
- **`04-remediation.md`** —
  - Remediation options: choose a **patched tag**, or **rebuild on a patched base**; re-scan. Inspect the clean image to show it passes: `skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0` → examiner `verify-clean-image` (digest returned) — the remediated image is pullable/clean.
  - `jq` the clean report to show zero Critical/High: `jq '.summary.severityCount.Critical // 0' scan-report.json` → examiner `verify-no-criticals` (returns 0).
  - **Security Exception Process** (ITSM) — the escape hatch when a fix isn't yet available; blurb + `{{< param dcs_docs_base_url >}}/governance/overview`.
- **`98-your-feedback.md`** — standard feedback page (workshop=lab-c01-image-scanning).
- **`99-workshop-summary.md`** — recap; **Check Your Understanding** (3 Q): vuln vs compliance scanning; what a gate does + threshold; two remediation paths and the exception process. A final examiner (repeat `verify-report-summary`-style) as the knowledge-check action, per house standard.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. All commands are `jq`/`skopeo`/`oc` against local fixtures or remote refs — no `cd`.
- After `editor:open-file`, the next `terminal:execute` returns focus to Terminal — standard.

## 8. Design Notes

- **Static scan-report fixtures**, not a live Harbor scan: keeps every step examiner-verifiable air-gapped and deterministic, and doesn't depend on a scanner being wired to the test cluster. Task in `tasks.md`: optionally wire a live Harbor scan/API read once a scanner-backed Harbor is reachable in-session.
- **No new sample image needed:** the clean case is `samples/hello-dcs:1.0` (exists, proven in A04); the flagged case is a *report fixture* + a narrated (non-asserted) blocked deploy. Avoids inventing an untestable "vulnerable image."
- Depth split from A04 as designed in the A04 plan/concepts ref: A04 = "read the result, understand the gate"; **C01 = report internals + gate policy + remediation**.
- Feeds **C04** (supply chain): C01 is a listed prerequisite there; C04 assumes the learner can read a report and knows the gate.
