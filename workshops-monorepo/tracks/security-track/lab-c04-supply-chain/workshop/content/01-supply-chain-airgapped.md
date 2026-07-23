---
title: The Supply Chain, Air-Gapped
---

Before you touch an image, it helps to see the whole path it travelled to reach your cluster —
and how the air-gap reshapes that path.

## What a supply chain is

A container image doesn't appear from nowhere. It flows through a chain of steps, each a place
where something could be added, swapped, or tampered with:

**source code → build → registry → run**

- **Source** — the git repository the image is built from (a revision, a commit).
- **Build** — a CI pipeline turns that source into an image and records *how* (the builder, the
  inputs).
- **Registry** — the image is stored and addressed, by tag and by digest.
- **Run** — a cluster pulls it and starts a container.

"Supply-chain security" is simply being able to **trust every link**: know the source, trust
the build, guarantee the registry served exactly what was built, and confirm the running
container is that same image. The rest of this lab is one control per link.

## Why the air-gap makes this tractable

On the public internet, the "run" step can pull from anywhere a manifest points —
`docker.io`, `quay.io`, an unknown mirror. Any of those links is outside your control.

{{< param product_short >}} is **air-gapped**: at runtime there is **no untrusted upstream**.
The only place a cluster can pull from is the {{< param product_short >}} **Harbor** registry.
That single fact collapses a sprawling, internet-wide chain into a short, auditable one:

- Every image that can run is **already inside Harbor**.
- Anything from outside had to be **deliberately brought in** (mirrored) — never fetched
  just-in-time from the internet.

So the supply chain becomes: *trusted sources feed Harbor; Harbor is the only thing the cluster
trusts.*

## The DCS trusted-source set

Images become available in Harbor through a small, governed set of routes — the same catalogs
you met in A03, now seen as the **inputs to the supply chain**:

- **DCS Catalogs** — curated image sets the platform vets and maintains (where `samples/hello-dcs` lives).
- **Allowed External Registries** — an explicit permit-list of upstream registries whose images *may* be brought in. Not "the internet" — a named, governed set.
- **Proxy-Cached Catalog** — a caching proxy for permitted upstream images; first pull fetches and caches, later pulls are local. **Not usable from a PROD namespace** — PROD consumes only images already fully in Harbor.
- **Mirroring via ITSM** — the controlled on-ramp for an external image that isn't in a catalog yet (page 4).

{{< note >}}
Catalogs, allowed registries, and mirroring are {{< param product_short >}}-specific — see the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/registry/overview).
The image format itself ([OCI image spec](https://github.com/opencontainers/image-spec)) and the
signing tools ([sigstore/cosign](https://docs.sigstore.dev/), [SLSA](https://slsa.dev/)) are
standard, and link to their upstream docs.
{{< /note >}}

Analogy: think of a secure facility with a single, monitored loading dock. Nothing arrives by
being thrown over the fence — everything comes through the dock, logged and inspected. Harbor is
that dock, and the catalogs are its approved suppliers.

With the shape of the chain in mind, the next three pages tighten one link each: **pin what you
run** (digest), **read where it came from** (provenance/signatures), and **control how it got
in** (mirroring).
