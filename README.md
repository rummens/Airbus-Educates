# DCS Academy — Educates on OpenShift

GitOps-deployable [Educates](https://educates.dev) training platform for OpenShift,
split into three Helm charts + an ArgoCD app-of-apps. Runs online or fully
air-gapped (`global.registry.host`). Pinned to **Educates 3.7.2**.

## Charts

| Chart | What it does | Key namespaces |
|-------|--------------|----------------|
| [`dcs-academy-kapp-controller`](dcs-academy-kapp-controller) | Carvel kapp-controller (prereq that reconciles the Educates installer) | `kapp-controller` |
| [`dcs-academy-platform`](dcs-academy-platform) | Installs Educates (cluster-essentials + training-platform) + optional metrics/monitoring | `dcs-educates-installer`, `educates` |
| [`dcs-academy-portal`](dcs-academy-portal) | Workshops + TrainingPortal + custom UI + OpenShift-OAuth gate + feedback (CNPG) | `dcs-academy-portal`, portal at `academy.<domain>`, backend `dcst-dcs-backend-ui`, sessions `dcst-*` |

Every chart has a top-level `enabled: true` toggle (set `false` to render nothing).

## Namespaces

- **Static (platform)** → `dcs-*` (e.g. `dcs-educates-installer`, `dcs-educates`, `dcs-educates-workshops`, `dcs-academy-portal` = custom UI + oauth gate).
- **Dynamic (user sessions)** → `dcst-*` (from the portal name `dcst-dcs-backend`, e.g. `dcst-dcs-backend-w01-xxxx`, `...-vc`); the Educates backend runs in `dcst-dcs-backend-ui`.
- Educates' own operator namespace stays `educates` (created by the upstream installer).

## Deploy (ArgoCD — the target flow)

```sh
# Prereqs (see argocd/README.md): ArgoCD controller cluster-admin, un-exclude
# APIService in the ArgoCD CR, create the oauth cookie secret.
oc apply -f argocd/root-app.yaml
```

App-of-apps rolls out in order: kapp-controller → platform → portal.
Per-cluster settings (ingress domain, router cert) come from a shared env file
under `argocd/envs/` (referenced via `$values`); other overrides go in each app's
`helm.valuesObject`.

## Deploy (helm — dev/test)

```sh
helm install dcs-academy-kapp-controller ./dcs-academy-kapp-controller
helm install dcs-academy-platform ./dcs-academy-platform          # waits: installer App reconciles
helm install dcs-academy-portal ./dcs-academy-portal/chart --create-namespace -n dcs-academy-portal
```
Note for plain helm: teardown needs the installer App finalizer cleared first
(ArgoCD's wave ordering handles this).

## Auth (OpenShift SSO)

`dcs-academy-portal` fronts the custom portal with an `oauth-proxy` (SA-as-
OAuthClient) at `academy.<domain>` — unauthenticated users are auto-redirected to
OpenShift OAuth (your SSO). No self-signup (`registration: anonymous`). A
ValidatingAdmissionPolicy reserves the academy host so Educates' own auto-route is
denied; the proxy is the only entry. HostNetwork-router caveat: the `-ui`
NetworkPolicy can't block node-sourced router traffic, so the VAP is the
router-level enforcement.

## Workshops in vcluster or native

Default: every workshop gets a per-session vcluster. Opt a workshop **out** with
`session.vcluster: false` → runs in a native, isolated OpenShift session namespace
(for operator / SCC / namespace-UID topics). See workshops README.

## Offline / air-gap

Set `global.registry.host` on each chart and mirror the images in
[OFFLINE-MIRROR-IMAGES.md](OFFLINE-MIRROR-IMAGES.md).
