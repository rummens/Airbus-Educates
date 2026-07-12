---
title: Mirroring and Scanning
---

Two last pieces complete the picture: how an *external* image legitimately gets into Harbor,
and how Harbor stops an unsafe one from being used.

## Mirroring: getting an external image in

The platform is air-gapped, so you can't pull from `docker.io` at runtime. When a team needs
an upstream image that isn't in a catalog yet, it is **mirrored** into Harbor — copied in
through a controlled process — and the request is raised as an
**[ITSM ticket]({{< param dcs_docs_base_url >}}/support/itsm-requests)** (External → DCS
Harbor, or DCS Harbor → DCS Harbor). Mirroring is asynchronous and governed, not something a
session does live.

So the workshop models the **outcome**: the `hello-dcs` image you've been using is already
mirrored and present. Confirm you can read its manifest — the proof it's fully in Harbor:

```terminal:execute
command: skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0 --format '{{.Digest}}'
```

```examiner:execute-test
name: verify-image-inspectable
title: The mirrored image is present in Harbor
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

## Scanning and the gate

Every image in Harbor is **scanned for vulnerabilities**. Harbor records a severity summary
per artifact (Critical / High / …), and the platform can set a **gate**: a policy that
**blocks** pulling or deploying an image whose findings exceed a threshold. That's how a
single-source registry becomes a safety control — not just storage, but a checkpoint.

You saw the scan result in the Harbor UI on the previous page. In practice:

- A **clean** image passes the gate and can be deployed.
- A **vulnerable** image (findings over the threshold) is **flagged and blocked** — the pull
  or admission is refused, and the team must remediate (rebuild on a patched base) or request
  a **security exception** via ITSM.

{{< note >}}
Foundations stops at "read the result, understand the gate." Remediation, scan policies, and
exceptions are the **Security & Compliance track** (C01/C04). The scan data itself lives in
Harbor and its API — it needs a real Harbor to view live.
{{< /note >}}

That's the {{< param product_short >}} registry end to end: one trusted source, images in via
catalogs and mirroring, gated by scanning, consumed by pull.
