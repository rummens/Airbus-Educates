# Workshop Plan: lab-c04-supply-chain

## 1. Workshop Metadata

- **Name:** `lab-c04-supply-chain`
- **Title:** Supply Chain & Provenance
- **Description:** Trace where images come from on an air-gapped platform — pin by digest, read image provenance and signatures, and understand trusted-source and mirroring practices on DCS.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module C — Security & Compliance)
- **Prerequisites:** C01 (Image Scanning & Harbor Gates). Assumes A04 (Harbor, catalogs, `skopeo`) and report-reading from C01.
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- Console: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Run location: **native OpenShift session namespace** (vcluster `enabled: false`). `budget: medium`.
- Workshop image: **`dcs-workshop-base`** — `skopeo` + `jq`; no docker/podman.
- Registry auth: read-only Harbor **robot account** (as A04/C01).
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.
- Signature/attestation fixture: `exercises/provenance.json` (a sample cosign/SLSA-style attestation) for the parts a scanner-less air-gapped session can't produce live. Rationale in Design Notes.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain what a software **supply chain** is and why an **air-gapped** platform narrows it to trusted sources + mirroring.
- **Pin an image by digest** (not a mutable tag) and explain the integrity guarantee.
- Read image **provenance** — labels/annotations (source repo, revision, build) — with `skopeo inspect` + `jq`.
- Explain image **signing/attestation** (cosign / sigstore, SLSA provenance) and how a signature is verified conceptually.
- Describe the DCS trusted-source model: **catalogs**, **Allowed External Registries**, and **image mirroring via ITSM**.

## 4. Connection to Previous Workshop

**Already known (from C01/A04):** `skopeo inspect`, digests vs tags, reading a JSON report with `jq`, catalogs/robot accounts. **New here:** digest pinning in a manifest, provenance labels, signatures/attestations, the trusted-source + mirroring model as a *supply-chain* story. **Do NOT re-teach:** `skopeo` basics or what a catalog is.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/pod-by-tag.yaml` — Pod referencing `$DCS_REGISTRY/samples/hello-dcs:1.0` (mutable tag) — the "before".
- `exercises/pod-by-digest.yaml` — Pod referencing the same image **by digest** (`hello-dcs@sha256:...`); the learner fills the digest from a `skopeo inspect` step (via `workshop:copy` of the command, or a documented placeholder they replace). The "after".
- `exercises/provenance.json` — a sample cosign/SLSA attestation payload (predicate with builder, source URI, git revision) for the signature-reading step.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — overview + first-time note. DCS blurb: **Registry (Harbor)** trusted sources/mirroring → `{{< param dcs_docs_base_url >}}/registry/overview`; upstream [OCI image spec](https://github.com/opencontainers/image-spec), [sigstore/cosign](https://docs.sigstore.dev/).
- **`01-supply-chain-airgapped.md`** — concept. What the supply chain is (source → build → registry → run); why air-gap = **no untrusted upstream at runtime**; the DCS trusted-source set: **DCS Catalogs**, **Allowed External Registries**, **Proxy-Cached Catalog**, and **mirroring via ITSM**. *(Concept page.)*
- **`02-pin-by-digest.md`** —
  - `terminal:execute` `skopeo inspect --format '{{ "{{" }}.Digest{{ "}}" }}' docker://$DCS_REGISTRY/samples/hello-dcs:1.0` → examiner `verify-digest` (a `sha256:` digest returned). Explain tag = movable pointer, digest = immutable content hash.
  - `editor:open-file` `pod-by-tag.yaml` then `pod-by-digest.yaml`; explain pinning by digest defeats tag mutation.
  - `terminal:execute` `oc apply -f pod-by-digest.yaml`; `oc get pod hello-pinned -w` → examiner `verify-pinned-running` (Running; polling). *(If the placeholder digest must be substituted, use `workshop:copy` to give the exact command, or ship the manifest already digest-pinned to `hello-dcs:1.0`'s known-good pattern — Design Notes.)*
- **`03-provenance-and-signatures.md`** —
  - `terminal:execute` `skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0 | jq '.Labels'` → examiner `verify-labels` (non-empty labels object). Explain provenance labels (`org.opencontainers.image.source`, `.revision`).
  - `editor:open-file` `provenance.json`; `terminal:execute` `jq -r '.predicate.builder.id, .predicate.invocation.configSource.uri' provenance.json` → examiner `verify-provenance` (builder + source URI printed). Explain SLSA provenance + cosign signing/verification conceptually (verify = check signature against a trusted key/identity). *(Signatures modelled from the fixture — live cosign verify not asserted air-gapped.)*
- **`04-mirroring-and-trust.md`** — concept + one recap command.
  - The **image-mirroring ITSM request** (External→DCS Harbor / DCS Harbor→DCS Harbor); why mirroring is the *only* on-ramp for external images; how a mirrored image inherits scanning + gating (ties back to C01). ITSM blurb → `{{< param dcs_docs_base_url >}}/support/itsm-requests`.
  - `terminal:execute` `skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0 | jq -r '.Name'` → examiner `verify-source-is-harbor` (the `.Name` is under `$DCS_REGISTRY` — proving every runtime image comes from the trusted registry).
- **`98-your-feedback.md`** — standard (workshop=lab-c04-supply-chain).
- **`99-workshop-summary.md`** — recap; **Check Your Understanding** (3 Q): tag vs digest integrity; what provenance/attestation gives you; how external images legitimately enter an air-gapped DCS. Final examiner (`verify-digest`-style) as the knowledge-check action.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. `skopeo`/`jq`/`oc` on remote refs + local fixtures — no `cd`.

## 8. Design Notes

- **No new image:** provenance/signatures read from `hello-dcs` labels + a static attestation fixture; digest pinning uses the real `hello-dcs` digest. Testable air-gapped.
- **Digest substitution:** if a learner-supplied digest is awkward to examiner-verify deterministically, ship `pod-by-digest.yaml` already pinned to `hello-dcs:1.0` (the manifest carries a real digest set at author time) and have the learner *confirm* it matches `skopeo inspect` — keeps the step verifiable. Decide at authoring; note the choice made.
- Live cosign verification is out of scope air-gapped (no key infra guaranteed in-session); modelled from a fixture. Task in `tasks.md`: wire real cosign verify when signed images + trust policy exist on the test cluster.
- Builds directly on **C01**; together they form the "image trust" pair of the Security track.
