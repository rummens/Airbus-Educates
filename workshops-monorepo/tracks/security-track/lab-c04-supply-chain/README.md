# Supply Chain & Provenance

**Answer the question every secure platform must: where did this image actually come from, and can I prove it?**

On the air-gapped Digital Container Service (DCS) there is no public registry to pull from at runtime, so the software supply chain narrows to a small set of trusted sources plus a controlled mirroring on-ramp — which makes "where did this image come from?" answerable with certainty. In this lab you'll follow the whole chain (source, build, registry, run) and use the platform's own tools to account for an image: pin it by digest instead of a mutable tag, read its provenance with `skopeo` and `jq`, and reason about signatures and attestations. Image work is pull-only with `skopeo` and `jq` — no docker or podman — matching how DCS actually operates.

- **Track:** Security & Compliance — Secure on DCS · Lab 4 of 5
- **Audience:** Intermediate — comfortable inspecting images with `skopeo` and reading JSON with `jq`
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-c01-image-scanning and lab-a03-harbor-registry; comfortable with the Linux CLI.

## By the end of this lab you'll be able to

- Explain what a software supply chain is, and why an air-gap narrows it to trusted sources plus mirroring.
- Pin an image by digest instead of a mutable tag, and state the integrity guarantee that gives you.
- Read image provenance — source repo, revision, build — with `skopeo` and `jq`.
- Explain image signing and attestation (cosign / sigstore, SLSA provenance) and how a signature is verified conceptually.
- Describe the DCS trusted-source model — catalogs, allowed external registries, and image mirroring via ITSM.

## What you'll do

- Pin a workload to an image by digest and confirm the integrity guarantee it buys.
- Read an image's provenance metadata with `skopeo inspect` and `jq`.
- Reason through signature and attestation verification from a fixture, then map the DCS trusted-source and mirroring model.

## Before you start

This lab builds directly on lab-c01 (reading a scan report, the Harbor gate) and lab-a03-harbor-registry (`skopeo inspect`, catalogs, digests vs tags, the read-only robot account). Those `skopeo` basics and "what a catalog is" are not re-taught here — finish both first.
