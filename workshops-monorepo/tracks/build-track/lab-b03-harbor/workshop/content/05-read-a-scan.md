---
title: Read a Scan
---

Harbor scans what it stores. The report is a document you can read — and the gate is
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
and no High** findings — a Medium and two Low.

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

**Two Critical, three High.** On {{< param product_short >}} a PROD project pulls only images
whose findings sit **below CVE severity 9** — Critical is 9.0 and above, so this image is
refused there. It can live in a DEV project quite happily.

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

- **A fixed version exists** — rebuild on an updated base, or bump the dependency. This is most
  of them, most of the time, and it is why `fixable` is the number to look at first.
- **No fix available** — then it is a conversation: can the component be removed, replaced, or
  is this the **security exception** path?

{{< warning >}}
**⚠️ Watch out:** a scan result belongs to a **digest**, not a tag. Re-pushing a different image
under the same tag does not inherit the old verdict — which is the other reason floating tags
are refused.
{{< /warning >}}

## The habit worth forming

Read the summary **before** you need it. An image that fails the gate is discovered at
promotion time, which is the worst possible moment to learn that your base image is two years
old.
