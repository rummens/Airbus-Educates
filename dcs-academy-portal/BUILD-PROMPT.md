# Build prompt — DCS Academy custom training portal

Paste this into a fresh Claude Code session at the repo root
(`/Users/marcel/PycharmProjects/Airbus-Educates`). It is self-contained; it
points at the design and the repo files you need.

---

You are building a **custom training portal** for the DCS Academy — a Flask app
that replaces the built-in Educates training portal landing/catalog UI, while
leaving the Educates workshop **session** runtime (dashboard: instructions,
terminal, editor) completely untouched.

**Read first, in order:**
1. `dcs-academy-portal/PLAN.md` — the full design and every locked decision.
   This is authoritative; follow it.
2. `CLAUDE.md` — repo guide + non-negotiable house standards (OpenShift `oc`,
   air-gapped Harbor images, variablize everything, params as a **list**).
3. `HANDOVER-oauth-gating.md` — how the `academy` host, oauth-proxy, and Educates
   session `oauth_handshake` interact. Critical for the reverse-proxy part.
4. `images/feedback-collector/app.py` — the feedback service you will absorb
   (endpoints, schema, CNPG `DATABASE_URL` seam).
5. `dcs-academy-workshops/templates/` — existing chart:
   `20-trainingportal.yaml`, `40-auth.yaml` (oauth-proxy), `50-portal-netpol.yaml`,
   `60-feedback-collector.yaml`, `80-monitoring.yaml`/ServiceMonitor pattern.
6. Auto-memory notes `educates-oauth-gating-openshift`, `crc-workshop-testing`,
   `dcs-domain-corrections`.
7. `dcs-academy-portal/Digital Container Services _ DCS.pdf` — print dump of the
   DCS docs landing page. **This is the visual target** (PLAN §8a): navy + teal
   palette, rounded white cards with teal line-icons, uppercase teal eyebrow
   labels, pill badges, bold geometric sans, hex-atom "DCS" logo. Render it
   (`Read` the PDF pages) and match the design as the theme defaults.

**What to build** (details in PLAN.md — do not restate, implement):

- `images/dcs-academy-portal/` — Flask app + Containerfile on
  **`registry.access.redhat.com/ubi9/python-312`**. Self-contained: vendor htmx,
  CSS, fonts, inline SVG icons, `psycopg`, `prometheus_client`, `kubernetes`
  client, `tzdata`. **No external calls except the configurable logo URL.**
  Multi-arch; **dev push to `ghcr.io/rummens/*`** (mirror to Harbor for prod).
- The app:
  - Server-rendered **Jinja + htmx/vanilla** UI: main page with **collapsible
    per-Track sections** → course tiles (title, one-sentence summary, complexity
    icon, duration icon, star rating if reviews ≥ threshold); course detail page;
    **Start session** → custom **provisioning screen** with a live status feed;
    **302 redirect** to the session host when ready.
  - Catalog from the **k8s API**: read Educates `Workshop` CRs + the new `Track`
    CRs (verify exact Workshop field paths on the live CRD).
  - Session lifecycle via the Educates **REST API** (robot token from
    `TrainingPortal.status`), request **bound to the SSO user** (`user` param
    from `X-Forwarded-Access-Token`). Do not reimplement session allocation.
  - **Reverse-proxy** an allowlist of Educates portal paths (`/oauth2/…`,
    `/oauth_callback`, `/workshops/session/…`, `/session/…`,
    `/workshops/environment/…`, `/workshops/catalog/…`) to the in-cluster
    Educates `training-portal` Service, so `PORTAL_HOSTNAME=academy` keeps the
    session `oauth_handshake` working. **Verify the minimal allowlist against a
    live session** — under-proxy breaks sessions, over-proxy re-exposes the
    Educates UI.
  - Live **provisioning status feed** merging `WorkshopSession.status.educates.
    phase`/`.message` + pods in the workshop namespace + pods in the vcluster
    namespace, mapped to human steps.
  - **Absorb feedback** into the app, storage **→ CloudNativePG** (implement the
    psycopg backend behind the existing `DATABASE_URL` seam). **Fresh start — no
    migration of old SQLite rows.** Course view shows **ratings only** (avg +
    count) when count ≥ `FEEDBACK_MIN_REVIEWS` (default 5). Comments only in admin.
  - **Admin** view (feedback analysis: ratings + comments + session/usage),
    gated by **SelfSubjectAccessReview** with the user's token; admin button
    shown only if SSAR passes.
  - **Theme** from env: `THEME_PRIMARY_COLOR`, `THEME_SECONDARY_COLOR`,
    `THEME_LOGO_URL` required; accent/product-name/favicon/background/font/footer
    optional. Inject as CSS variables server-side.
  - **Prometheus** `/metrics` (see PLAN §9: running sessions per lab, active
    users, request counter, provision-time histogram, catalog/track gauges,
    feedback metrics, errors). Stateless → HA-safe.
  - `PORTAL_SESSION_TLS_VERIFY=false` disables cert verification on server-side
    HTTP calls (dev cluster self-signed certs). Default `true`.
- `dcs-academy-portal/chart/` — Helm chart (layout in PLAN §12): `Track` CRD,
  Track CRs rendered from `values.tracks`, Deployment/Service, **CNPG `Cluster`
  CR** (operator installed separately — chart depends, does not install it),
  RBAC (PLAN §11), NetworkPolicy locking the Educates Service to this app +
  session namespaces, ServiceMonitor. Follow the existing charts' conventions
  (params as a **list**, `global.registry`/Harbor image rewrite, sync-waves,
  labels helper).
- Wire-ins: change oauth-proxy `--upstream` (in `40-auth.yaml`) to this app's
  Service; point `TrainingPortal.analytics.webhook.url` at this app; retire the
  standalone `feedback-collector` once absorbed; add an `argocd/apps/` entry.

**House standards (must follow):** OpenShift `oc` never `kubectl`; every image
from Harbor (`$(image_repository)` / `global.registry`), no external registries;
variablize everything; `config.yaml`/values `params` is a **list of {name,value}**.

**Testing:** use `crc-local-testing/` flow (portal-less on CRC arm64, git-source
reads `origin/main` so push content before redeploy; editor needs the CRC
self-signed cert trusted). Confirm: main page renders tracks+courses, a session
starts and the provisioning screen shows real phases, redirect lands in a working
Educates session (no "content blocked"/handshake break), feedback writes to CNPG,
admin gate works for an admin and 403s a non-admin, `/metrics` scrapes.

**Decisions are locked (PLAN §2, §14).** Do NOT re-ask them. Two things to
**verify against the live cluster during build** (don't pre-assume): the minimal
Educates proxy path allowlist (watch a real session), and the exact Educates
Workshop field paths (`oc explain workshop.spec`).

**Git:** commit when asked; don't push without asking (push deploys via ArgoCD).
Commit trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

Work in this order: PLAN §15 build order (1→11). Ship incrementally; keep the app
lazy and self-contained — reuse the feedback app's code, don't rewrite it.
