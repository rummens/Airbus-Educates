Exercise files for "Harbor & Image Scanning".

- `pod-from-catalog.yaml` — a Pod referencing `samples/hello-dcs:1.0` straight from Harbor
  (`${DCS_REGISTRY}` ref), to show a catalog pull landing on the cluster.
- `scan-report.json` — a clean-ish Harbor/Trivy-style scan report for `samples/hello-dcs:1.0`
  (a `summary.severityCount` object plus a `vulnerabilities` array of Low/Medium findings).
- `scan-report-flagged.json` — the same schema for an image the gate would block: 2 Critical
  and several High findings, each with a `FixedVersion`.
- `deploy-flagged.yaml` — a Deployment referencing a would-be-blocked tag, used to *narrate*
  the gate refusing a pull (observe/concept — not asserted against a scanner-less cluster).

**Live scan vs fixture.** A live, scanner-backed Harbor is not guaranteed reachable or
deterministic in every session, so the two `scan-report*.json` files are **static fixtures**
shipped here — reading them keeps every step in this workshop examiner-verifiable and
reproducible air-gapped. Where a scanner-backed Harbor *is* reachable in-session, the
equivalent live step is the same `jq` queries run against Harbor's scan-report API response
for the artifact instead of the fixture file — the page flow and the queries are identical
either way.
