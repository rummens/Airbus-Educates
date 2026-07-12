---
title: Meet the Sample App
---

Before you deploy anything, it's worth knowing *what* you're deploying and *where it comes
from* — because on {{< param product_short >}} that "where" is not Docker Hub.

## What the App Is

`hello-dcs` is a tiny web server. It listens on **port 8080** and answers HTTP requests
with a small page — nothing more. That's deliberate: a minimal app keeps the focus on the
*workflow* around it, and it gives you a single, evolving artifact to carry through the
Developer track. Later workshops feed it configuration, add health probes, and give it
storage — but it starts life as this bare web server.

## Where Its Image Lives

Look at the image line in the manifest you have open:

```editor:select-matching-text
file: ~/exercises/deployment.yaml
text: "image: ${DCS_REGISTRY}/samples/hello-dcs:1.0"
```

The image reference is `{{< param dcs_registry >}}/samples/hello-dcs:1.0`. Every part of
that matters:

- `{{< param dcs_registry >}}` — the {{< param product_short >}} **Harbor** registry. On an air-gapped platform this is the *single source of images*; there is no reaching out to Docker Hub or Quay from inside the cluster.
- `samples/hello-dcs` — the repository within Harbor.
- `:1.0` — an explicit version tag. Always pin a tag; never rely on `:latest`, which is ambiguous and not reproducible.

## Why Harbor, Not Docker Hub

{{< param product_short >}} is **air-gapped** — workloads cannot pull from the public
internet. Instead, images are made available through {{< param product_short >}}'s
[Harbor registry]({{< param dcs_docs_base_url >}}/registry/overview): the platform mirrors
approved images into Harbor, scans them for vulnerabilities, and your namespace pulls from
there with a read-only robot account. You met this in Foundations **A04** — here you simply
consume the result.

{{< note >}}
If you've worked with VMs, think of the Harbor image as a **golden VM template in your
organisation's internal catalog**: vetted, versioned, and served from inside the perimeter —
never downloaded ad-hoc from the open internet.
{{< /note >}}

No commands to run on this page — you now know what `hello-dcs` is and where it comes from.
Next, you'll deploy it.
