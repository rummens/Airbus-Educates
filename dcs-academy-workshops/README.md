# dcs-academy-workshops

Workshop catalog + Educates backend portal, **separate from the platform install**
([dcs-academy-platform](../dcs-academy-platform)). Renders one `Workshop` CR per
entry and a `TrainingPortal` that hosts them. Ships
[lab-k8s-fundamentals](https://github.com/educates/lab-k8s-fundamentals) from its
GitHub repo. Add more by appending to the list.

The OpenShift-OAuth gate (oauth-proxy + host-reservation VAP) lives in the
[dcs-academy-portal](../dcs-academy-portal) chart now — it fronts the custom portal
at `academy.<ingressDomain>` and keeps this Educates backend in-cluster only.

Portal name `dcst-dcs-backend` → dynamic session namespaces are `dcst-*`; the
Educates backend runs in `dcst-dcs-backend-ui`. `portal.ingress.hostname` (academy)
must match the portal chart's `auth.hostname`.

---

## Prerequisites

- Platform installed ([dcs-academy-platform](../dcs-academy-platform)) — Educates
  CRDs + control plane running.

## Install

```sh
helm install dcs-academy-workshops ./dcs-academy-workshops \
  --create-namespace -n dcs-educates-workshops
```

Verify:

```sh
oc get workshops
oc get trainingportal dcst-dcs-backend
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

**Bypass — read this.** Educates always publishes its *own* portal route
(no disable flag), which would reach the portal directly, around the proxy.
How the chart closes it:

1. **Host claim.** The portal's `ingress.hostname` is set to the proxy host
   (`academy`), so `PORTAL_HOSTNAME` matches the public host (required anyway —
   otherwise session cookies/CSP are generated for the wrong host and the
   workshop iframe is browser-blocked). The oauth-proxy Route runs at an earlier
   ArgoCD sync-wave, wins the `academy` host, and Educates' route is rejected
   (`HostAlreadyClaimed`). Deterministic under ArgoCD only — plain helm has no
   wave ordering (dev-only).
2. **VAP backstop (fail-closed).** `templates/42-auth-route-vap.yaml` ships a
   `ValidatingAdmissionPolicy` (`reserve-academy-host`, OCP 4.16+/K8s 1.30+)
   denying any Route CREATE/UPDATE with `spec.host = academy.<domain>` outside
   the release namespace. This kills the residual fail-open: without it, if the
   proxy Route is ever recreated *after* Educates' route exists, Educates wins
   the host (router admission is oldest-claim-wins) and the portal serves
   unauthenticated. With it, Educates' route can never exist on that host — the
   ingress-to-route controller's creation attempts are denied (warning events in
   `<portal>-ui`, harmless; portal unaffected). Verified: deleting the proxy
   Route → `academy` serves **503** until ArgoCD selfHeal recreates it.
3. **NetworkPolicy** (`auth.networkPolicy`, default on) — defense in depth for
   clusters whose router is NOT HostNetwork. On HostNetwork routers (this test
   cluster) router traffic comes from the node and podSelector rules don't match,
   so the netpol is ineffective there — the VAP is the enforcement that holds.

Session hosts (`<portal>-w##-<id>.<domain>` + console/editor subdomains) are not
behind the proxy but are gated by Educates' own portal-issued session tokens:
an unauthenticated browser is bounced `oauth_handshake` → portal (behind the
proxy) → OpenShift OAuth. Verified end-to-end with curl.

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
