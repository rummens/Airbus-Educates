---
title: Summary
---

You went from "a gate can block an image" (A03) to reading the report behind the decision,
understanding the policy that makes it, and remediating a flagged image — the everyday
security loop on an air-gapped {{< param product_short >}}.

## What You Did

- Separated **vulnerability scanning** (CVEs in image layers) from **compliance scanning**
  (policy/config), and saw scan scope run **per-image, per-project, and global** — an image is
  re-evaluated as new CVEs appear, never "scanned once and done."
- Read a Harbor scan report with **`jq`** — the `severityCount` summary and the
  `vulnerabilities` findings (CVE `id`, `severity`, `package`, `FixedVersion`) — and used it
  as a risk summary.
- Read a **flagged** report (two Criticals) and traced what the **gate** does: it sits in the
  **pull path** and refuses the artifact, so the Pod sticks in `ImagePullBackOff`. Threshold
  policy: block at High-and-above, warn on Medium, per-project override.
- **Remediated** — patched tag or rebuild on a patched base — and confirmed the clean image is
  present (digest) with **zero Criticals** in its report, so it passes the gate.
- Learned the **Security Exception Process** (ITSM): a time-boxed, approved waiver for a
  specific finding when no fix is available yet — fix if you can, waive only if you must.

## Challenge

Do it yourself, unguided: **prove the remediated image would pass the gate.** Read
`scan-report.json` and confirm its Critical count is zero. Run the check when ready.

```examiner:execute-test
name: verify-no-criticals
title: Challenge — the clean report has zero Criticals
args:
- scan-report.json
timeout: 10
```

{{< note >}}
**Hint:** `jq '.summary.severityCount.Critical // 0' scan-report.json` — the `// 0` returns
`0` even if the key is absent. A gate that blocks on High-and-above lets a zero-Critical,
zero-High image through.
{{< /note >}}

## Check Your Understanding

1. What is the difference between **vulnerability** scanning and **compliance** scanning?

{{< note >}}
**Answer:** Vulnerability scanning matches the software in an image's layers against known
[CVEs](https://www.cve.org/) — "does this contain a known flaw?" Compliance scanning checks
the image against policy/configuration rules — "is it built the way policy requires?" (runs as
root, missing labels, forbidden base). An image can pass one and fail the other.
{{< /note >}}

2. What does a **scan gate** do, and what is the default {{< param product_short >}} threshold?

{{< note >}}
**Answer:** The gate sits in the pull path and **blocks** using an image whose scan findings
exceed a threshold — the pull is refused at Harbor, so the Pod ends up in `ImagePullBackOff`.
The default is **block at High-and-above, warn on Medium**, with a per-project override to
tighten it. See the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/registry/overview).
{{< /note >}}

3. Name the two ways to **remediate** a flagged image, and what to do when neither is possible
   yet.

{{< note >}}
**Answer:** Pick a **patched tag** (a newer tag whose packages already meet each finding's
`FixedVersion`), or **rebuild on a patched base** and re-scan. When no fix exists yet (empty
`FixedVersion`) or one can't ship in time, request a **Security Exception** — a time-boxed,
approved waiver raised as an [ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests)
under [governance]({{< param dcs_docs_base_url >}}/governance/overview). Fix if you can, waive
only if you must.
{{< /note >}}

## Next Steps

Later in the Security & Compliance track: **supply-chain security** (C04) builds directly on
this — it assumes you can read a scan report and know what the gate does, and adds image
signing and provenance on top.
