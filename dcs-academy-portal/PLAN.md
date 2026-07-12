# DCS Academy — Custom Training Portal (`dcs-academy-portal`)

Design + build plan for a **custom landing/catalog portal** that replaces the
built-in Educates training portal UI, while keeping the Educates session runtime
(workshop dashboard: instructions + terminal + editor) untouched.

Research that produced this plan: see the proposal in the session that created
this folder. Educates exposes a REST API + Kubernetes CRs that a custom
front-end is explicitly meant to consume (docs.educates.dev "portal REST API").
We build on that seam — we do **not** fork Educates.

---

## 1. Goal

Replace only the **main page users use to find their lab**. Users get a richer
landing page (modules/tracks → courses, pre-launch detail, live provisioning
screen, custom look). Everything after "Start session" stays native Educates.

## 2. Locked decisions (from the requirements interview)

| Topic | Decision |
|---|---|
| Architecture | Custom Flask app = server-rendered UI **+** backend-for-frontend (BFF) **+** reverse-proxy for the Educates paths the session runtime needs. One image. |
| Frontend | **Jinja templates + htmx/vanilla JS**. No Node build, no SPA framework. All assets vendored in the image. |
| Language/base | **Python (Flask)** on the **Red Hat hardened UBI Python** image. Self-contained; only the logo may load from outside. |
| Session forwarding | On ready, **302 redirect** the browser to the session host. Session host has its own Educates token auth (prevents takeover). |
| Admin gating | **Option 1 — SelfSubjectAccessReview (SSAR)** with the user's OpenShift token. Admin button shown only if SSAR allows; admin routes enforce SSAR server-side. |
| Module/track model | **New `Track` CRD**, rendered by the Helm chart from values. Portal reads Track + Workshop CRs via the k8s API to build the catalog. |
| Portal host | **Replaces Educates at the `academy.<domain>` host**, behind the existing oauth-proxy. Educates portal stays in-cluster only (never externally routed). |
| Session ↔ user | **Bind to SSO user**: portal passes the authenticated username (from `X-Forwarded-Access-Token`) as the Educates session-request `user` param → returning user resumes their own session. |
| Feedback | **Absorb** the existing `feedback-collector` into this portal, **switch storage to CloudNativePG (CNPG)**. Ratings (not comments) shown in the course view when review count ≥ threshold. Full feedback analysis (ratings + comments) in the admin view. |
| CNPG operator | Chart **depends on** CNPG (ships the `Cluster` CR); operator installed **separately** (ArgoCD/OLM). |
| Track authoring | **Helm values → Track CRs** (GitOps-managed). |
| Deploy | **Helm chart** (fits the existing ArgoCD app-of-apps). |

## 3. The architecture crux — reverse-proxy the Educates session paths

`PORTAL_HOSTNAME=academy` is mandatory (see `HANDOVER-oauth-gating.md`): the
Educates **session gateway does a browser-side `oauth_handshake` back to the
portal host** for every session, and issues session URLs/cookies/CSP
`frame-ancestors` for that host. If `academy` stops serving those Educates
endpoints, **every session breaks** (the old "content blocked" / handshake
failures).

Therefore the new portal must serve its **own UI on its own paths** and
**transparently reverse-proxy an allowlist of Educates portal paths** to the
in-cluster Educates `training-portal` Service:

```
browser ──▶ oauth-proxy (academy, existing)
              └─▶ dcs-academy-portal  (Flask, this project)
                    ├─ GET /                     → custom catalog UI (Jinja)
                    ├─ GET /course/<name>        → custom course detail
                    ├─ GET /launch/<name>        → provisioning screen (SSE)
                    ├─ GET /admin                → admin (SSAR-gated)
                    ├─ GET /metrics              → Prometheus
                    └─ PROXY allowlist ─────────▶ Educates training-portal Service (in-cluster)
                         /oauth2/…  /oauth_callback  /workshops/session/…
                         /session/…  /workshops/environment/…  /workshops/catalog/…
                    └─ k8s API (SA token): Workshop, Track, WorkshopSession, Pods
                    └─ k8s API (USER token): SelfSubjectAccessReview (admin check)
```

- oauth-proxy `--upstream` changes from the Educates Service **to this app's
  Service** (`40-auth.yaml`).
- The proxy allowlist keeps the Educates auth/session runtime working under
  `academy` while we own the landing experience. Anything not in the allowlist
  and not a custom UI route → 404 (do not blindly proxy everything).
- Educates `training-portal` Service stays **in-cluster only** (no Route). The
  VAP (`42-auth-route-vap.yaml`) already reserves the `academy` host; keep the
  NetworkPolicy so only this app + session namespaces reach the Educates Service
  → satisfies "Educates API must not be exposed."

> Builder: verify the exact minimal path allowlist against a live session
> (start one, watch which `academy/...` paths the session gateway hits). Under-
> proxying breaks sessions; over-proxying re-exposes the Educates UI.

## 4. Catalog data model

**`Track` CRD** (new, cluster- or namespace-scoped; operator-free — it is pure
data the portal reads). Rendered by the chart from `values.tracks`:

```yaml
apiVersion: academy.dcs/v1alpha1
kind: Track
metadata: { name: developer-basics }
spec:
  title: "Developer — Basics"
  description: "Get productive on DCS: namespaces, workloads, registry."
  order: 10
  icon: "code"        # maps to a vendored inline SVG
```

**Course = Educates `Workshop` CR.** The portal reads native Educates fields
where present (`title`, `description`, `difficulty`, `duration`) and
`academy.dcs/*` labels/annotations for the rest:

| Datum | Source |
|---|---|
| Display title (tile/detail) | annotation `academy.dcs/display-name` → `spec.title` (if human) → prettified CR name (`lab-a02-kubernetes-essentials` → "Kubernetes Essentials") |
| Title (raw) | Workshop `spec.title` |
| One-sentence summary (tile) | annotation `academy.dcs/summary` (fallback: first sentence of `spec.description`) |
| Complexity (icon) | Workshop `spec.difficulty` (`beginner|intermediate|advanced|extreme`) |
| Duration (icon) | Workshop `spec.duration` |
| Tile icon | annotation `academy.dcs/icon` (FA-style name → vendored inline SVG; falls back to the track's section icon) |
| Track membership | label `academy.dcs/track: developer-basics` |
| Order within track | label `academy.dcs/order: "10"` (also drives the "Lab N of M" sequence) |
| Long detail (detail page) | `spec.description` + optional annotation `academy.dcs/details` (markdown) |

> Builder: confirm exact Educates Workshop field paths on the live CRD
> (`oc explain workshop.spec` / `oc get crd workshops.training.educates.dev -o yaml`).
> Read Workshop CRs directly via the k8s API for the catalog (richer + reliable);
> use the Educates **REST API** only for the session lifecycle (request/status/
> terminate) — don't reimplement session allocation.

## 5. Pages / UX

- **Main page** — one **collapsible section per Track** (ordered by `spec.order`).
  Under each: course tiles for Workshops whose `academy.dcs/track` matches,
  ordered by `academy.dcs/order`. Tile shows **title, one-sentence summary,
  complexity icon, duration icon**, and (if review count ≥ threshold) a compact
  star rating. Collapsible via htmx/vanilla, no framework.
- **Course detail** (`/course/<name>`) — full description/details, complexity,
  duration, author, aggregate **rating (stars + count, no comments)** if ≥
  threshold, and **Start session** → `/launch/<name>`.
- **Launch / provisioning screen** (`/launch/<name>`) — custom animated screen
  driven by a live status feed (§6). On `Running` + reachable → **302 redirect**
  to the session URL.
- **Admin** (`/admin`) — visible only if SSAR passes; contains the **feedback
  analysis view** (ported from `feedback-collector` `/admin`: per-course +
  aggregate ratings **and** comments) plus session/usage overview.

## 6. Live provisioning status feed

Endpoint `/api/session/<name>/status` (SSE or htmx poll) merges, via the app SA:

1. `WorkshopSession.status.educates.phase` + `.status.educates.message`
   (confirmed live: printer columns "Status"/"Message" on
   `workshopsessions.training.educates.dev`).
2. Pods in the **session/workshop namespace** — workshop pod init/container
   states.
3. Pods in the **vcluster namespace** — vcluster statefulset readiness (when the
   workshop uses a virtual cluster).

Map to human steps, e.g.:
`Reserving session → Starting virtual cluster → Starting workshop pod →
Loading content → Ready`. Redirect when phase `Running` and the session URL is
reachable.

`PORTAL_SESSION_TLS_VERIFY=false` (env) disables cert verification on the app's
**server-side** HTTP calls (Educates REST + any session-host reachability probe)
for the dev cluster with self-signed certs. Default `true`. The browser redirect
itself is unaffected (that's the user's browser trusting the cert).

## 7. Feedback absorption → CNPG

Fold `images/feedback-collector/app.py` into the portal:

- Keep endpoints: `POST /analytics` (Educates analytics webhook sink — keep the
  TrainingPortal `analytics.webhook.url` pointing at the portal Service),
  `POST /feedback`, `GET /form` (or reuse), admin report, `/metrics`.
- **Storage → CNPG.** The existing app already has the seam
  (`DATABASE_URL=postgres://…`, stubbed `_pg`). Implement the psycopg backend,
  bundle `psycopg` in the image, point `DATABASE_URL` at the CNPG Cluster.
- **Schema** stays (`feedback(id, ts, workshop, session, source, rating,
  clarity, comment)`). Same aggregates.
- **Course view** shows only `AVG(rating)` + count when `count >=
  FEEDBACK_MIN_REVIEWS` (default 5, env-configurable). **Never** comments outside
  admin.
- **Per-user progress** (same CNPG DB, table `progress(username, workshop, status,
  ts)` UNIQUE(username,workshop)): `/launch` marks `started`, end-of-lab feedback
  marks `completed` (sticky — never downgrades). Drives tile badges
  (Completed / In progress), the "Continue where you left off" banner, and is keyed
  on the SSO username from the oauth-proxy header.
- **Data migration:** default **fresh start** (early-stage data). Optionally ship
  a one-shot `Job` that imports the old SQLite rows if the PV still holds them.
  *(Assumption — flag if you want the old rows migrated.)*
- Retire the standalone `feedback-collector` Deployment/PVC/Service
  (`60-feedback-collector.yaml`) once absorbed; keep the Grafana dashboard
  (`dashboards/feedback.json`) pointed at the new metrics.

## 8. Theme (env-configurable)

Server-side inject CSS variables into a `<style>` block from env. Required:

- `THEME_PRIMARY_COLOR`
- `THEME_SECONDARY_COLOR`
- `THEME_LOGO_URL` (the **only** sanctioned external fetch; also allow a mounted
  file / data-URI for fully air-gapped)

Add (sufficient set): `THEME_ACCENT_COLOR`, `THEME_PRODUCT_NAME` (title/brand),
`THEME_FAVICON` (emoji or vendored asset), `THEME_BACKGROUND`,
`THEME_FONT_FAMILY` (from a vendored font), `THEME_FOOTER_HTML`. All optional
with sane defaults. Everything else (fonts, icons, htmx, CSS) vendored in the
image — **no CDN, no external calls** except the logo.

**Defaults = the DCS docs look (§8a).** Ship the design below as the built-in
default so an unconfigured deploy already looks on-brand.

## 8a. Design reference (match the DCS docs start page)

Source: `dcs-academy-portal/Digital Container Services _ DCS.pdf` (print dump of
the live DCS docs landing page). Match its design language:

- **Palette:** deep **navy** for headings/text (~`#16264a`) + **teal/cyan** accent
  (~`#12b5b0`) on highlighted words, icons, links, pill borders. Near-white page
  background (`#ffffff`/`#f7fafb`). → `THEME_PRIMARY_COLOR`=navy,
  `THEME_SECONDARY_COLOR`/`THEME_ACCENT_COLOR`=teal by default.
- **Logo:** hex/atom mark + "DCS" wordmark (D navy, C teal, S navy), top-left in a
  minimal white sticky header.
- **Typography:** bold geometric/rounded sans (Poppins/Nunito-like — vendor one
  offline). Large bold navy headlines with an inline **teal accent word**
  (e.g. "Built for the *Modern Enterprise.*").
- **Eyebrow labels:** small **UPPERCASE, letter-spaced, teal** kickers above
  headings (e.g. `PLATFORM ADVANTAGES`). Use for track section headers.
- **Cards:** large radius (~20px), white, thin light border + soft shadow; a
  **teal line-icon** in a rounded light-tint box top-left; bold navy title; gray
  body; footer meta as small uppercase tags with dot separators. → this is the
  **course tile** and the **module section** styling.
- **Pills/badges:** rounded, thin teal border, light fill (e.g. difficulty/
  duration chips).
- **Buttons:** rounded; primary solid teal/navy, secondary outline; optional
  leading icon. "Start session" = primary.
- **Icons:** consistent teal line-icons (stroke ~1.5). Vendor an inline SVG set;
  map `Track.spec.icon` + difficulty/duration to these.
- Optional floating helper pill bottom-right (like the docs' "What's new?").

Keep it a **design system** driven by the theme env/CSS-vars, not hard-coded — so
primary/secondary/logo swaps re-skin the whole portal.

## 9. Metrics (Prometheus)

`GET /metrics`, scraped via a `ServiceMonitor` (match existing
`80-monitoring.yaml` pattern). At least:

- `dcs_portal_sessions_running{workshop}` — gauge, running sessions per lab
  (from WorkshopSession list).
- `dcs_portal_users_active` — gauge, distinct users with a running session.
- `dcs_portal_session_requests_total{workshop,result}` — counter.
- `dcs_portal_session_provision_seconds` — histogram (request→Running).
- `dcs_portal_catalog_workshops` / `dcs_portal_tracks` — gauges.
- `dcs_portal_feedback_total{workshop}`, `dcs_portal_feedback_rating_avg{workshop}`
  (carry over from feedback-collector).
- `dcs_portal_errors_total{kind}` — counter.

App is **stateless** (all state in CNPG), so it runs ≥1 replica safely — unlike
the old SQLite single-writer. Proper `/healthz` + `/readyz` probes. Use a
Prometheus multiprocess-safe registry if multi-worker (gunicorn), or single-worker
+ threads.

## 10. Security / network

- Reuse the existing **oauth-proxy** gate on `academy` (SSO-only). App trusts
  `X-Forwarded-*`; reads the user token from `X-Forwarded-Access-Token`
  (`--pass-access-token` already set).
- Admin: **SSAR** with the user's token (e.g. can-i delete
  `trainingportals`/`workshopsessions` in the workshops namespace). No group-sync
  dependency.
- Educates `training-portal` Service: **in-cluster only** — no Route, keep the
  NetworkPolicy (ingress from this app + session namespaces only), VAP reserves
  the `academy` host. → "Educates API not exposed" satisfied.
- Robot creds for the Educates REST API read from `TrainingPortal.status`
  (`credentials.robot`, `clients.robot`) via the app SA; never sent to the
  browser (BFF holds them).
- Token scope: SSAR needs `user:check-access`; if the SA-as-OAuthClient default
  scope is `user:info` only, add `--scope=user:info user:check-access` to the
  oauth-proxy args.

## 11. RBAC (app ServiceAccount)

- `get/list/watch`: `workshops`, `trainingportals`, `workshopsessions`
  (`training.educates.dev`), and the new `tracks` (`academy.dcs`).
- `get/list/watch`: `pods` in the session/workshop + vcluster namespaces (label-
  or name-scoped; prefer a Role per relevant namespace set, or a narrow
  ClusterRole).
- SSAR uses the **user** token, not the SA — no extra SA perms for it.

## 12. Helm chart layout (`dcs-academy-portal/chart/`)

Mirror the existing charts' conventions (params list, `image_repository`/Harbor,
`global.registry`, sync-wave annotations, labels helper):

```
chart/
  Chart.yaml            # depends: cloudnative-pg? NO — operator installed separately; only Cluster CR here
  values.yaml           # image, theme.*, feedback.minReviews, tracks[], session.tlsVerify, resources, cnpg.*
  crds/track.yaml       # Track CRD
  templates/
    00-serviceaccount-rbac.yaml
    10-tracks.yaml            # render Track CRs from .Values.tracks
    20-deployment.yaml        # the portal (env: theme, DATABASE_URL, PORTAL_* , scopes)
    21-service.yaml
    30-cnpg-cluster.yaml      # CNPG Cluster CR + app DB secret wiring
    40-networkpolicy.yaml     # lock Educates portal Service to this app + sessions
    50-servicemonitor.yaml
    60-analytics-wiring.yaml  # (or patch trainingportal analytics.webhook.url → this Service)
    _helpers.tpl
```

Integrate with ArgoCD as a new app in `argocd/apps/` (sync-wave after
Educates workshops). Update `20-trainingportal.yaml` oauth-proxy upstream +
`analytics.webhook.url` to target this app.

## 13. Image (`images/dcs-academy-portal/`)

- Base: **`registry.access.redhat.com/hi/python:latest`** — Red Hat **Hardened
  Image** (hummingbird), distroless: no shell, no package manager, nonroot uid
  65532, Python 3.14. Because deps can't be pip-installed there, the build is
  **multi-stage**: a `python:3.14` builder does `pip install --target=/opt/deps
  --only-binary=:all:`, the hardened runtime copies `/opt/deps` and runs
  `python3 -m gunicorn` (no console scripts / PYTHONPATH=/opt/deps). Builder Python
  MINOR must match runtime (3.14 → cp314 wheels; psycopg[binary]≥3.2.10). Mirror to
  Harbor for prod (air-gap); the base pull is fine at build time.
- Self-contained: vendor htmx, CSS, fonts, inline SVG icons, `psycopg`, Flask,
  `prometheus_client`, `kubernetes` client, `tzdata`. **No external fetch except
  the logo.**
- Multi-arch (arm64 for CRC + amd64 for prod). **Dev: push to `ghcr.io/rummens/*`**
  (public, like the other images); mirror to Harbor for prod.
- `build.sh` alongside the existing image builds.

## 14. Resolved + remaining

Resolved (2026-07-12):
- **Feedback data:** fresh start, no migration.
- Concurrency: stateless + CNPG, HA-safe; `/healthz` + `/readyz` + `/metrics`.
- **Base image:** `registry.access.redhat.com/ubi9/python-312`; dev push to
  `ghcr.io/rummens/*`, mirror to Harbor for prod.
- **Track CRD:** `academy.dcs/v1alpha1`, **cluster-scoped**.
- **Design:** match the DCS docs page (§8a), theme-driven.

Verify during build (don't pre-assume):
- **Proxy path allowlist** — confirm the minimal set against a live session
  (start one, watch which `academy/...` paths the session gateway calls).
- **Educates Workshop field paths** — confirm on the live CRD
  (`oc explain workshop.spec`).

## 15. Build order (for the builder session)

1. Scaffold image + Flask app skeleton (health, `/metrics`, config from env).
2. k8s client layer: read Workshop + Track CRs → catalog model.
3. Jinja UI: main (collapsible tracks), course detail, theme CSS-vars.
4. Educates REST client (robot token from TrainingPortal status) + session
   request bound to SSO user.
5. Reverse-proxy allowlist for Educates session paths (the crux — test a live
   session).
6. Provisioning status feed (WorkshopSession + pods) + launch screen + redirect.
7. Absorb feedback: CNPG psycopg backend, analytics webhook, course-view ratings
   (threshold), admin analysis.
8. SSAR admin gate + admin button.
9. Metrics (all §9).
10. Helm chart + Track CRD + CNPG Cluster + RBAC + NetworkPolicy +
    ServiceMonitor; wire oauth-proxy upstream + analytics webhook.
11. Test on CRC (portal-less/oauth as per repo), then prod cluster.

See `BUILD-PROMPT.md` for the self-contained builder prompt.
