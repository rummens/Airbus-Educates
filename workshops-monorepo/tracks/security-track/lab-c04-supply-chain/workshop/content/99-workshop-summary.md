---
title: Summary
---

You followed an image through the whole {{< param product_short >}} supply chain — source,
build, registry, run — and used one control per link to make it trustworthy on an air-gapped
platform.

## What You Did

- Saw the supply chain as **source → build → registry → run**, and why an air-gap narrows it to **trusted sources + mirroring**.
- **Pinned a Pod by digest** instead of a mutable tag, and ran it — the integrity guarantee that a retag can't change what runs.
- Read image **provenance** (`org.opencontainers.image.source` / `.revision`) with `skopeo inspect` + `jq`.
- Modelled a signed **SLSA attestation** from a fixture — builder id, config source URI, git revision — and how a signature is verified against a trusted identity.
- Confirmed the trusted-source model: **catalogs** and **allowed registries** define what's in, **mirroring via ITSM** is the only (scanned, gated) on-ramp, and every runtime image is served **from Harbor**.

## Challenge

Do it yourself, unguided: **prove the sample image has a stable, immutable identity.** Inspect
`samples/hello-dcs:1.0` and check it reports a `sha256:` digest — the anchor everything else
pins to. Run the check when ready.

```examiner:execute-test
name: verify-digest
title: Challenge — the image reports a sha256 digest
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

{{< note >}}
**Hint:** `skopeo inspect --format '{{ "{{" }}.Digest{{ "}}" }}' docker://$DCS_REGISTRY/samples/hello-dcs:1.0`
prints just the digest — a single `sha256:...` line.
{{< /note >}}

## Check Your Understanding

1. Why does pinning by **digest** give you an integrity guarantee that a **tag** doesn't?

{{< note >}}
**Answer:** A tag is a mutable pointer — someone can re-push `1.0` to point at different content
with the same name. A digest is a `sha256:` hash of the image content, so a reference pinned to a
digest can only ever resolve to that exact content; change one byte and the digest changes.
{{< /note >}}

2. What does **provenance / attestation** give you that an image label alone does not?

{{< note >}}
**Answer:** A label is an unsigned claim baked in at build time — anyone can write one. A signed
attestation (e.g. SLSA provenance via cosign) is a claim about *who* built the image and *from
what source*, wrapped in a signature you can verify against a trusted key/identity — so you *know*
the origin rather than just trusting a text field.
{{< /note >}}

3. How does an **external** image legitimately enter an air-gapped {{< param product_short >}}?

{{< note >}}
**Answer:** Only by being **mirrored** into Harbor through a governed **ITSM request** — never a
live pull from the internet. Because that is the single on-ramp, every image inherits scanning
and the gate; there is no side door.
{{< /note >}}

## Next Steps

You've completed the "image trust" pair of the Security track (C01 scanning/gating + C04 supply
chain). Next in Security & Compliance: applying these guarantees to **pod security and secrets**
on {{< param product_short >}}.
