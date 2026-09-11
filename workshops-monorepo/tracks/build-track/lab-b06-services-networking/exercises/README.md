Exercise files for the Services & Cluster Networking workshop.

- `deployment.yaml`             — two replicas, so every Service has more than one endpoint.
- `service-clusterip.yaml`      — the default type: one virtual IP, load-balanced.
- `service-headless.yaml`       — `clusterIP: None`: one DNS record per ready Pod.
- `service-externalname.yaml`   — a CNAME: one stable in-cluster name for something elsewhere.
- `service-nodeport.yaml`       — applied to see what a node port does and does not buy you.
- `service-loadbalancer.yaml`   — applied to watch its external address never arrive.

Manifests carrying `${DCS_REGISTRY}` are applied with
`envsubst < <file> | oc apply -f -`, never with a plain `oc apply -f`.
