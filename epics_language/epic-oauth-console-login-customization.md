# Epic: OAuth & Console Login Customization for External-LB, Multi-Region Clusters

## Problem

Two related but distinct gaps, both on the OpenShift login/authentication
surface:

1. Clusters sit behind an external LB with a customer-facing FQDN that
   differs from the cluster's actual FQDN. The oauth-server Route
   hostname was already fixed (`ingress.config.openshift.io`
   `spec.componentRoutes`), which corrected the console's "Copy login
   command" link target — but the token-display page it links to still
   renders `oc login --server=<internal API FQDN>`. That value comes from
   a separate oauth-server startup config field, not the Route, and has
   no supported override. The native console menu item also can't be
   hidden — no supported toggle exists in the 4.x console.
2. Users across Dev, QA, QA Managed, PreProd, Hub, and country-specific
   clusters (Germany, Spain, France, Europe) can't tell from the login
   screen which cluster/region/data-classification context they're
   authenticating into.

## Approach summary

- A small standalone service reuses oauth-server's existing token-request
  flow almost verbatim, with the server URL corrected and its own
  `OAuthClient`.
- A console dynamic plugin (`ConsolePlugin` CR) hides the native, broken
  menu item — no console image rebuild.
- The OAuth login page gets cluster-identity branding via OpenShift's
  supported custom-login-template mechanism, packaged as a Helm chart
  with all flag images bundled in, so operators swap a values.yaml
  reference rather than shipping new files per cluster.

## Global risks

- The console-hide mechanism (US-2) relies on an internal test attribute,
  not a published API — can silently break on an OCP upgrade. Add to the
  post-upgrade validation checklist.
- US-3's environment list mixes two axes — environment tier (Dev, QA, QA
  Managed, PreProd) and country/region (Germany, Spain, France, Europe) —
  plus Hub, which is neither. Confirm with the cluster inventory owner
  whether tier-only clusters get a generic flag/banner or a specific
  country assignment before finalizing values files.

## Reference material

Full extracted source files (not just excerpts) are attached separately:
`copy-login-command-reference/` — `oauth-server-reference/tokenrequest.go`,
`console-masthead-reference/masthead-toolbar-excerpt.tsx` +
`useCopyLoginCommands.ts`, each with a README. The facts below are
inlined from that research so this document is self-contained.

---

## US-1 — Custom "Copy login command" link with correct external server URL

**As a** cluster user
**I want** a "Copy login command" option that shows a working `oc login`
command using the external API FQDN
**So that** I can log in via CLI without hitting an unreachable internal
hostname.

### Acceptance criteria
- New `OAuthClient` (`custom-login-command`) created, `grantMethod: auto`,
  scope `user:full`, own redirect URI — does not touch or repoint
  `openshift-browser-client`.
- Standalone service implements `/oauth/token/request` and
  `/oauth/token/display`, reusing the existing CSS/JS/CSRF flow.
- `--server=` value is a configured external API FQDN (env var or
  ConfigMap), not derived from cluster state.
- Deployed behind its own Route with valid TLS.
- `ConsoleLink` CR (`location: UserMenu`) added, labeled distinctly (e.g.
  "Copy login command (external)") until US-2 ships.
- End-to-end test: click link → copy command → `oc login` succeeds
  against the external endpoint.

### Technical reference (verified against source, not docs)

**Repo:** `https://github.com/openshift/oauth-server`
**File:** `pkg/server/tokenrequest/tokenrequest.go` (full file in reference
bundle — reuse almost verbatim)

Endpoints it installs (`Install()` method):
```go
mux.HandleFunc(path.Join(prefix, oauthdiscovery.RequestTokenEndpoint), ...)  // GET /oauth/token/request
mux.HandleFunc(path.Join(prefix, oauthdiscovery.DisplayTokenEndpoint), ...)  // GET+POST /oauth/token/display
mux.HandleFunc(path.Join(prefix, oauthdiscovery.ImplicitTokenEndpoint), ...) // informational only
```

Flow: `requestToken` redirects to `/oauth/authorize` (response_type=code)
→ `displayTokenGet` renders a form with the auth code + CSRF token
(`formTemplate`) → user submits → `displayTokenPost` exchanges the code
for a token server-side (`osinOAuthClient.NewAccessRequest(osincli.AUTHORIZATION_CODE, ...)`)
→ renders `tokenTemplate` (the page with token / `oc login` / `curl`
snippets, plus the `codeSnippet()` JS clipboard-copy helper — reuse this
whole block as-is).

**The bug, exact location:** `tokenTemplate`, in the `oc login` snippet:
```go
codeSnippet(document.getElementById('login'), [
  'oc login',
  '--token={{.AccessTokenJSStr}}',
  '--server={{.PublicMasterURLJSStr}}',
]);
```
`PublicMasterURL` is set in `displayTokenPost` from `t.publicMasterURL`,
which is injected via `NewTokenRequest(loginURL, ...)` in
`pkg/oauthserver/auth.go`:
```go
loginURL := c.ExtraOAuthConfig.Options.LoginURL
if len(loginURL) == 0 {
    loginURL = c.ExtraOAuthConfig.Options.MasterPublicURL
}
```
This is an oauth-server startup config value, not the Route hostname —
confirms there's no supported override independent of a full oauth-server
config change (which would affect the native flow too, hence the
standalone-service approach).

**Why a new OAuthClient, not the existing one:** `auth.go`,
`getOsinOAuthClient()`, fetches the platform-managed OAuthClient object
`openshift-browser-client` and hardcodes its redirect URL:
```go
osOAuthClientConfig.RedirectUrl = oauthdiscovery.OpenShiftOAuthTokenDisplayURL(c.ExtraOAuthConfig.Options.MasterPublicURL)
```
That object is reconciled by the platform. Example manifest for the new,
dedicated client:
```yaml
apiVersion: oauth.openshift.io/v1
kind: OAuthClient
metadata:
  name: custom-login-command
secret: <generate, store in a Secret, don't inline>
redirectURIs:
  - https://custom-login.apps.<external-domain>/oauth/token/display
grantMethod: auto
scopeRestrictions:
  - literals:
      - user:full
```

**Confirms the native link itself is already correct (context, not a
bug to fix):** `openshift/console`,
`frontend/packages/console-shared/src/hooks/useCopyLoginCommands.ts`,
calls `GET /api/copy-login-commands` on the console backend, which
returns `requestTokenURL` reflecting the oauth-server Route hostname —
i.e. your earlier ingress fix is correctly reflected in the link target.
Only the destination page's content is wrong (see above).

---

## US-2 — Hide the native "Copy login command" menu item

**As a** cluster user
**I want** only the working link visible in the User menu
**So that** I'm not misled into using the broken native one.

### Acceptance criteria
- Spike (timebox 1 day) confirms a `ConsolePlugin` bundle can run a
  MutationObserver against console-owned DOM before full build starts.
- `ConsolePlugin` deployed (Deployment + Service + CR), enabled in
  `consoles.operator.openshift.io` `spec.plugins`.
- Native item hidden reliably, verified across page reload and a fresh
  login session.
- `ConsoleLink` label from US-1 simplified back to "Copy login command"
  once confirmed hidden.
- Sequencing: don't ship this before US-1 is live and verified — never a
  window where neither link works.

### Technical reference (verified against source)

**Repo:** `https://github.com/openshift/console`
**File:** `frontend/public/components/masthead/masthead-toolbar.tsx`

Exact menu-item registration (two branches, both carry the same
attribute):
```tsx
if (requestTokenURL) {
  userActions.unshift({
    label: t('Copy login command'),
    href: requestTokenURL,
    externalLink: true,
    dataTest: 'copy-login-command',   // renders as data-test="copy-login-command"
  });
} else if (externalLoginCommand) {
  userActions.unshift({
    callback: launchCopyLoginCommandModal,
    dataTest: 'copy-login-command',   // same attribute, external-OIDC modal path
    label: t('Copy login command'),
  });
}
```
`requestTokenURL` / `externalLoginCommand` come from
`frontend/packages/console-shared/src/hooks/useCopyLoginCommands.ts`
(see US-1 reference) — the `requestTokenURL` branch is the relevant one
for a standard built-in OAuth server setup; `externalLoginCommand` is the
external-OIDC-issuer path and not in use on this cluster, but the
selector below is safe against either branch.

**Selector to target:** `[data-test="copy-login-command"]`. Hide the
containing `<li>` (`el.closest('li')`), not just the link, or a blank row
is left behind. The menu only mounts this node when the User menu is
opened, so a MutationObserver against `document.body` (not a one-time
querySelector on page load) is required.

**Risk, stated plainly:** `data-test` attributes are internal e2e-test
hooks, not a published API contract — can be renamed/removed in any OCP
release without changelog mention.

---

## US-3 — Cluster-identity branding on the OAuth login page, via Helm chart with bundled flag images

**As an** operator responsible for a specific cluster
**I want** the login page to show the cluster's country flag and allowed
data classifications, with all flag images already packaged in the Helm
chart
**So that** users see at a glance where they're logging in and what data
handling rules apply, and I only ever edit `values.yaml` to point at a
different bundled file — never ship new image files myself.

### Acceptance criteria
- Login page template built on the standard `oc adm create-login-template`
  scaffold — IDP list, error rendering, and CSRF field preserved
  unmodified; only branding markup added.
- All flag images for every target cluster are bundled inside the chart
  (e.g. `files/flags/germany.svg`, `files/flags/spain.svg`,
  `files/flags/france.svg`, `files/flags/europe.svg`, plus a generic/
  neutral flag for tier-only clusters). Chart uses Helm's `.Files.Get` +
  `b64enc` to inline the selected file as a `data:image/svg+xml;base64,...`
  URI directly in the rendered `login.html` — the rendered page is a
  single self-contained HTML blob (see delivery mechanism below, no
  separate static-file serving is available for a custom login page).
- `values.yaml` exposes at minimum:
  ```yaml
  clusterName: "Germany"
  countryFlagFile: "flags/germany.svg"     # relative path inside chart's files/
  dataClassifications:
    - Public
    - Internal
    - Confidential
  ```
- Chart renders the final `login.html`, packages it as a Secret in the
  `openshift-config` namespace, and (via Helm hook or a documented manual
  step) patches `oauth.config.openshift.io/cluster`
  `spec.templates.login.name` to reference that Secret.
- Values files provided for at least: Dev, QA, QA Managed, PreProd, Hub
  cluster, Germany, Spain, France, Europe — with the tier-vs-country axis
  question (see Global risks) resolved before these are finalized.
- Rendering verified on at least two target environments (recommend one
  country-specific and one tier-only, e.g. Germany + Dev) before wider
  rollout.
- Regression check: standard login error states (bad credentials, IDP
  unavailable) still render correctly after branding changes.

### Technical reference

**Supported mechanism (no fork, no plugin, unlike US-1/US-2):**
`oauth.config.openshift.io/v1`, resource name `cluster`,
`spec.templates.login.name` → references a `Secret` in the
`openshift-config` namespace containing the custom HTML.
Scaffold command: `oc adm create-login-template > login.html` — this
produces the baseline HTML/Go-template (IDP list, error block, CSRF
field) that the chart's template should extend, not replace.

There is no companion static-asset serving for a custom login page — the
Secret is HTML content only. This is why flags must be inlined
(base64 data URI or raw inline `<svg>`) rather than referenced by URL,
and why bundling the source images inside the chart (rather than an
external image host) is the right call for "operator only edits
values.yaml."

Related, same mechanism family, not in scope but worth knowing if this
epic grows: `spec.templates.providerSelection` (`oc adm
create-provider-selection-template`) governs the identity-provider
selection buttons shown when a cluster has multiple IDPs configured, and
`spec.templates.error` (`oc adm create-error-template`) governs the
auth-error page. Same Secret-reference pattern applies to both.
