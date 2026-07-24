"""Env-driven configuration for the DCS Academy portal.

Everything the app needs comes from the environment (12-factor). Theme values
become CSS variables injected server-side (see app.py / base.html), so a
re-skin is a values.yaml change, not a rebuild. Defaults reproduce the DCS docs
look (navy + teal, Poppins) so an unconfigured deploy already looks on-brand.
"""
import os


def _b(name, default):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


# --- who we talk to ---------------------------------------------------------
# The (cluster-scoped) TrainingPortal CR whose .status carries the Educates REST
# robot credentials and the portal-UI namespace.
PORTAL_NAME = os.environ.get("EDUCATES_PORTAL_NAME", "dcst")
# Only used as the default namespace for the admin SSAR (trainingportals is
# cluster-scoped, so the SSAR namespace is effectively ignored).
PORTAL_CR_NAMESPACE = os.environ.get("EDUCATES_PORTAL_CR_NAMESPACE", "dcs-academy-portal")
# In-cluster base URL of the Educates training-portal Service. Empty = derive
# http://training-portal.<status.educates.namespace>.svc  at runtime.
PORTAL_SERVICE_URL = os.environ.get("EDUCATES_PORTAL_SERVICE_URL", "").rstrip("/")

# Track CRD group/version (cluster-scoped, operator-free — pure catalog data).
TRACK_GROUP = os.environ.get("TRACK_GROUP", "academy.dcs")
TRACK_VERSION = os.environ.get("TRACK_VERSION", "v1alpha1")
ACADEMY_PREFIX = "academy.dcs"        # label/annotation namespace on Workshops

# --- behaviour --------------------------------------------------------------
PORT = int(os.environ.get("PORT", "8080"))
# Serve a bundled sample catalog with no cluster (pure-UI local iteration).
DEMO = _b("PORTAL_DEMO", False)
# Verify TLS on server-side HTTP (Educates REST + reachability probe). Dev
# clusters use self-signed certs → set false there. Default true.
SESSION_TLS_VERIFY = _b("PORTAL_SESSION_TLS_VERIFY", True)
FEEDBACK_MIN_REVIEWS = int(os.environ.get("FEEDBACK_MIN_REVIEWS", "5"))
# Background refresh of the catalog (Educates env catalog + Workshop/Track CRs).
# Keeps the workshop→environment map warm + last-known-good so a stale/empty read
# never makes request_session 404/503 on a dead reference. Seconds.
CATALOG_REFRESH_SECONDS = int(os.environ.get("PORTAL_CATALOG_REFRESH_SECONDS", "300"))
DATABASE_URL = os.environ.get("DATABASE_URL", "")      # postgres://… → CNPG; empty → sqlite
FEEDBACK_DB = os.environ.get("FEEDBACK_DB", "/tmp/feedback.db")   # sqlite path (dev/local)

# Filesystem root of the workshops-monorepo checkout maintained by the git-sync
# sidecar (see slides.py). The portal serves each lab's workshop/slides/ dir from
# here at /slides/<lab>/ so decks are readable without starting a session. Empty
# (no sidecar) → the Slides feature is off (button hidden, /slides 404s).
SLIDES_ROOT = os.environ.get("PORTAL_SLIDES_ROOT", "").rstrip("/")

# Admin gate: SelfSubjectAccessReview with the *user's* token. Admin = whoever
# can perform this verb on this resource in the portal namespace.
ADMIN_SSAR_GROUP = os.environ.get("ADMIN_SSAR_GROUP", "training.educates.dev")
ADMIN_SSAR_RESOURCE = os.environ.get("ADMIN_SSAR_RESOURCE", "trainingportals")
ADMIN_SSAR_VERB = os.environ.get("ADMIN_SSAR_VERB", "delete")
ADMIN_SSAR_NAMESPACE = os.environ.get("ADMIN_SSAR_NAMESPACE", PORTAL_CR_NAMESPACE)

# Shared token for the machine-triggered catalog rescan (POST /admin/rescan),
# used by the workshops chart's ArgoCD PostSync hook. Empty = token auth off, so
# only an SSAR admin user can trigger a rescan (the Job path is then disabled).
RESCAN_TOKEN = os.environ.get("PORTAL_RESCAN_TOKEN", "")

# --- login (portal is the OpenShift OAuth client; no oauth-proxy) -----------
# The portal runs the OAuth2 authorization-code flow itself against the cluster's
# OpenShift OAuth server (ServiceAccount-as-OAuthClient), so it learns the real
# user identity + token and sets its own session cookie. When disabled the portal
# is open (local/dev) and _user() is empty.
OAUTH_ENABLED = _b("PORTAL_OAUTH_ENABLED", True)
# client_id = system:serviceaccount:<ns>:<sa>; client_secret = a token for that SA
# (the projected SA token, used only for the server-side code exchange).
OAUTH_CLIENT_ID = os.environ.get("PORTAL_OAUTH_CLIENT_ID", "")
OAUTH_CLIENT_SECRET_FILE = os.environ.get(
    "PORTAL_OAUTH_CLIENT_SECRET_FILE", "/var/run/secrets/kubernetes.io/serviceaccount/token")
# Public callback URL the OAuth server redirects the browser back to. Must match
# the SA's serviceaccounts.openshift.io/oauth-redirecturi annotation.
OAUTH_REDIRECT_URL = os.environ.get("PORTAL_OAUTH_REDIRECT_URL", "")
# SA-as-OAuthClient only permits user:info (enough to read the username).
OAUTH_SCOPE = os.environ.get("PORTAL_OAUTH_SCOPE", "user:info")
# Where to discover the OAuth authorize/token endpoints, and where to read the
# user identity (users/~). Default = in-cluster API (reliable pod-side DNS + CA).
OAUTH_ISSUER_URL = os.environ.get("PORTAL_OAUTH_ISSUER_URL", "https://kubernetes.default.svc").rstrip("/")
OAUTH_API_URL = os.environ.get("PORTAL_OAUTH_API_URL", "https://kubernetes.default.svc").rstrip("/")
# Optional explicit overrides if discovery/DNS is awkward (e.g. CRC). Empty =
# use discovery from OAUTH_ISSUER_URL.
OAUTH_AUTHORIZE_URL = os.environ.get("PORTAL_OAUTH_AUTHORIZE_URL", "").rstrip("/")
OAUTH_TOKEN_URL = os.environ.get("PORTAL_OAUTH_TOKEN_URL", "").rstrip("/")
# CA bundle for the server-side calls (discovery + token + users/~). Default = SA
# CA. The external oauth route cert may differ → set OAUTH_TLS_VERIFY=false on
# self-signed dev clusters (CRC).
OAUTH_CA_FILE = os.environ.get("PORTAL_OAUTH_CA_FILE", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt")
OAUTH_TLS_VERIFY = _b("PORTAL_OAUTH_TLS_VERIFY", True)
# Flask session cookie signing key. Set from a Secret so sessions survive restarts
# and pod replicas agree; empty = ephemeral random (dev only).
SESSION_SECRET = os.environ.get("PORTAL_SESSION_SECRET", "")
# SameSite for the portal session cookie. MUST be "None" for the embedded Console/
# Editor tabs to work: those are separate cross-origin session subdomains
# (console-<session>/editor-<session>) whose iframes do an Educates oauth_handshake
# back to the portal — with "Lax" the portal cookie isn't sent in that third-party
# context, the portal 302s to OpenShift OAuth inside the iframe, and the OAuth page
# (X-Frame-Options: DENY) refuses to frame → "page unavailable". "None" needs Secure
# (set below). Set "Lax" only on a deploy that doesn't embed the console/editor.
SESSION_COOKIE_SAMESITE = os.environ.get("PORTAL_SESSION_COOKIE_SAMESITE", "None")
# Local/dev identity fallback: when OAuth is off there is no logged-in user, so
# progress/trophies have no one to bind to. Set PORTAL_DEV_USER to a fixed name
# to exercise per-user features locally. Unset in prod (OAuth provides identity).
DEV_USER = os.environ.get("PORTAL_DEV_USER", "")

# --- theme (→ CSS variables) ------------------------------------------------
# Only primary/secondary/logo are "required" per the plan; all have on-brand
# defaults so nothing breaks unconfigured.
THEME = {
    "primary": os.environ.get("THEME_PRIMARY_COLOR", "#002157"),      # DCS navy (logo "DC" + cube)
    "secondary": os.environ.get("THEME_SECONDARY_COLOR", "#00a2c1"),  # DCS teal (logo "S" + flower)
    "accent": os.environ.get("THEME_ACCENT_COLOR", "") or os.environ.get("THEME_SECONDARY_COLOR", "#00a2c1"),
    "background": os.environ.get("THEME_BACKGROUND", "#f7fafb"),
    "product_name": os.environ.get("THEME_PRODUCT_NAME", "DCS Academy"),
    "logo_url": os.environ.get("THEME_LOGO_URL", ""),                 # empty → built-in inline DCS mark
    "favicon": os.environ.get("THEME_FAVICON", "🧊"),
    "font_family": os.environ.get("THEME_FONT_FAMILY", "Poppins"),
    "footer_html": os.environ.get("THEME_FOOTER_HTML", ""),
}
