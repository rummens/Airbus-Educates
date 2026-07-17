---
title: Read a Scan Report
---

Every artifact that lands in Harbor is scanned automatically, and "scanned" actually means
two different questions get asked.

## Two kinds of scan

**Vulnerability scanning** asks: *does this image contain software with a known security
flaw?* A scanner such as [Trivy](https://trivy.dev/) reads every package baked into every
image layer and matches it against public vulnerability databases. A match is a **CVE** —
a [Common Vulnerabilities and Exposures](https://www.cve.org/) identifier, e.g.
`CVE-2021-3711` — with a **severity** (Critical / High / Medium / Low) and, usually, the
package version that fixes it.

**Compliance scanning** asks a different question: *is this image built the way policy
requires?* Not "is there a known bug" but "does it break a rule" — running as root, a
missing required label, a forbidden base image. The findings aren't CVEs; they're policy
violations. An image can be perfectly clean on vulnerabilities and still fail compliance,
or the other way round.

Both run at more than one scope: **per-image** (the report you're about to read, for one
tag/digest) and **per-project** (a Harbor project like `samples` can require everything in
it to be scanned, rolling findings up so a team sees its whole footprint at a glance).

{{< note >}}
The **live path**: where a scanner-backed Harbor is reachable in-session, the same `jq`
queries below run against Harbor's scan-report API response for the artifact instead of a
file. This workshop ships the report as a fixture so every step here is reproducible and
examiner-verifiable air-gapped — the queries are identical either way.
{{< /note >}}

## Open the report

`scan-report.json` is a saved vulnerability-scan result for `samples/hello-dcs:1.0` — the
image you've been inspecting and pulling all workshop. Open it and look at its shape:

```editor:open-file
file: ~/exercises/scan-report.json
```

Two parts matter: a **`summary`** block with a `severityCount` — how many findings at each
severity — and a **`vulnerabilities`** array, one object per finding. Each finding carries
an `id` (the CVE), a `severity`, the `package` it's in, the `installedVersion`, and a
`FixedVersion` (empty when no fix exists yet). That's the whole vocabulary of a scan
report.

## Summarise the risk

You rarely read every finding first — you start with the counts, using
[`jq`](https://jqlang.github.io/jq/) — a command-line JSON processor — to pull just the
field you need out of the report:

```terminal:execute
command: |-
  jq '.summary.severityCount' scan-report.json
```

You should see the per-severity tally:

```
{
  "Critical": 0,
  "High": 0,
  "Medium": 1,
  "Low": 2
}
```

Zero Critical, zero High — for a gate that blocks on High-and-above (the next page), this
image is fine.

```examiner:execute-test
name: verify-report-summary
title: The report has a severity summary
args:
- scan-report.json
timeout: 10
```

## List the findings

Now the detail — one line per finding: severity, CVE ID, package. The `-r` flag tells `jq`
to print **raw** strings rather than JSON-quoted ones, so the output reads as plain text
instead of `"like\tthis"`:

```terminal:execute
command: |-
  jq -r '.vulnerabilities[] | "\(.severity)\t\(.id)\t\(.package)"' scan-report.json
```

```
Medium	CVE-2024-2961	glibc
Low	CVE-2023-29491	ncurses
Low	CVE-2023-5981	gnutls
```

```examiner:execute-test
name: verify-report-cves
title: The report lists CVE findings
args:
- scan-report.json
timeout: 10
```

**`FixedVersion`** is the field to watch: `CVE-2024-2961` and `CVE-2023-29491` both list one
— a newer package version clears them, so they're actionable now. `CVE-2023-5981` has an
**empty** `FixedVersion` — no upstream fix exists yet. You can't patch your way out of that
one; it's exactly the case the exception process (page 6) exists for.

This image's report is clean enough to pass. Next, one that isn't.
