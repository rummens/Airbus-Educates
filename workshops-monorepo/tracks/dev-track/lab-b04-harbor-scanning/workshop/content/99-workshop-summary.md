---
title: Summary
---

You went from "here's an image running on {{< param product_short >}}" to understanding the
registry it lives in end to end: how it's catalogued, who's allowed to touch it, what it
does to every image on arrival, and what happens when an image fails that check.

## What You Did

- Navigated Harbor's **catalogs** (DCS Catalogs, Allowed External Registries, the
  Proxy-Cached Catalog) and the **robot account** model — pull-only vs push-capable, both
  scoped to a project.
- Inspected and pulled `samples/hello-dcs:1.0` with `skopeo`, using a read-only robot
  account — no `docker`/`podman` daemon needed.
- Confirmed the image B02 builds and pushes actually lands in its Harbor project.
- Read a Harbor scan report with `jq` — the `severityCount` summary and the
  `vulnerabilities` findings (CVE `id`, `severity`, `package`, `FixedVersion`) — and told
  **vulnerability** scanning apart from **compliance** scanning.
- Read a **flagged** report and traced what the **gate** does: it sits in the pull path and
  refuses the artifact, so the Pod would stick in `ImagePullBackOff`.
- **Remediated** a flagged image (patched tag or rebuild on a patched base) and confirmed
  the replacement passes — digest present, zero Criticals.
- Learned that mirroring, quota increases, and security exceptions are all **ITSM**
  requests, not self-service or direct admin actions.

## Check Your Understanding

1. Why does {{< param product_short >}} have exactly **one** registry instead of letting
   teams pull from anywhere?

{{< note >}}
**Answer:** The platform is air-gapped, and having a single trusted source (Harbor) means
there is exactly one place to enforce "nothing unsafe runs here" — scanning, gating, and
access control all happen at that one chokepoint instead of being bypassable elsewhere.
{{< /note >}}

2. What's the difference between **vulnerability** scanning and **compliance** scanning?

{{< note >}}
**Answer:** Vulnerability scanning matches the software in an image's layers against known
[CVEs](https://www.cve.org/) — "does this contain a known flaw?" Compliance scanning checks
the image against policy/configuration rules — "is it built the way policy requires?" (runs
as root, missing labels, forbidden base). An image can pass one and fail the other.
{{< /note >}}

3. What does a **scan gate** do, and where does it sit?

{{< note >}}
**Answer:** It sits in the pull path and blocks using an image whose scan findings exceed a
threshold — the pull is refused at Harbor, so the Pod ends up in `ImagePullBackOff`. The
default posture is block at High-and-above, warn on Medium, with a per-project override to
tighten it further.
{{< /note >}}

4. Name the two ways to **remediate** a flagged image, and what to do when neither is
   possible yet.

{{< note >}}
**Answer:** Pick a **patched tag** (a newer tag whose packages already meet each finding's
`FixedVersion`), or **rebuild on a patched base** and re-scan. When no fix exists yet (an
empty `FixedVersion`) or one can't ship in time, request a **Security Exception** — a
time-boxed, approved waiver raised as an
[ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests). Fix if you can,
waive only if you must.
{{< /note >}}

## Knowledge Check

Prove it end to end: confirm the clean report you worked with still has a proper
severity summary.

```examiner:execute-test
name: verify-report-summary
title: Knowledge check — the clean report has a severity summary
args:
- scan-report.json
timeout: 10
```

## Next Steps

Later in the Developer track: **B05 — RBAC & Tenancy** moves on from "what can this image
do" to "who can do what in your namespace" — a different angle on the same access-control
thread you've now seen applied to Harbor's projects and robot accounts.
