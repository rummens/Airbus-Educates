---
title: Workshop Overview
---

Welcome back. In this workshop, part of **{{< param product_name >}}**, you'll work with the
one place every image on {{< param product_short >}} comes from — the **Harbor** registry.
In A02 you deployed an image that Harbor was already serving. Now you'll manage that
relationship yourself: find images in **catalogs**, pull one with `skopeo`, run it, browse
it in the Harbor UI, and see how vulnerability scanning decides what is allowed to run.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

{{< param product_short >}} is **air-gapped**: the public internet — and every public registry
like `docker.io` or `quay.io` — is unreachable. That is a deliberate security posture, and it
puts Harbor at the centre of everything you run. Understanding how images get *into* Harbor,
and how you get them *out*, is the whole job of this workshop.

## What You'll Learn

By the end you will be able to:

- Explain why {{< param product_short >}} uses a single, air-gapped registry, and how images arrive through **catalogs** (DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog).
- Inspect and pull a catalog image with [`skopeo`](https://github.com/containers/skopeo) — and say why `skopeo`, not `docker`/`podman`.
- Run a catalog image on the cluster and confirm the pull landed.
- Browse a Harbor **project** — its tags, digests, and scan results.
- Explain how external images are brought in via an **image-mirroring ITSM request**.
- Read a Harbor vulnerability **scan result** and explain the **gate** that blocks unsafe images.
- Know that Harbor also stores **Helm charts**, that **PROD** namespaces cannot use the Proxy-Cached Catalog, and that **pushing** needs a dedicated project (out of scope here).

## Prerequisites

- **lab-a02-kubernetes-essentials** — you should be comfortable running `oc` and applying a manifest.
- Familiarity with [container images](https://kubernetes.io/docs/concepts/containers/images/) and basic [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) usage.

No experience with `skopeo` or Harbor is assumed — we introduce both.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} project. Your session is pre-configured with a read-only
Harbor **robot account**, so `skopeo` can pull and inspect images from the registry
without you logging in. Commands are run with `oc` and `skopeo` in the terminal.

## Time and Difficulty

- **Estimated time:** 45 minutes
- **Difficulty:** Beginner

## Further Reading

- [Harbor documentation](https://goharbor.io/docs/)
- [`skopeo` documentation](https://github.com/containers/skopeo)
- [Images (Kubernetes)](https://kubernetes.io/docs/concepts/containers/images/)
