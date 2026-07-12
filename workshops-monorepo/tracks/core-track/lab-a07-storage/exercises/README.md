Exercise files for "Storage on DCS".

- `pvc-file.yaml` — a PersistentVolumeClaim for **File** storage (RWX), using the
  `${DCS_SC_FILE}` storage class.
- `pvc-block.yaml` — a PersistentVolumeClaim for **Block** storage (RWO), using the
  `${DCS_SC_BLOCK}` storage class (used in the summary challenge).
- `hello-dcs-with-volume.yaml` — the A02 sample Deployment with the File PVC mounted at `/data`.

The manifests use the `${DCS_REGISTRY}`, `${DCS_SC_FILE}` and `${DCS_SC_BLOCK}` environment
variables so nothing is tied to a specific registry or storage-class name; apply them with
`envsubst` (the instructions do this for you).
