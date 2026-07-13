---
title: Read a Scan Report
---

Time to read an actual report. Harbor stores a scan result as JSON against each artifact —
you'll work with a saved report for the `samples/hello-dcs:1.0` image you already know from
A04. It's shipped as a fixture so you can read it the same way every time, air-gapped.

## Open the report

Open the report in the editor and look at its shape:

```editor:open-file
file: ~/exercises/scan-report.json
```

Two parts matter. A **`summary`** block with a `severityCount` — how many findings at each
severity — and a **`vulnerabilities`** array, one object per finding. Each finding carries an
`id` (the CVE), a `severity`, the `package` it's in, the `installedVersion`, and a
`FixedVersion` (empty when no fix exists yet). That's the whole vocabulary of a scan report.

## Summarise the risk

You rarely read every finding first — you start with the counts. Ask `jq` for the summary:

```terminal:execute
command: |-
  jq '.summary.severityCount' scan-report.json
```

You should see the per-severity tally, for example:

```
{
  "Critical": 0,
  "High": 0,
  "Medium": 2,
  "Low": 3
}
```

Zero Critical, zero High — that's the headline. For a gate that blocks on High-and-above,
this image is fine.

```examiner:execute-test
name: verify-report-summary
title: The report has a severity summary
args:
- scan-report.json
timeout: 10
```

## List the findings

Now the detail. Print one line per finding — severity, CVE ID, and package:

```terminal:execute
command: |-
  jq -r '.vulnerabilities[] | "\(.severity)\t\(.id)\t\(.package)"' scan-report.json
```

Each line is one CVE the scanner matched, for example:

```
Medium	CVE-2024-2961	glibc
Medium	CVE-2023-4813	glibc
Low	CVE-2023-29491	ncurses
Low	CVE-2024-0553	gnutls
Low	CVE-2023-5981	gnutls
```

```examiner:execute-test
name: verify-report-cves
title: The report lists CVE findings
args:
- scan-report.json
timeout: 10
```

## Reading it as a risk summary

The counts tell you *whether* to worry; the findings tell you *what about*. Two things to
read every time:

- **Severity** drives the decision — a Critical is release-blocking, a Low is usually
  informational. The gate acts on severity, not on the raw count.
- **`FixedVersion`** tells you whether you *can* act. A finding with a fixed version is
  remediable now — update the package or the base image. A finding with an **empty**
  `FixedVersion` (like `CVE-2023-5981` above) has no upstream fix yet; you can't patch your
  way out of it, which is exactly when the exception process on page 4 comes in.

This image is clean enough to pass. On the next page you'll read a report that isn't — and
watch the gate act on it.
