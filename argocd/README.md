# ArgoCD deployment

App-of-apps that pulls the three charts from
`https://github.com/rummens/Airbus-Educates` and deploys Educates on OpenShift.

```
argocd/
  root-app.yaml          # app-of-apps -> argocd/apps
  apps/
    01-kapp-controller.yaml     # sync-wave 0
    02-educates-platform.yaml   # sync-wave 1  (portal.enabled=false, auth.enabled=true)
    03-educates-workshops.yaml  # sync-wave 2  (vcluster.enabled=true)
```

## Prerequisites

1. **OpenShift GitOps** (ArgoCD) installed — namespace `openshift-gitops`.
2. **ArgoCD controller needs cluster-admin.** The platform installs CRDs, SCCs,
   and ClusterRoleBindings (including a cluster-admin binding for the Educates
   installer), so the ArgoCD application-controller SA must itself be cluster-admin:
   ```sh
   oc adm policy add-cluster-role-to-user cluster-admin \
     -z openshift-gitops-argocd-application-controller -n openshift-gitops
   ```
3. **Un-exclude APIService in the ArgoCD instance.** OpenShift GitOps excludes
   `apiregistration.k8s.io/APIService` by default, so it will silently skip
   kapp-controller's APIService and kapp-controller will crashloop
   (`APIService … not found`). Remove that one exclusion from the ArgoCD CR:
   ```sh
   # edit spec.resourceExclusions and delete the block with:
   #   apiGroups: [apiregistration.k8s.io]  kinds: [APIService]
   oc edit argocd openshift-gitops -n openshift-gitops
   ```
4. **Phase 2 cookie secret** (never committed as plaintext). Two options:

   **a) SealedSecret (commit-safe, preferred).** Needs the sealed-secrets
   controller. Generate the encrypted value and set it in the platform env file:
   ```sh
   VALUE=$(openssl rand -hex 16)   # 32 bytes; base64 32 = 44 bytes and FAILS
   echo -n "$VALUE" | kubeseal --raw --namespace educates --name educates-oauth-proxy
   ```
   Put the output under `auth.sealedSecret` in `argocd/envs/platform-<cluster>.yaml`:
   ```yaml
   auth:
     enabled: true
     existingSecret: ""            # leave empty; SealedSecret creates it
     sealedSecret:
       enabled: true
       encryptedCookieSecret: "<kubeseal output>"
   ```

   **b) Pre-created secret (no controller).** Create it once, out of git:
   ```sh
   oc create namespace educates --dry-run=client -o yaml | oc apply -f -
   oc create secret generic educates-oauth-proxy \
     --from-literal=cookie-secret="$(openssl rand -hex 16)" -n educates
   ```
   (Phase 1 only: set `auth.enabled: false` in the env file and skip this.)

### Per-cluster ingress

`ingressDomain` and the router `tlsCertificateRef` are **not** hardcoded in the
chart — they live in `argocd/envs/platform-<cluster>.yaml`, which the
`educates-platform` Application pulls via a multi-source `valueFiles` ref. Point
the Application at the right env file per cluster (`platform-x86.yaml` /
`platform-crc.yaml`); add a new file to onboard another cluster. (At larger scale,
swap the app-of-apps for an ApplicationSet with a cluster generator.)

## Deploy

```sh
oc apply -f argocd/root-app.yaml
```

ArgoCD then creates the three child apps and rolls them out in wave order:
kapp-controller → platform → workshops. Watch:

```sh
oc get applications -n openshift-gitops
```

Expected convergence (a few minutes; the platform App reconcile is the long pole):
- `kapp-controller` Healthy
- `educates-platform` Healthy (installer App = ReconcileSucceeded)
- `educates-workshops` Healthy (portal at `https://container-paas-ui.apps-crc.testing`,
  authed entry at `https://container-paas-secure.apps-crc.testing`)

## Why it converges cleanly

- **Sync waves** order rollout; on delete, ArgoCD tears down in **reverse** wave
  order — platform (App CR + finalizer) is removed *before* kapp-controller and
  while the installer ServiceAccount still exists, so the App finalizer's cleanup
  runs. (Deleting everything at once — e.g. `helm uninstall` — deadlocks the
  finalizer; ArgoCD's ordering avoids it.)
- **CRDs are async:** the Workshop/TrainingPortal CRs carry
  `SkipDryRunOnMissingResource=true`; combined with sync retry ArgoCD waits for
  the platform CRDs instead of hard-failing.
- **Layered reconcilers:** ArgoCD manages only the App CR + config + workshop CRs.
  kapp-controller owns the ~30 platform resources (invisible to ArgoCD, no diff
  churn). `ignoreDifferences` on the App + its tracking ConfigMap stop ArgoCD from
  fighting kapp-controller over co-owned fields.

## Air-gap

Add to each app's `helm.valuesObject`:
```yaml
global:
  registry:
    host: YOUR_REGISTRY
    pullSecret: mirror-pull   # platform/workshops only, if the mirror needs auth
```
Mirror images per each chart's README before syncing.

## Teardown

```sh
oc delete -f argocd/root-app.yaml
```
The `resources-finalizer.argocd.argoproj.io` on each app prunes its resources in
reverse wave order. Confirm the installer App is gone before the namespaces clear.
