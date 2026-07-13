---
title: Mirroring and Trusted Sources
---

The last link is **how an image legitimately enters the chain**. On an air-gapped platform there
is exactly one answer, and it's a governed process — not a live pull.

## Mirroring: the only on-ramp for external images

You can't pull from `docker.io` at runtime — it's unreachable. So when a team needs an upstream
image that isn't in a catalog yet, it is **mirrored** into Harbor: copied in through a controlled
process, raised as an **[ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests)**
(External → DCS Harbor, or DCS Harbor → DCS Harbor). Mirroring is asynchronous and governed — not
something a session does live.

That governance is the point. Because mirroring is the *only* way an external image gets in,
every image in Harbor has passed through it — and a mirrored image **inherits the platform's
controls**: it is **scanned** and subject to the **gate** you saw in C01. There is no side door
that skips scanning. The supply chain has exactly one entrance, and that entrance enforces the
rules.

So the trusted-source model is complete:

- **Catalogs** and **allowed registries** define *what may be brought in*.
- **Mirroring via ITSM** is *how* it's brought in — controlled, logged, scanned.
- **Digest pinning** and **provenance/attestation** let you *prove* what you're running and where
  it came from.

## Prove the runtime source

The clinching property of an air-gapped chain: **every image a cluster runs is addressed under
Harbor**. Confirm it for the sample image — read the fully-qualified name skopeo resolves:

```terminal:execute
command: skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0 | jq -r '.Name'
```

The `.Name` is the image under your {{< param product_short >}} registry
(`$DCS_REGISTRY/samples/hello-dcs`) — not `docker.io`, not `quay.io`. Nothing you run points
outside Harbor, because nothing outside Harbor is reachable.

```examiner:execute-test
name: verify-source-is-harbor
title: The runtime image is served from the DCS registry
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

That's the supply chain end to end: trusted sources feed Harbor through a governed, scanned
on-ramp; you pin by digest and read provenance to prove exactly what you run and where it was
built. On an air-gapped platform the chain is short enough to trust every link.
