# Offline image mirror list

All images required to run the DCS Academy (Educates 3.7.2) fully air-gapped.
Pinned to what the charts deploy today. After mirroring, set
`global.registry.host=<your-registry>` in each chart (see chart READMEs).

Two ways to get the **platform** images:

- **Recommended — relocate the installer bundle** (carries every platform image,
  all session/base/JDK images, docker-in-docker, debian, and all loft-sh vcluster
  images in one shot, with digests):
  ```sh
  imgpkg copy -b ghcr.io/educates/educates-installer:3.7.2 \
    --to-repo <your-registry>/educates/educates-installer
  ```
- **Or mirror the explicit refs below** (for a `skopeo`/`oc image mirror` job).

Everything NOT in the installer bundle (kapp-controller, oauth-proxy,
kube-state-metrics, workshop content + workshop app images) must be mirrored
explicitly regardless.

---

## Plain list (feed to your mirror job)

```
# --- Prerequisite: kapp-controller (dcs-academy-kapp-controller) ---
ghcr.io/carvel-dev/kapp-controller@sha256:610a14076cfe8864cd0bd961277b8c239298ab418234a1a8c324f2f5792c9b1d

# --- Educates installer bundle (dcs-academy-platform) ---
ghcr.io/educates/educates-installer:3.7.2

# --- Educates platform images (carried by the bundle; listed for an explicit job) ---
ghcr.io/educates/educates-session-manager:3.7.2
ghcr.io/educates/educates-training-portal:3.7.2
ghcr.io/educates/educates-docker-registry:3.7.2
ghcr.io/educates/educates-pause-container:3.7.2
ghcr.io/educates/educates-base-environment:3.7.2
ghcr.io/educates/educates-jdk8-environment:3.7.2
ghcr.io/educates/educates-jdk11-environment:3.7.2
ghcr.io/educates/educates-jdk17-environment:3.7.2
ghcr.io/educates/educates-jdk21-environment:3.7.2
ghcr.io/educates/educates-conda-environment:3.7.2
ghcr.io/educates/educates-secrets-manager:3.7.2
ghcr.io/educates/educates-tunnel-manager:3.7.2
ghcr.io/educates/educates-image-cache:3.7.2
ghcr.io/educates/educates-assets-server:3.7.2
ghcr.io/educates/educates-lookup-service:3.7.2
ghcr.io/educates/educates-node-ca-injector:3.7.2

# --- Platform external deps (carried by the bundle) ---
debian:sid-20230502-slim
docker:27.5.1-dind

# --- vcluster images (carried by the bundle; needed only if vcluster.enabled) ---
ghcr.io/loft-sh/kubernetes:v1.31.1
ghcr.io/loft-sh/kubernetes:v1.32.1
ghcr.io/loft-sh/kubernetes:v1.33.4
ghcr.io/loft-sh/kubernetes:v1.34.0
ghcr.io/loft-sh/vcluster-oss:0.30.2

# --- Auth (dcs-academy-workshops, auth.enabled) ---
registry.redhat.io/openshift4/ose-oauth-proxy:v4.14

# --- Monitoring (dcs-academy-platform, monitoring.enabled) ---
registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.14.0

# --- Workshop content image (per workshop; only needed with source.type=image) ---
ghcr.io/educates/lab-k8s-fundamentals-files:8.1

# --- Workshop APP images (deployed BY lab-k8s-fundamentals content) ---
ghcr.io/educates/lab-k8s-fundamentals-frontend:3.0
postgres:17.7
redis:8.6.2
```

---

## Notes

- **Workshop app images are per-workshop.** The block above is for
  `lab-k8s-fundamentals`. Every workshop you add pulls whatever its content
  deploys — inspect each workshop's `templates/` / manifests and add those refs.
  For workshops using `source.type: git`, also mirror the git repo (or switch to
  `source.type: image` and mirror the `*-files` image).
- **Version drift:** tags above match Educates 3.7.2, the pinned oauth-proxy /
  kube-state-metrics / kapp-controller versions, and the workshop content at the
  time of writing. Re-run `helm template` + check the installer bundle after any
  version bump.
- **kapp-controller** can also be pulled by tag `ghcr.io/carvel-dev/kapp-controller:v0.60.3`;
  the chart pins the digest (see dcs-academy-kapp-controller/values.yaml `image.digest`).
- After mirroring, per-cluster overrides: `global.registry.host` (+ `pullSecret`)
  on the platform and workshops charts; workshop content images rewrite
  automatically, git/http sources do not.

## Harbour Config


### 0. GHCR — (educates images)

```text
educates/{educates-installer,educates-session-manager,educates-training-portal,educates-docker-registry,educates-pause-container,educates-base-environment,educates-jdk8-environment,educates-jdk11-environment,educates-jdk17-environment,educates-jdk21-environment,educates-conda-environment,educates-secrets-manager,educates-tunnel-manager,educates-image-cache,educates-assets-server,educates-lookup-service,educates-node-ca-injector,lab-k8s-fundamentals-files,lab-k8s-fundamentals-frontend}

```

#### 2. Tag Filter

Since this explicit list now includes your workshop content images (`8.1` and `3.0`), update your **Tag** filter field to look for all three target tags, separated by a comma:

```text
3.7.2, 8.1, 3.0

```

### 1. GHCR — Loft-sh (vcluster images)

* **Source Registry:** `ghcr-endpoint`
* **Name (Repository):**
```text
loft-sh/{kubernetes,vcluster-oss}

```


* **Tag:**
```text
v1.31.1, v1.32.1, v1.33.4, v1.34.0, 0.30.2

```



### 2. GHCR — Carvel Dev (kapp-controller Prerequisite)

* **Source Registry:** `ghcr-endpoint`
* **Name (Repository):**
```text
carvel-dev/kapp-controller

```


* **Tag:** *(Harbor accepts full SHA-256 digests in the Tag filter field)*
```text
sha256:610a14076cfe8864cd0bd961277b8c239298ab418234a1a8c324f2f5792c9b1d

```



### 3. Docker Hub (External Deps & App Images)

> ⚠️ **Important:** Official Docker Hub images do not have an organization prefix in their standard pull strings (e.g., `postgres:17.7`), but their true underlying path in the registry is under the `library/` namespace. You must explicitly include `library/` here.

* **Source Registry:** `dockerhub-endpoint`
* **Name (Repository):**
```text
library/{debian,docker,postgres,redis}

```


* **Tag:**
```text
sid-20230502-slim, 27.5.1-dind, 17.7, 8.6.2

```



### 4. Red Hat Registry (Auth Proxy)

* **Source Registry:** `redhat-endpoint`
* **Name (Repository):**
```text
openshift4/ose-oauth-proxy

```


* **Tag:**
```text
v4.14

```



### 5. Kubernetes Registry (Monitoring)

* **Source Registry:** `k8s-endpoint`
* **Name (Repository):**
```text
kube-state-metrics/kube-state-metrics

```


* **Tag:**
```text
v2.14.0

```



---

### 💡 Pro-Tip for Harbor Replication Logs

When you execute these rules, Harbor will cross-reference every listed tag against every repository in that specific rule.

For example, it will look for the tag `17.7` inside the `library/debian` repository. This will output a harmless `v2/images/tags/list: 404 Not Found` or `Tag not found` warning in your Harbor replication logs for those mismatched combinations. **You can safely ignore these.** The job will still finish with a `Success` status once it successfully matches and pulls the correct tags.
