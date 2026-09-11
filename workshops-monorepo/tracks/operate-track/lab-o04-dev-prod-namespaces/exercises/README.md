Exercise files for the DEV vs PROD Namespaces workshop.

- `hello-dcs-unsized.yaml` — the app with **no** `resources` block: fine in DEV, refused by PROD.
- `hello-dcs-sized.yaml`   — the same app with requests and limits. The only difference.
- `service.yaml`           — something for the Route to point at.
- `route.yaml`             — applied in **both** namespaces, unchanged, with two different outcomes.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f - -n <namespace>`, never with a plain `oc apply -f`.
