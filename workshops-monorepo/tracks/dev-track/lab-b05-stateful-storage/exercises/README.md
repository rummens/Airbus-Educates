Exercise files for "Stateful Workloads & Storage".

- `pvc.yaml` — a PersistentVolumeClaim (`hello-dcs-data`, RWO, 1Gi) using the
  `${DCS_STORAGE_CLASS}` storage class.
- `deployment-stateful.yaml` — the `hello-dcs` Deployment with the PVC mounted at `/data`.

The manifests use the `${DCS_REGISTRY}` and `${DCS_STORAGE_CLASS}` environment variables so
nothing is tied to a specific registry or storage-class name; apply them with `envsubst`
(the instructions do this for you).
