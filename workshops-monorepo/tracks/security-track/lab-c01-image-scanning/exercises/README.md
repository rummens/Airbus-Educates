Exercise files for "Image Scanning & Harbor Gates".

- `scan-report.json` — a clean-ish Harbor/Trivy-style scan report for `samples/hello-dcs:1.0`
  (a `summary.severityCount` object plus a `vulnerabilities` array of Low/Medium findings).
- `scan-report-flagged.json` — the same schema for an image the gate would block: 2 Critical
  and several High findings, each with a `FixedVersion`.
- `deploy-flagged.yaml` — a Deployment referencing a would-be-blocked tag, used to *narrate*
  the gate refusing a pull (observe/concept — not asserted against a scanner-less cluster).

The reports are **static fixtures**: a live Harbor scanner is not guaranteed reachable or
deterministic in-session, so shipping the reports keeps every step examiner-verifiable on an
air-gapped platform. Read them with `jq` — the `jq` queries in the instructions match this
schema exactly.
