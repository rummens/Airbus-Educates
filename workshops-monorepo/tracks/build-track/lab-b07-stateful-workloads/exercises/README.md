Exercise files for the Stateful Workloads workshop.

- `service-headless.yaml` — the headless Service (`clusterIP: None`) that gives each
  replica its own DNS name. A StatefulSet needs one, named in `spec.serviceName`.
- `statefulset.yaml`      — two replicas, one PersistentVolumeClaim **per replica** from
  `volumeClaimTemplates`, mounted inside the image's writable home.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
