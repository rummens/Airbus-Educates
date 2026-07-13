---
title: Provenance and Signatures
---

Pinning proves *what* runs. This page is about *where it came from* — the **source** and
**build** links. Two layers of evidence: **provenance labels** baked into the image, and a
signed **attestation** that vouches for them.

## Provenance labels on the image

A well-built image carries standard [OCI](https://github.com/opencontainers/image-spec)
annotations recording its origin — the source repository and the exact git revision it was built
from. Read the image's labels:

```terminal:execute
command: skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0 | jq '.Labels'
```

You should see a JSON object of labels. The supply-chain-relevant ones are:

- `org.opencontainers.image.source` — the source repository URL.
- `org.opencontainers.image.revision` — the git commit the image was built from.

```examiner:execute-test
name: verify-labels
title: The image carries a non-empty labels object
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

Labels answer "what does the image *claim* about itself." But a label is just text baked in at
build time — anyone who can build an image can write any label. On its own it's a claim, not
proof. That's what signing and attestation add.

## Attestation: a signed claim about the build

An **attestation** is a machine-readable statement about an image — *who* built it, *from what
source*, *how* — wrapped in a **signature**. Tools like
[cosign](https://docs.sigstore.dev/) (from the sigstore project) create and verify these, and the
[SLSA](https://slsa.dev/) framework standardises the *provenance* format: an in-toto statement
whose predicate describes the build.

A real air-gapped session doesn't have live signing infrastructure, so we read a representative
attestation from a fixture. Open it:

```editor:open-file
file: ~/exercises/provenance.json
```

It's an in-toto statement with a SLSA provenance predicate. Pull out the two links that matter —
who built it and from what source:

```terminal:execute
command: jq -r '.predicate.builder.id, .predicate.invocation.configSource.uri' ~/exercises/provenance.json
```

You should see the **builder id** (the CI system that produced the image) and the **config
source URI** (the git repo + entrypoint it built from). The git **revision** is right beside it
at `.predicate.invocation.configSource.digest.sha1` — the same commit the image label claimed,
now inside a *signed* statement.

```examiner:execute-test
name: verify-provenance
title: The attestation yields a builder id and source URI
timeout: 10
```

## How a signature is verified (conceptually)

Verification answers "should I trust this attestation?" Conceptually:

1. The attestation is **signed** by the builder's key (or a sigstore identity — a short-lived
   certificate tied to the CI's OIDC identity).
2. A verifier checks the signature against a **trusted key or identity** it was told to expect
   (e.g. "only accept images signed by *our* CI").
3. If the signature is valid **and** the identity is one you trust, the provenance is
   trustworthy — you now *know*, not just *hope*, where the image came from.

{{< note >}}
Live `cosign verify` needs signed images and a trust policy on the cluster, which an air-gapped
session doesn't guarantee — so provenance and signatures are modelled here from the fixture. On a
signing-enabled {{< param product_short >}} cluster the same predicate comes from a real, verified
attestation. See [sigstore/cosign](https://docs.sigstore.dev/) and [SLSA](https://slsa.dev/).
{{< /note >}}
