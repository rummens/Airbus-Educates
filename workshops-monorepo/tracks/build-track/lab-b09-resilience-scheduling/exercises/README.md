Exercise files for the Resilience & Scheduling workshop.

- `deployment.yaml`        — three replicas with `terminationGracePeriodSeconds` and a
  `preStop` hook, so shutdown is something you can watch rather than assume.
- `pdb.yaml`               — a PodDisruptionBudget: `minAvailable: 2`, the floor the
  platform must respect while it does maintenance.
- `deployment-spread.yaml` — the same app asking to be spread across nodes, with a
  `topologySpreadConstraint` and a preferred `podAntiAffinity`.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
