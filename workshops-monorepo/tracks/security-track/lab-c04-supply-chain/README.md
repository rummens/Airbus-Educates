# lab-c04-supply-chain

**Supply Chain & Provenance** — Security & Compliance (Module C) workshop for the DCS Academy.

Learners trace where images come from on an air-gapped platform: pin a Pod to an image
**by digest** (not a mutable tag), read image **provenance** (source repo, revision, build)
with `skopeo inspect` + `jq`, model **signing/attestation** (cosign / SLSA) from a fixture,
and understand the DCS trusted-source model — catalogs, allowed registries, and **mirroring
via ITSM**. Pull-only, `skopeo`/`jq` (no docker/podman). Prerequisite: lab-c01
(Image Scanning & Harbor Gates); assumes A04 (`skopeo`, catalogs, digests).

Built with the `airbus-educates-workshop-authoring` skill. See the plan at
`planning/workshop-plans/lab-c04-supply-chain.md`.
