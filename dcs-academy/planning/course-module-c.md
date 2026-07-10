# Module C — Security & Compliance Track (Elective)

For security and compliance practitioners. Builds on Foundations. Carries a security-focused sample workload. Sequential within the track. All follow the house standards. Names: `lab-c0N-name`.

*Breakdown-level plan — lighter than Modules A/B; expand to full per-workshop plans when this track is scheduled (see `tasks.md`).*

---

### Workshop C01: Image Scanning & Harbor Gates

**Directory name:** `lab-c01-image-scanning`
**Covers ideas:** 12
**Type:** Elective (Security)
**Prerequisites:** Module A (esp. A04 Harbor)
**Learning objectives:** Interpret Harbor scan results; understand gate policies that block vulnerable images.
**Narrative arc:** Push an image → read its scan → see a vulnerable image blocked by the gate.
**Code exercises:** Trigger a scan; inspect findings (`dcs-tools` / `trivy`); attempt to deploy a flagged image.
**DCS-specific:** Harbor scan gates → `/concepts/registry`.

### Workshop C02: Pod Security / SCC on DCS

**Directory name:** `lab-c02-pod-security-scc`
**Covers ideas:** 13
**Type:** Elective (Security)
**Prerequisites:** Module A
**Learning objectives:** Explain the restricted policy / arbitrary-UID requirement; recognise what needs baseline and why.
**Narrative arc:** Deploy a well-behaved image → deploy a root-assuming image and watch it fail → understand the fix.
**Code exercises:** Compare a compliant vs non-compliant image; read the rejection; discuss remediation.
**Docs:** SCC → upstream; contrast with Educates restricted policy.

### Workshop C03: Secrets Management

**Directory name:** `lab-c03-secrets-management`
**Covers ideas:** 14
**Type:** Elective (Security)
**Prerequisites:** Module A
**Learning objectives:** Handle secrets safely; avoid leaking them into images, logs, or env dumps.
**Narrative arc:** Spot a bad pattern (secret in image/log) → move to a Secret → verify it is not exposed.
**Code exercises:** Refactor a workload to use a Secret; confirm no leakage.

### Workshop C04: Supply Chain & Provenance

**Directory name:** `lab-c04-supply-chain`
**Covers ideas:** 15
**Type:** Elective (Security)
**Prerequisites:** C01
**Learning objectives:** Describe trusted-source and provenance practices in an air-gapped supply chain.
**Narrative arc:** Where images come from → why mirroring/trust matters air-gapped → verify provenance.
**Code exercises:** Inspect image provenance/signatures available in Harbor.

### Workshop C05: EU Data-Residency & Compliance

**Directory name:** `lab-c05-data-residency`
**Covers ideas:** 16
**Type:** Elective (Security)
**Prerequisites:** Module A
**Learning objectives:** Describe DCS data-locality guarantees and the compliance workflows a tenant follows.
**Narrative arc:** Multi-national EU context → data-residency guarantees → tenant compliance responsibilities.
**Code exercises:** Mostly conceptual + observe; inspect where workloads/data are placed.
**DCS-specific:** Link to DCS compliance docs via `dcs_docs_base_url`.

## Future Expansion Ideas

- Network policy / zero-trust workshop.
- Admission policy (Kyverno) authoring for tenants.
