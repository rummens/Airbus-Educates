# dcs-academy-platform

Installs the [Educates](https://educates.dev) training **platform** (cluster
-essentials + training-platform) on OpenShift, plus optional CR metrics /
monitoring. **Platform-only** — the Workshops, TrainingPortal, custom UI, and the
OpenShift-OAuth gate live in [`dcs-academy-portal`](../dcs-academy-portal).

Pinned to **Educates 3.7.2**. Deploy this first, then the portal chart.

> New here? Read [architecture.md](architecture.md) for how all charts, CRDs, and the
> GitOps layers fit together.

## How it installs Educates

Educates ships as Carvel imgpkg bundles, not a Helm chart. This chart renders the
official **kapp-controller `App`** (fetches `ghcr.io/educates/educates-installer`,
templates with ytt using a config Secret built from values, resolves images with
kbld, deploys with kapp) plus its RBAC and config. One App installs both packages.
Requires **kapp-controller** ([`dcs-academy-kapp-controller`](../dcs-academy-kapp-controller)).

## Namespaces

- `dcs-educates-installer` (static, `dcs-`) — the installer App + RBAC + config.
- `educates` — Educates operator namespace, created by the upstream installer.

## Values (defaults are the x86 test cluster — override per cluster)

| Value | Default | Purpose |
|-------|---------|---------|
| `enabled` | `true` | Master switch; `false` renders nothing. |
| `global.registry.host` | `""` | Empty = upstream; set = rewrite all images (air-gap). |
| `global.registry.pullSecret` | `""` | Existing pull secret for the mirror. |
| `educates.version` | `3.7.2` | Educates release / bundle tag. |
| `educates.ingressDomain` | `apps.test.ocp.globomantics.com` | Cluster wildcard domain. |
| `educates.ingress.tlsCertificateRef` | `globomantics-ingress-cert` / `openshift-ingress` | Router wildcard cert (edge TLS on all Educates ingresses). |
| `educates.security.policyEngine` | `security-context-constraints` | Forced on OpenShift. |
| `educates.security.rulesEngine` | `none` | Kyverno off on OpenShift. |
| `educates.theming.*` | off | Brand color + logo stubs → Educates `websiteStyling`. |
| `monitoring.*` | on | CR metrics (kube-state-metrics) + ServiceMonitor + Grafana reader. |

## Install (helm)

```sh
helm install dcs-academy-platform ./dcs-academy-platform
oc get app.kappctrl.k14s.io installer.educates.dev -n dcs-educates-installer -w   # ReconcileSucceeded
oc get pods -n educates
```

For ArgoCD see [../argocd](../argocd) (app `dcs-academy-platform`, ns `dcs-educates`).

## Offline / air-gap

Set `global.registry.host` and mirror the images in
[../OFFLINE-MIRROR-IMAGES.md](../OFFLINE-MIRROR-IMAGES.md). The installer bundle is
relocated with `imgpkg copy` (carries every platform image); kbld resolves them
from the mirror.

## Security grants

| Kind | Name | Scope | Reason |
|------|------|-------|--------|
| ClusterRoleBinding | `educates-installer` → `cluster-admin` | cluster | The installer creates CRDs, cluster packages, operators, SCCs. Mirrors upstream installer RBAC. |
| ServiceAccount | `educates-installer` | `dcs-educates-installer` | Identity kapp-controller runs the installer App as. |
| ClusterRole/Binding + SA | `educates-metrics`, `grafana-reader` | cluster/ns | Read-only CR metrics + Thanos read for Grafana (monitoring, gated). |

Educates itself creates workshop-session SCCs/RBAC internally, governed by
`clusterSecurity.policyEngine: security-context-constraints`.

## Teardown

Under ArgoCD, delete the Application (wave order clears the App finalizer first).
Plain `helm uninstall` deletes the installer SA + App together and **deadlocks the
App finalizer** — clear it first, then purge orphaned Educates CRDs/ns/SCCs:

```sh
oc patch app.kappctrl.k14s.io installer.educates.dev -n dcs-educates-installer \
  -p '{"metadata":{"finalizers":[]}}' --type=merge
```
