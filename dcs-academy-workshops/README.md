# dcs-academy-workshops

Workshop catalog + portal + OpenShift-OAuth gate, **separate from the platform
install** ([dcs-academy-platform](../dcs-academy-platform)). Renders one `Workshop`
CR per entry, a `TrainingPortal` that hosts them, and the `oauth-proxy` that fronts
it. Ships [lab-k8s-fundamentals](https://github.com/educates/lab-k8s-fundamentals)
from its GitHub repo. Add more by appending to the list.

Portal name `dcst-dcs` → dynamic session namespaces are `dcst-*`; the public UI is
served at `academy.<ingressDomain>` (set by `portal.ingress.hostname`).

---

## Prerequisites

- Platform installed ([dcs-academy-platform](../dcs-academy-platform)) — Educates
  CRDs + control plane running.
- oauth cookie secret in the release namespace (see argocd/README) — or leave
  `auth.existingSecret` empty for plain helm (auto-generated via lookup).

## Install

```sh
helm install dcs-academy-workshops ./dcs-academy-workshops \
  --create-namespace -n dcs-educates-workshops
```

Verify:

```sh
oc get workshops
oc get trainingportal dcst-dcs
echo "https://academy.apps.test.ocp.globomantics.com"   # -> OpenShift OAuth, then portal
```

The portal lists every workshop; sessions run per each workshop's budget/policy
(and per-session vcluster unless opted out).

---

## Content sources — "loading" a workshop

Each workshop's `source.type` selects where Educates fetches content
(via Carvel vendir):

| type | use | air-gap |
|------|-----|---------|
| `git` | **default** — pull the workshop repo live at session build | mirror the git repo |
| `image` | published `*-files` OCI image | mirror the image; rewrites via `global.registry.host` |
| `githubRelease` | a GitHub release asset | mirror the asset |
| `http` | a tarball URL | mirror the URL |

lab-k8s-fundamentals ships with `git` (loads
`github.com/educates/lab-k8s-fundamentals` at `origin/main`). For a locked or
air-gapped deploy, switch it to `image`:

```yaml
workshops:
  - name: lab-k8s-fundamentals
    source:
      type: image
      image:
        repository: ghcr.io/educates/lab-k8s-fundamentals-files
        tag: "8.1"
```

With `global.registry.host=YOUR_REGISTRY` set, image refs rewrite to
`YOUR_REGISTRY/educates/lab-k8s-fundamentals-files:8.1`. `git`/`http` URLs are
**not** rewritten — mirror those repos/URLs yourself for offline use.

---

## Adding workshops

Append to `workshops:` in [values.yaml](values.yaml) (a commented
`lab-container-basics` example is included). Each entry:

```yaml
- name: <workshop-name>          # must match the Workshop metadata.name
  title: "..."
  description: "..."
  source: { type: git, git: { url: ..., ref: origin/main } }
  includePaths: [/workshop/**, /README.md]
  session:
    budget: medium               # small|medium|large|x-large|custom
    policy: restricted           # restricted|baseline|privileged
    applications: { terminal: true, console: true, editor: true, slides: true }
    # vcluster: true             # per-workshop override of global vcluster.enabled
  portal: { expires: 60m, orphaned: 5m }
```

The portal hosts all listed workshops automatically.

---

## OpenShift OAuth gate + the auth bypass

With `auth.enabled` (default), an `oauth-proxy` (ServiceAccount-as-OAuthClient)
fronts the portal at `academy.<domain>` and **auto-redirects unauthenticated
users to OpenShift OAuth** (`--skip-provider-button`, like ArgoCD). Portal
`registration.type: anonymous` means no self-signup — the OAuth login is the only
gate. Verified: `GET https://academy.<domain>/` → `302` to
`oauth-openshift.<domain>/oauth/authorize`.

**Bypass — read this.** Educates always publishes its *own* portal route at
`<portal.name>-ui.<domain>` (e.g. `dcst-dcs-ui.<domain>`), which reaches the
portal directly, around the proxy. On this platform it can NOT be closed from the
chart:

- **NetworkPolicy** — ineffective when the OpenShift ingress router runs on
  `HostNetwork` (default on some clusters): router traffic comes from the node, so
  podSelector rules don't match it.
- **Route-hostname conflict** (proxy + Educates claim the same host) — races on
  route admission and can fail *open*. Not used.

Close the bypass at the **infra layer** (deployment choice):

1. **Switch the router off HostNetwork** — set the IngressController
   `endpointPublishingStrategy` to `LoadBalancer`/`NodePortService`. Then a
   NetworkPolicy restricting the portal pod to the oauth-proxy works; re-add one
   if desired.
2. **External gateway** — put a reverse proxy / API gateway doing OpenShift OAuth
   in front of the apps domain, or restrict `*-ui.<domain>` at the edge.

The chart intentionally does not ship a NetworkPolicy, since it silently fails on
HostNetwork routers and blocks `helm install` (the portal namespace doesn't exist
yet). Enforcement is an infra decision.

## vcluster per session (phase 3)

`--set vcluster.enabled=true` turns on `session.applications.vcluster` for every
workshop and raises the budget to `large`. Override per workshop with
`session.vcluster: true|false`. vcluster images ship in the platform bundle and
are registry-overridable there.

**OpenShift SCC grant (required).** vcluster syncs a coredns pod (uid + is
`NET_BIND_SERVICE`) into the host `<session>-vc` namespace, which Educates
hardcodes to the **baseline** SCC — baseline rejects `NET_BIND_SERVICE`, so
coredns never starts and the vcluster hangs "not ready". When vcluster is on,
this chart adds a `session.objects` RoleBinding granting the **educates-privileged**
SCC to the service accounts in that namespace (`$(vcluster_namespace)`). Without
it, vcluster does not come up on OpenShift.

---

## ArgoCD

Workshop/TrainingPortal carry `sync-wave: "5"` + `SkipDryRunOnMissingResource=true`,
so ArgoCD converges once the platform CRDs exist. The oauth-proxy runs at an
earlier wave, so it owns `academy.<domain>` before the portal reconciles (Educates'
own route for that host is rejected). Deploy as app `dcs-academy-workshops` after
the platform. Set `auth.existingSecret` (or the SealedSecret) under ArgoCD — no
`lookup` at template time.

## Uninstall

```sh
helm uninstall dcs-academy-workshops -n dcs-educates-workshops
```
