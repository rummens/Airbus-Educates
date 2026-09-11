# DCS Data Classification Matrix (sample)

A **teaching fixture** — a simplified illustration of how DCS classifies data and which
regions each classification may reside in. The authoritative matrix lives in the DCS
governance documentation.

| Classification | Description | Example data | Allowed region(s) |
|---|---|---|---|
| PUBLIC | Non-sensitive, publicly releasable | Product brochures, open docs | eu-de, eu-es |
| INTERNAL | Internal use; low impact if disclosed | Team wikis, build logs | eu-de, eu-es |
| CONFIDENTIAL | Sensitive; disclosure harms the business or partners | Contracts, design data | eu-de |
| RESTRICTED | Highly sensitive; national / programme-restricted | Export-controlled, classified programme data | eu-de |

## How to read it

- **Classification** — the sensitivity level assigned to the data a workload handles.
- **Allowed region(s)** — the DCS regions in which data of that classification may be stored
  and processed. Higher classifications are pinned to fewer regions.
- **Residency guarantee** — DCS keeps data of a given classification inside its permitted
  region(s). Because the platform is **on-prem and air-gapped**, there is no path for the
  data to leave: the guarantee is structural, not just policy.

Regions in this fixture (`eu-de` = Germany, `eu-es` = Spain) are examples of the
multi-national European footprint.
