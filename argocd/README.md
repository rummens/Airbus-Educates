# ArgoCD deployment

App-of-apps that pulls the three charts from
`https://github.com/rummens/Airbus-Educates` and deploys DCS Academy on OpenShift.

```
argocd/
  root-app.yaml          # app-of-apps -> argocd/apps
  apps/
    01-kapp-controller.yaml     # sync-wave 0 -> dcs-academy-kapp-controller
    02-educates-platform.yaml   # sync-wave 1 -> dcs-academy-platform  (ns dcs-educates)
    04-academy-portal.yaml      # sync-wave 2 -> dcs-academy-portal    (ns dcs-academy-portal; UI + oauth gate)
    03-educates-workshops.yaml  # sync-wave 3 -> dcs-academy-workshops (ns dcs-educates-workshops)
```

Per-cluster settings (ingress domain, router cert, auth/vcluster toggles) are
**chart defaults** now — the apps are single-source (no env files). Override per
cluster via each Application's `spec.source.helm.valuesObject`.

## Prerequisites

1. **OpenShift GitOps** (ArgoCD) installed — namespace `openshift-gitops`.
2. **ArgoCD controller needs cluster-admin** (installs CRDs, SCCs, cluster-admin binding):
   ```sh
   oc adm policy add-cluster-role-to-user cluster-admin \
     -z openshift-gitops-argocd-application-controller -n openshift-gitops
   ```
3. **Un-exclude APIService in the ArgoCD CR** — OpenShift GitOps excludes
   `apiregistration.k8s.io/APIService` by default, which makes kapp-controller
   crashloop. Remove that block:
   ```sh
   oc edit argocd openshift-gitops -n openshift-gitops   # delete the apiregistration/APIService exclusion
   ```
4. **oauth cookie secret** (never committed) in the portal namespace:
   ```sh
   oc create namespace dcs-academy-portal --dry-run=client -o yaml | oc apply -f -
   oc create secret generic oauth-proxy \
     --from-literal=cookie-secret="$(openssl rand -hex 16)" -n dcs-academy-portal
   ```
   (16/24/32 bytes required — `-hex 16` = 32B; `base64 32` = 44B and fails. Or use
   the SealedSecret: `auth.sealedSecret.enabled=true` on the portal chart.)

## Deploy

```sh
oc apply -f argocd/root-app.yaml
oc get applications -n openshift-gitops
```

Expected: `dcs-academy-kapp-controller`, `dcs-academy-platform`,
`dcs-academy-portal`, `dcs-academy-workshops` all Synced/Healthy. Platform reconcile
(installer App) is the long pole (a few minutes). Portal at
`https://academy.<domain>` → OpenShift OAuth.

## Why it converges cleanly

- **Sync waves** order rollout; on delete, teardown runs in reverse (App CR before
  its SA) so the installer App finalizer can clean up (avoids the finalizer
  deadlock that plain `helm uninstall` hits).
- **Async CRDs:** Workshop/TrainingPortal carry `SkipDryRunOnMissingResource=true`
  + retry, so ArgoCD waits for the platform CRDs instead of hard-failing.
- **Auth route precedence:** the portal app (wave 2, incl. oauth-proxy + the
  host-reservation VAP) syncs before the workshops app (wave 3) creates the
  TrainingPortal, so the proxy claims `academy.<domain>` and the VAP denies
  Educates' own auto-published portal route for that host — the proxy is the only
  entry (see dcs-academy-portal chart).
- **Layered reconcilers:** ArgoCD manages the App CR + config + CRs; kapp-controller
  owns the platform resources (invisible to ArgoCD). `ignoreDifferences` on the App
  + tracking ConfigMap stop churn.

## Per-cluster override example

```yaml
# in apps/02-educates-platform.yaml
spec:
  source:
    helm:
      valuesObject:
        educates:
          ingressDomain: apps.mycluster.example.com
          ingress:
            tlsCertificateRef: { name: my-router-cert, namespace: openshift-ingress }
```

## Air-gap

Add `global.registry.host` (+ `pullSecret`) to each app's `valuesObject` and
mirror [../OFFLINE-MIRROR-IMAGES.md](../OFFLINE-MIRROR-IMAGES.md).

## Teardown

```sh
oc delete -f argocd/root-app.yaml
```
Finalizers prune in reverse wave order. Confirm the installer App is gone before
namespaces clear.
