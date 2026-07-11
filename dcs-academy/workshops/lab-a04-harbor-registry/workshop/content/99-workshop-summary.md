---
title: Summary
---

You worked with the {{< param product_short >}} Harbor registry end to end — the single,
air-gapped source every image on the platform comes from.

## What You Did

- Learned why {{< param product_short >}} uses **one air-gapped registry**, and how images arrive via **catalogs** (DCS Catalogs, Allowed External Registries, Proxy-Cached — the last not usable from PROD).
- Inspected and pulled a catalog image with **`skopeo`** (daemonless — no docker/podman double-virtualization), and ran it on the cluster.
- Browsed a Harbor **project** — tags, digests, scan results — in the UI and on the CLI.
- Learned that **pushing** needs a dedicated, GitOps-managed project (out of scope here).
- Saw how external images are **mirrored** in via ITSM, and how **vulnerability scanning gates** unsafe images.

## Challenge

Do it yourself, unguided: **confirm a specific image is present in Harbor by its digest.**
Inspect `samples/hello-dcs:1.0` and check it reports a digest. Run the check when ready.

```examiner:execute-test
name: verify-image-inspectable
title: Challenge — inspect the image in Harbor
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

{{< note >}}
**Hint:** `skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0` — look for the
`Digest` field. Add `--format '{{ "{{" }}.Digest{{ "}}" }}'` to print just the digest.
{{< /note >}}

## Check Your Understanding

1. Why does {{< param product_short >}} run everything from a single registry?

{{< note >}}
**Answer:** It's air-gapped — public registries are unreachable. One trusted source means
every image can be vetted, scanned, and recorded; you can't run an unknown image from the
internet because there is no internet to run it from.
{{< /note >}}

2. What does a vulnerability **scan gate** do?

{{< note >}}
**Answer:** It blocks pulling/deploying an image whose scan findings exceed a set threshold
— turning the registry into a safety checkpoint. Remediate or request a security exception.
{{< /note >}}

3. Why can you pull from Harbor in this lab but not push?

{{< note >}}
**Answer:** Pulling uses a read-only robot account. Pushing needs a dedicated,
GitOps-managed Harbor project and a push-capable robot account, which the platform
provisions — too much to stand up per session, so it's conceptual here.
{{< /note >}}

## Next Steps

Next in Foundations: **Access & Tenancy** — how teams onboard to {{< param product_short >}}
and how access is scoped to your namespaces.
