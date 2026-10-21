---
title: Read a Scan
---

Harbor scans what it stores. The report is a JSON document. The PROD gate compares one field
in it, the severity count, with the threshold.

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
command: jq '{artifact, scanner: .scanner.name, summary}' ~/exercises/scan-report.json
```

```section:begin
name: breakdown-summarise-report
prefix: Breakdown
title: What each part of the command does
```

- **`jq '{…}'`** — builds a smaller JSON object from the report.
- **`artifact`, `summary`** — copies those two fields across unchanged.
- **`scanner: .scanner.name`** — adds a field `scanner` holding only the scanner's name.
- **`~/exercises/scan-report.json`** — the report, by its full path, so the command works whichever directory the terminal is in.

```section:end
name: breakdown-summarise-report
```

```examiner:execute-test
name: verify-clean-summary
title: Verify you can read the clean image's severity summary
timeout: 60
retries: .INF
delay: 3
```

`summary.severityCount` gives the number of findings at each of the four severity levels. This one has **no Critical
and no High** findings: one Medium and two Low.

Note `fixable`: of the three findings, two have a fixed version available. Whether a fix exists
decides what you can do about each finding.

## An image that fails the gate

```terminal:execute
command: jq '{artifact, summary}' ~/exercises/scan-report-flagged.json
```

```section:begin
name: breakdown-summarise-flagged
prefix: Breakdown
title: What each part of the command does
```

- **`jq '{artifact, summary}'`** — prints a smaller JSON object with only the `artifact` and `summary` fields.
- **`~/exercises/scan-report-flagged.json`** — the second report, for the image that fails the gate.

```section:end
name: breakdown-summarise-flagged
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

## List the Critical findings

```terminal:execute
command: jq -r '.vulnerabilities[] | select(.severity=="Critical") | "\(.id)  \(.package) \(.installedVersion) → \(.FixedVersion // "no fix")"' ~/exercises/scan-report-flagged.json
```

```section:begin
name: breakdown-list-criticals
prefix: Breakdown
title: What each part of the command does
```

- **`jq -r`** — runs the filter and prints plain text, without JSON quotes.
- **`.vulnerabilities[]`** — goes through each finding in the list.
- **`| select(.severity=="Critical")`** — keeps only the findings rated Critical.
- **`| "\(.id)  \(.package) \(.installedVersion) → …"`** — prints one line per finding. Each `\( … )` inserts a field: the CVE id, the package and its installed version.
- **`.FixedVersion // "no fix"`** — the version that fixes it, or `no fix` when the field is missing or empty.

```section:end
name: breakdown-list-criticals
```

```examiner:execute-test
name: verify-critical-detail
title: Verify the Critical findings can be listed with their packages
timeout: 60
retries: .INF
delay: 3
```

For each finding, decide:

- **A fixed version exists:** rebuild on an updated base, or bump the dependency. That covers
  most findings most of the time, which is why `fixable` is the number to read first.
- **No fix available:** find out whether the component can be removed or replaced, or request
  a **security exception**.

{{< warning >}}
**⚠️ Watch out:** a scan result belongs to a **digest**, not to a tag. Re-pushing a different
image under the same tag does not inherit the old verdict, which is the other reason floating
tags are refused.
{{< /warning >}}

## Check scans early

Read the scan summary while you are still in DEV. Otherwise a failing image is only found at
promotion time, for example because the base image is outdated.
