# DCS Responsibility Matrix — RACI (sample)

A **teaching fixture** — a simplified slice of the DCS Responsibility Matrix. It shows the
split between what the **platform** operates and what the **tenant** owns. The authoritative
matrix lives in the DCS governance documentation.

RACI = **R**esponsible, **A**ccountable, **C**onsulted, **I**nformed.

| Activity | Platform | Tenant |
|---|---|---|
| Physical & regional infrastructure (data-residency guarantee) | A/R | I |
| Node region topology labels | A/R | I |
| Cluster-wide security controls (Kyverno, scanning gates) | A/R | C |
| Classifying the data a workload handles | C | A/R |
| Tagging workloads with their data classification | I | A/R |
| Placing workloads in a permitted region (nodeSelector/affinity) | C | A/R |
| Requesting a security exception (via ITSM) | C | A/R |
| Accepting the Terms & Conditions for the tenant's namespaces | I | A/R |

## The split in one line

The **platform** guarantees *where* data can live and enforces the controls around it; the
**tenant** is responsible for *classifying* its data, *tagging and placing* its workloads
accordingly, and *requesting exceptions* when a control can't be met.
