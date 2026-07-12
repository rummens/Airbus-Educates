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
# The TrainingPortal CR (name + the namespace it lives in) whose status carries
# the Educates REST robot credentials and the portal-UI namespace.
PORTAL_NAME = os.environ.get("EDUCATES_PORTAL_NAME", "dcst-dcs-backend")
PORTAL_CR_NAMESPACE = os.environ.get("EDUCATES_PORTAL_CR_NAMESPACE", "dcs-educates-workshops")
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
DATABASE_URL = os.environ.get("DATABASE_URL", "")      # postgres://… → CNPG; empty → sqlite
FEEDBACK_DB = os.environ.get("FEEDBACK_DB", "/tmp/feedback.db")   # sqlite path (dev/local)

# Admin gate: SelfSubjectAccessReview with the *user's* token. Admin = whoever
# can perform this verb on this resource in the portal namespace.
ADMIN_SSAR_GROUP = os.environ.get("ADMIN_SSAR_GROUP", "training.educates.dev")
ADMIN_SSAR_RESOURCE = os.environ.get("ADMIN_SSAR_RESOURCE", "trainingportals")
ADMIN_SSAR_VERB = os.environ.get("ADMIN_SSAR_VERB", "delete")
ADMIN_SSAR_NAMESPACE = os.environ.get("ADMIN_SSAR_NAMESPACE", PORTAL_CR_NAMESPACE)

# Header the oauth-proxy passes through with the SSO identity / token.
USER_HEADER = os.environ.get("PORTAL_USER_HEADER", "X-Forwarded-User")
TOKEN_HEADER = os.environ.get("PORTAL_TOKEN_HEADER", "X-Forwarded-Access-Token")

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
