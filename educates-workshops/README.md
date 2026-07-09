# educates-workshops

Workshop catalog for Educates, **separate from the platform install**
([educates-openshift](../educates-openshift)). Renders one `Workshop` CR per
entry plus a `TrainingPortal` that hosts them all. Ships
[lab-k8s-fundamentals](https://github.com/educates/lab-k8s-fundamentals) sourced
straight from its GitHub repo. Add more workshops by appending to the list.

Splitting content from the platform lets workshops be versioned, added, and
re-released on their own cadence without touching the platform install.

---

## Prerequisites

The Educates platform must already be installed (CRDs + running control plane):

```sh
# Platform, WITHOUT its built-in smoke-test portal (this chart owns the portal):
helm template educates ../educates-openshift --set portal.enabled=false | oc apply -f -
```

---

## Install

```sh
helm template workshops ./educates-workshops | oc apply -f -
```

Verify:

```sh
oc get workshops
oc get trainingportal container-paas
echo "https://container-paas-ui.apps-crc.testing"   # open it
```

The portal lists every workshop and starts sessions (budget medium, policy
restricted for lab-k8s-fundamentals).

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

Same design as the platform chart: Workshop/TrainingPortal carry
`sync-wave: "5"` and `SkipDryRunOnMissingResource=true`, so ArgoCD converges once
the platform CRDs exist — deploy this as a second `Application` that syncs after
the platform one. Nothing here needs cluster access at template time (no
`lookup`), so it is fully GitOps-safe with no extra values.

## Uninstall

```sh
helm template workshops ./educates-workshops | oc delete -f - --ignore-not-found
```
