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

**Harbor "replication" is not enough for the installer bundle.** It copies image
tags but does NOT rewrite the bundle's internal ImagesLock or write the
ImageLocations metadata kbld needs — so the install still resolves the bundle's
inner refs to ghcr.io. Only `imgpkg copy` relocates a bundle correctly. Two ways:

- **From a workstation / CI** — [../mirror-educates-bundle.sh](../mirror-educates-bundle.sh)
  (needs the `imgpkg` binary; no container engine, but ~4 GB RAM + ~20 GB disk).
- **In-cluster Job (recommended, air-gap-friendly)** — enable `bundleMirror`. The
  chart runs the [`images/educates-mirror`](../images/educates-mirror) image (imgpkg
  baked in) as an ArgoCD sync-hook Job that relocates the bundle into your registry.
  Idempotent (re-runs are a cheap no-op). This is what to use when a DevSpace/pod was
  too small to run imgpkg by hand.

  PUSH creds are supplied as a **SealedSecret** — seal them once with `kubeseal`
  (scoped to the target name+namespace) and paste the encrypted strings into values;
  safe to commit, only the cluster's sealed-secrets controller can decrypt them:
  ```sh
  echo -n '<robot-user>'  | kubeseal --raw --name educates-mirror-creds --namespace dcs-educates-installer
  echo -n '<robot-token>' | kubeseal --raw --name educates-mirror-creds --namespace dcs-educates-installer
  ```
  ```yaml
  global:
    registry:
      host: "registry.example/dcs-internal-images"   # destination (also where the install pulls)
  bundleMirror:
    enabled: true
    # hook defaults to PostSync so the SealedSecret is unsealed before the Job runs.
    registryCredsSecret: educates-mirror-creds        # Secret name the values are sealed against
    sealedRegistryCredentials:
      username: "AgB...<kubeseal --raw output for the user>..."
      password: "AgC...<kubeseal --raw output for the token>..."
    proxy:
      httpsProxy: "http://proxy.corp:3128"            # egress to ghcr.io for the SOURCE bundle
      noProxy: ".svc,registry.example"
  ```
  The chart renders a `SealedSecret`; the controller unseals it into
  `educates-mirror-creds` (keys `username`/`password`) which the Job mounts. Requires
  the **sealed-secrets controller** on the cluster. (Prefer to manage the Secret
  yourself? Leave `sealedRegistryCredentials` empty and `oc create secret generic
  educates-mirror-creds …` out-of-band — then you may also use `hook: PreSync`.)

  **Creds are optional.** Set `registryCredsSecret: ""` to run the Job with no creds
  env (anonymous/ambient auth) if your registry accepts the push that way.

  **Docker Hub rate limit.** The bundle pulls a couple of `docker.io` images, and
  anonymous pulls hit Docker Hub's limit (`toomanyrequests`). Provide a Docker Hub
  PAT — same shape as the push creds (existing Secret or SealedSecret):
  ```yaml
  bundleMirror:
    dockerHubCredsSecret: educates-dockerhub-creds
    sealedDockerHubCredentials:            # or pre-create the Secret yourself
      username: "AgB...<kubeseal --raw for the docker hub user>..."
      password: "AgC...<kubeseal --raw for the docker hub PAT>..."
  ```
  It's wired as `IMGPKG_REGISTRY_*_1` for `index.docker.io` (the push creds are `_0` —
  keep them set). The Job logs each login (host + user, never the password), calling
  out the destination push target, so you can confirm auth in `oc logs`.

  **Private CA (internal registry / proxy behind your own CA).** Two options:
  ```yaml
  bundleMirror:
    trustClusterCABundle: true    # preferred: inject the OpenShift trust bundle
    # insecureSkipTLSVerify: true # last resort: imgpkg --registry-verify-certs=false
  ```
  `trustClusterCABundle` creates a ConfigMap labelled
  `config.openshift.io/inject-trusted-cabundle=true` (the Cluster Network Operator
  fills it with the system + your custom cluster CAs), mounts it into the Job, and
  points imgpkg at it via `SSL_CERT_FILE` — so TLS to a private registry **or** the
  egress proxy validates while public (ghcr) TLS still works. Keep `hook: PostSync`
  (default) so the bundle is populated before the Job runs.

  Mirror the small `educates-mirror` image itself into your registry first (plain
  image — Harbor replication is fine) so the Job can pull it in the air gap. Source
  bundle stays `ghcr.io/educates/educates-installer:<version>`; destination is
  `<host>/educates/educates-installer:<version>`, which is exactly what the installer
  App pulls once `global.registry.host` is set.

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
