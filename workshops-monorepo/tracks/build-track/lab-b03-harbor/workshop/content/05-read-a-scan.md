---
title: Read a Scan
---

Harbor scans what it stores. The report is a document you can read, and the gate is
arithmetic on one field of it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/scan
```

{{< note >}}
**📌 These reports are fixtures.** This training cluster has no scanner-backed registry
attached, so you read real report *structure* rather than a live scan. The fields and the
decision are what transfer.
{{< /note >}}

## A clean image

```editor:open-file
file: ~/exercises/scan-report.json
```

```terminal:execute
command: jq '{artifact, scanner: .scanner.name, summary}' exercises/scan-report.json 2>/dev/null || jq '{artifact, scanner: .scanner.name, summary}' ~/exercises/scan-report.json
```

```examiner:execute-test
name: verify-clean-summary
title: Verify you can read the clean image's severity summary
timeout: 60
retries: .INF
delay: 3
```

The `summary.severityCount` is the whole verdict in four numbers. This one has **no Critical
and no High** findings: one Medium and two Low.

Note `fixable`: of the three findings, two have a fixed version available. That distinction
decides what you can actually do about them.

## An image that fails the gate

```terminal:execute
command: jq '{artifact, summary}' ~/exercises/scan-report-flagged.json
```

```examiner:execute-test
name: verify-flagged-summary
title: Verify the flagged image's Critical findings are visible
timeout: 60
retries: .INF
delay: 3
```

**Two Critical, three High.** On {{< param product_short >}} a PROD project pulls only
images whose findings sit **below CVE severity 9**, and Critical means 9.0 and above, so this
image is refused there. It can sit in a DEV project without any trouble.

## Look at what is actually wrong

```terminal:execute
command: jq -r '.vulnerabilities[] | select(.severity=="Critical") | "\(.id)  \(.package) \(.installedVersion) → \(.FixedVersion // "no fix")"' ~/exercises/scan-report-flagged.json
```

```examiner:execute-test
name: verify-critical-detail
title: Verify the Critical findings can be listed with their packages
timeout: 60
retries: .INF
delay: 3
```

Each line is a decision:

- **A fixed version exists:** rebuild on an updated base, or bump the dependency. That covers
  most findings most of the time, which is why `fixable` is the number to read first.
- **No fix available:** then it is a conversation. Can the component be removed or replaced,
  or is this the **security exception** path?

{{< warning >}}
**⚠️ Watch out:** a scan result belongs to a **digest**, not to a tag. Re-pushing a different
image under the same tag does not inherit the old verdict, which is the other reason floating
tags are refused.
{{< /warning >}}

## The habit worth forming

Read the summary **before** you need it. Otherwise an image that fails the gate is
discovered at promotion time, which is a late moment to learn that your base image is two
years old.
