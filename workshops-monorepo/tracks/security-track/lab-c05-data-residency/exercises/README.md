Exercise files for "EU Data-Residency & Compliance".

These are **read-only teaching fixtures** — you inspect them with `yq`/`grep`, you do not
deploy them:

- `data-classification-matrix.md` — a sample DCS data-classification matrix (levels,
  examples, allowed regions per level).
- `workload-classified.yaml` — a Deployment carrying a `data.dcs/classification` annotation
  and a region `nodeSelector` (image via `${DCS_REGISTRY}`).
- `raci.md` — a sample Responsibility Matrix (RACI) splitting platform vs tenant duties.

Nothing here needs to be applied to the cluster: residency is a platform guarantee, so these
fixtures illustrate how classification and placement are *expressed* and *governed*, not
something a session stands up.
