Exercise files for the Harbor workshop.

- `scan-report.json`         — a vulnerability report for a clean image, in the shape Harbor's
  scanner produces. Read with `jq`.
- `scan-report-flagged.json` — the same report for an image that would **not** pass the PROD
  gate: two Critical findings.

The reports are fixtures. This training cluster has no scanner-backed registry attached, so
the lab reads real report structure rather than pretending to run a scan — the fields, the
severity counts and the gate arithmetic are the parts you need.
