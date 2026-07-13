Exercise files for "Supply Chain & Provenance".

- `pod-by-tag.yaml` — a Pod that runs the sample image by its **mutable tag**
  (`${DCS_REGISTRY}/samples/hello-dcs:1.0`) — the "before". Shown for contrast.
- `pod-by-digest.yaml` — the same image pinned by **immutable digest**
  (`${DCS_REGISTRY}/samples/hello-dcs@${DIGEST}`) — the "after". The instructions
  capture the real digest from `skopeo inspect` into `${DIGEST}` and substitute both
  variables with `envsubst` at apply time, so the manifest is never tied to a specific
  registry or a hardcoded (possibly stale) digest.
- `provenance.json` — a sample cosign/SLSA-style attestation (an in-toto statement with a
  SLSA provenance predicate: builder, config source URI, git revision). Used to read
  provenance where an air-gapped session can't produce a live signature.

The manifests use the `${DCS_REGISTRY}` (and, for the digest pod, `${DIGEST}`) environment
variables so they are not tied to a specific registry; apply them with `envsubst` (the
instructions do this for you).
