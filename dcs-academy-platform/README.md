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
| `educates.ingress.caCertificate` / `caCertificateRef` / `caFromClusterBundle` | `""` / `""` / `false` | Extra trusted CA for **workshop sessions** — inline PEM, an existing `ca.crt` Secret, or (recommended) sync from the OpenShift cluster trust bundle. Educates mounts it into the session trust store **and the vendir content-download step**, so `spec.workshop.files` git/http pulls from a private-CA host (GitLab/Harbor) pass TLS. See [Private CA for workshop content](#private-ca-for-workshop-content). |
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

## Private CA for workshop content

**Symptom:** sessions never load content; the workshop-download step fails with an
x509 "certificate signed by unknown authority" against your GitLab (or Harbor). The
container fetching `spec.workshop.files` doesn't trust your internal CA.

**How the fix works:** whenever a trusted CA is configured (any of the three ways
below), Educates' session-manager adds a `ca-trust-store-initialization` init
container that builds it into a shared `/etc/pki/ca-trust` volume and mounts that into
**both** the workshop container **and** the `workshop-downloads-initialization`
(vendir) container — so git/http pulls over HTTPS validate. Verified against the
operator's `session-manager/handlers/workshopsession.py` (the CA-trust mounts are
gated on this being set). One knob covers every workshop — no per-lab patch or session
ConfigMap.

**Pick how you supply the CA** (first non-empty wins; none commits secrets you care
about to git except option 1):

1. **Inline PEM** — `educates.ingress.caCertificate`. Simplest, but puts the cert in git.
2. **Existing Secret** — `educates.ingress.caCertificateRef: {name, namespace}`, a Secret
   with a `ca.crt` key you create out-of-band:
   ```sh
   oc create secret generic org-ca -n dcs-educates-installer --from-file=ca.crt=org-ca.pem
   ```
   Cert stays out of git.
3. **Let OpenShift own it (recommended)** — `educates.ingress.caFromClusterBundle: true`.
   The chart creates a ConfigMap labelled `config.openshift.io/inject-trusted-cabundle=true`
   (the Cluster Network Operator fills `ca-bundle.crt` with the system CAs plus any custom
   CA you added cluster-wide via Proxy `spec.trustedCA`), and a small PostSync hook Job
   copies that bundle into the `educates-cluster-ca` Secret's `ca.crt` that Educates reads.
   Nothing in git; the cluster trust bundle is the source of truth. The copy exists because
   Educates reads a **Secret**, not the injected **ConfigMap**; the Job re-runs each sync,
   so force a sync (or add a CronJob) after a CA rotation.

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
