# Handover — OpenShift OAuth gating for the Educates portal

## Goal
Only OpenShift-authenticated (company SSO) users may reach the training portal /
start a workshop. No self-signup. Portal UI at `academy.<domain>`.

## TL;DR status
**Working on the x86 test cluster** (`api.test.ocp.globomantics.com`), deployed via
ArgoCD. `academy.apps.test.ocp.globomantics.com` → 302 to OpenShift OAuth →
(after login) portal. The earlier "content blocked" and 504 are addressed
(details below).

**2026-07-10 verification session — open questions resolved:**
- **Q2 session-host gating: CONFIRMED airtight.** Unauthenticated curl to a
  session host (and its console/editor subdomains) → 302 `oauth_handshake` →
  portal `/oauth2/authorize` (behind proxy) → 302 to OpenShift OAuth. 3-hop
  chain verified live; no unauthenticated path in.
- **Q3 route precedence: CLOSED with a ValidatingAdmissionPolicy** (cluster is
  4.20, VAP is GA). `reserve-academy-host` denies any Route CREATE/UPDATE with
  `spec.host == academy.<domain>` outside `dcs-educates-workshops`. Applied
  live AND added to the chart as `templates/42-auth-route-vap.yaml` (push to
  deploy; ArgoCD adopts the live one, same name). Educates' rejected bypass
  route in `dcst-dcs-ui` was deleted; the ingress-to-route controller's
  recreation attempts are denied (warning events only, portal unaffected,
  TrainingPortal stays Running). Flap test passed: deleted the proxy route →
  academy served **503 (fail closed)** for ~70s until ArgoCD selfHeal
  recreated it → gate restored. No fail-open scenario remains.
- **Q1 authed e2e:** first real run TIMED OUT on
  `/workshops/session/<name>/` — root cause found and fixed: the shipped
  NetworkPolicy (portal ingress = oauth-proxy only) also blocked the session
  gateway's server-to-server OAuth code exchange at
  `PORTAL_API_URL=http://training-portal.<portal>-ui` → `/oauth_callback` on
  the session host hung forever (visible in gateway logs as
  `GET /oauth_callback ... - - ms - -`). Fix: netpol now also allows ingress
  from namespaces labeled `training.educates.dev/portal.name=<portal>`
  (both env `-w##` and session namespaces carry it). Patched live + in chart.
  Verified from inside a session pod: token endpoint 400/13ms (reachable).
  NOTE: pod-to-pod IS enforced even on HostNetwork routers — only router
  traffic bypasses the netpol. Re-run the browser login → workshop check.
- **Q4 reserved sessions:** unchanged (`reserved: 1`); raise if 504/waiting UX
  bites.

## Why this shape (constraints)
- **Educates portal can't do native OIDC.** It's an OAuth *provider* (issues
  tokens to sessions); `TrainingPortal.registration.type` only accepts
  `anonymous|one-step`. No field to point it at an external IdP. So an
  **oauth-proxy** in front is the only way to use OpenShift OAuth.
- Auth model: **oauth-proxy + ServiceAccount-as-OAuthClient** (SA redirect
  annotation registers it; proxy uses the SA token — no client secret in git).
  `--skip-provider-button=true` → auto-redirect to OpenShift (ArgoCD-style).
- Portal `registration.type: anonymous` → no signup form; SSO is the only gate.

## The hard part — the bypass, and how it's closed
Educates ALWAYS publishes its own portal route (no disable flag). Two closure
attempts FAILED:
- **NetworkPolicy** → ineffective: this cluster's ingress router is
  `HostNetwork` (endpointPublishingStrategy=HostNetwork), so router traffic comes
  from the node and podSelector rules don't match. (NetworkPolicy is still shipped,
  gated `auth.networkPolicy`, for clusters where the router is NOT HostNetwork.)
- **Route-hostname conflict under plain helm** → races on route admission, and
  once FAILED OPEN (Educates route won `academy`, proxy rejected → portal served
  unauthenticated).

**What works (current design):** set the Educates portal hostname = the proxy host
(`portal.ingress.hostname: academy`) so `PORTAL_HOSTNAME=academy`. The oauth-proxy
runs at an earlier sync-wave, so under **ArgoCD** its Route is admitted on
`academy` first; Educates' own portal Route is then rejected
(`admitted=False, reason=HostAlreadyClaimed`). Deterministic under ArgoCD (wave
ordering); it does NOT hold under plain helm (no waves) — helm is dev-only.

Verified live:
```
PORTAL_HOSTNAME=academy.apps.test.ocp.globomantics.com     # portal
route educates-portal-oauth  host=academy  admitted=True    # proxy (dcs-educates-workshops)
route (dcst-dcs-ui)          host=academy  admitted=False reason=HostAlreadyClaimed  # educates, rejected
curl https://academy…/  ->  302 -> oauth-openshift…/oauth/authorize
```

## Why PORTAL_HOSTNAME=academy matters (the "content blocked" fix)
With `PORTAL_HOSTNAME=dcst-dcs-ui…` (≠ the host users hit), the portal generated
session URLs, cookies, and CSP `frame-ancestors` for the wrong host → the workshop
dashboard's cross-origin iframe was browser-blocked ("This content is blocked").
Setting `PORTAL_HOSTNAME=academy` fixes it. This is REQUIRED for the proxy to work
functionally, and it's what forces the route conflict above.

## The 504 on opening a workshop
Transient. Opening a session while it's still provisioning (vcluster spin-up takes
minutes) makes a synchronous request exceed the router's 30s default → 504. After
provisioning, `academy/workshops/session/<name>/` and the session host both return
302 (Educates `oauth_handshake`) in ~40ms. Mitigation shipped:
`haproxy.router.openshift.io/timeout: 120s` (value `auth.routeTimeout`) on the
`academy` route. Consider raising `TrainingPortal` reserved sessions so users get a
pre-provisioned one (currently `reserved: 1`).

## Session-host flow (verify this)
Workshop sessions run at their OWN hosts `dcst-dcs-w01-<id>.<domain>` (+ console/
editor subdomains), NOT behind the oauth-proxy. They do an Educates
`oauth_handshake` back to the portal at `academy` (behind the proxy). The user's
browser carries the oauth-proxy cookie, so the handshake passes through. **To
confirm gating is airtight, a new session should check:** can an *unauthenticated*
browser reach a session host directly and get in, or is it always bounced through
the portal → OpenShift OAuth? (Educates gates sessions with portal-issued tokens,
so it should bounce — but verify.)

## Key files
- `dcs-academy-workshops/templates/40-auth.yaml` — oauth-proxy (SA, Route,
  Deployment, cookie secret), `--skip-provider-button`, route timeout.
- `dcs-academy-workshops/templates/41-auth-sealed-secret.yaml` — SealedSecret option.
- `dcs-academy-workshops/templates/42-auth-route-vap.yaml` — VAP reserving the
  academy host for the proxy route (fail-closed backstop, gated `auth.enabled`).
- `dcs-academy-workshops/templates/50-portal-netpol.yaml` — netpol (gated).
- `dcs-academy-workshops/templates/20-trainingportal.yaml` — sets portal
  `ingress.hostname` (= PORTAL_HOSTNAME) when auth on.
- `dcs-academy-workshops/values.yaml` — `auth.*` (enabled, existingSecret,
  sealedSecret, tlsCertificateRef, routeTimeout, networkPolicy), `portal.ingress.hostname: academy`.
- `dcs-academy-workshops/README.md` — "OpenShift OAuth gate + the auth bypass".
- `argocd/apps/03-educates-workshops.yaml` — app; ignoreDifferences.

## Cluster facts (x86 test)
- Domain `apps.test.ocp.globomantics.com`; router cert `globomantics-ingress-cert`
  (ns `openshift-ingress`); **router is HostNetwork**.
- Namespaces: static `dcs-*` (`dcs-educates-installer`, `dcs-educates`,
  `dcs-educates-workshops`), dynamic sessions `dcst-*`, Educates operator `educates`.
- Cookie secret: for ArgoCD set `auth.existingSecret` or `auth.sealedSecret`
  (helm template has no cluster access → generated cookie churns each sync).
  Cookie must be 16/24/32 bytes (`openssl rand -hex 16`).

## Diagnose commands
```sh
# proxy + portal + routes
oc get pod -n dcs-educates-workshops -l app.kubernetes.io/component=oauth-proxy
oc set env deploy/training-portal -n dcst-dcs-ui --list | grep PORTAL_HOSTNAME
oc get route -A | grep academy
oc get route -n dcst-dcs-ui -o jsonpath='{range .items[*]}{.spec.host} {.status.ingress[0].conditions[0].status}/{.status.ingress[0].conditions[0].reason}{"\n"}{end}'
curl -sk -m10 -o /dev/null -w '%{http_code} -> %{redirect_url}\n' https://academy.apps.test.ocp.globomantics.com/
oc logs -n dcs-educates-workshops -l app.kubernetes.io/component=oauth-proxy --tail=50
```

## Open questions for the new session
1. End-to-end authed run: login → start workshop → dashboard + terminal + editor
   all load (no content-block, no 504)?
2. Is direct access to a session host by an unauthenticated user truly bounced to
   OpenShift OAuth? (session-token gating.)
3. Route-precedence robustness: if the proxy Route is ever recreated after
   Educates' route exists (e.g. selfHeal), does Educates win `academy` and fail
   open? Consider a ValidatingAdmissionPolicy denying Educates' portal route for
   the `academy` host as a fail-closed backstop.
4. Reserved-session count vs vcluster provisioning time (avoid 504 UX).

See also the memory note `educates-oauth-gating-openshift`.
