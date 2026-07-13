---
title: Workshop Overview
---

Welcome back. In this workshop, part of **{{< param product_name >}}**, you'll answer a
question every secure platform has to answer: **where did this image actually come from, and
can I prove it?** In A04 you pulled images from Harbor; in C01 you saw Harbor scan and gate
them. Now you'll follow the whole **software supply chain** — source, build, registry, run —
and learn the controls that keep it trustworthy on an air-gapped platform: **digest pinning**,
**provenance**, **signatures/attestations**, and **mirroring**.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

{{< param product_short >}} is **air-gapped**: there is no public registry to pull from at
runtime, so the supply chain narrows to a small set of **trusted sources** plus a controlled
**mirroring** on-ramp. That makes the questions in this lab answerable with certainty — every
image is accounted for, and you'll use the platform's own tools to show it.

## What You'll Learn

By the end you will be able to:

- Explain what a software **supply chain** is, and why an air-gap narrows it to trusted sources + mirroring.
- **Pin an image by digest** instead of a mutable tag, and state the integrity guarantee that gives you.
- Read image **provenance** — source repo, revision, build — with [`skopeo`](https://github.com/containers/skopeo) and [`jq`](https://stedolan.github.io/jq/).
- Explain image **signing/attestation** ([cosign / sigstore](https://docs.sigstore.dev/), [SLSA provenance](https://slsa.dev/)) and how a signature is verified conceptually.
- Describe the {{< param product_short >}} trusted-source model — catalogs, allowed external registries, and **image mirroring via ITSM**.

## Prerequisites

- **lab-c01** (Image Scanning & Harbor Gates) — reading a scan report with `jq`, the Harbor gate.
- **lab-a04-harbor-registry** — `skopeo inspect`, catalogs, digests vs tags, the read-only robot account.

We build directly on those; `skopeo` basics and "what a catalog is" are not re-taught here.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} session namespace. Your session is pre-configured with a read-only Harbor
**robot account**, so `skopeo` can inspect and pull without you logging in. All image work uses
`skopeo` and `jq`; the cluster is driven with `oc`.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Intermediate

## Further Reading

- [OCI image spec](https://github.com/opencontainers/image-spec) — the image/digest format
- [sigstore / cosign](https://docs.sigstore.dev/) — signing and verification
- [SLSA](https://slsa.dev/) — supply-chain levels and provenance
- [`skopeo`](https://github.com/containers/skopeo) and [`jq`](https://stedolan.github.io/jq/)

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
