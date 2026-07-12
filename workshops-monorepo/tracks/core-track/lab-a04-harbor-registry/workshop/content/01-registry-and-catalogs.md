---
title: The Registry and Its Catalogs
---

Before you touch an image, it's worth understanding *why* {{< param product_short >}}'s
registry works the way it does — because the air-gap shapes everything.

## One Trusted Source

On the public internet, a cluster pulls images from wherever a manifest points —
`docker.io`, `quay.io`, `ghcr.io`, and so on. {{< param product_short >}} does not work that
way. It is **air-gapped**: those registries are simply unreachable. Every image you run
comes from **one** place — the {{< param product_short >}} **Harbor** registry.

That single-source model is a security decision, not a limitation. When there is exactly one
registry, the platform can guarantee that everything running on it has been **vetted,
scanned, and recorded** — you cannot accidentally run an unknown image from the internet
because there is no internet to run it from.

{{< note >}}
The Harbor registry is a {{< param product_short >}}-specific concept — how images are
catalogued, mirrored, and gated is particular to the platform. See the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/registry/overview).
[Harbor](https://goharbor.io/docs/) itself and [OCI images](https://kubernetes.io/docs/concepts/containers/images/)
are standard, and link to their upstream docs.
{{< /note >}}

## How Images Arrive: Catalogs

If the platform is sealed off, how does an image ever get *in*? Through **catalogs** —
the three defined routes by which images become available in Harbor:

- **DCS Catalogs** — curated image sets the platform provides and maintains. This is where the
  `samples/hello-dcs` image you deployed in A02 lives. Think of it as the platform's own
  vetted shelf.
- **Allowed External Registries** — a permitted list of upstream registries whose images may
  be brought in. Not "the whole internet" — a governed, explicit set.
- **Proxy-Cached Catalog** — a caching proxy for permitted upstream images: the first pull
  fetches and caches, later pulls are served locally. **It cannot be used from a PROD
  namespace** — PROD may only consume images that are already fully present in Harbor, never
  a just-in-time proxy fetch.

Analogy: if you've used a corporate software repository mirror, this is the same idea — you
don't `pip install` from the internet on a locked-down machine; you pull from the mirror your
organisation curates.

## What Harbor Organises

Inside Harbor, content is grouped into **projects** (namespaces of the registry — e.g.
`samples`). A project holds **repositories**, each repository holds **tags** and the
immutable **digests** they point at. Harbor also:

- stores **Helm charts** alongside container images (same catalog rules apply — hands-on Helm is a Developer-track topic);
- uses **robot accounts** — non-human credentials — for automation like pulling in a workshop session;
- manages repositories and permissions **the GitOps way** (declared in git, not clicked in a UI);
- **scans images for vulnerabilities** and can **gate** them — the subject of page 4.

Your session has been given a **read-only robot account**, which is why you can pull and
inspect without logging in — but not push. More on that on page 3.

## Your Toolkit

You'll do all image work with **`skopeo`** — a daemonless command-line tool for inspecting and
copying images between registries. Confirm it is available:

```terminal:execute
command: skopeo --version
```

You should see a version line, for example:

```
skopeo version 1.14.0
```

We'll explain *why* `skopeo` (and not `docker` or `podman`) on the next page. For now, this
just confirms your toolkit is ready.

```examiner:execute-test
name: verify-skopeo
title: Verify skopeo is available
timeout: 10
```
