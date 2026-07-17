"""Kubernetes access layer.

Two identities:
  * the app ServiceAccount (in-cluster) — reads Workshop/Track/TrainingPortal/
    WorkshopSession CRs and session pods (catalog + provisioning feed);
  * the *user's* token (from the oauth-proxy header) — one call only, a
    SelfSubjectAccessReview, to decide whether to show/allow admin.

Everything is read-only via the SA except SSAR (which is a create against the
authz API and grants nothing). Session allocation is NOT done here — that is
the Educates REST API's job (see educates.py).
"""
import re
import ssl
import threading
import urllib.error
import urllib.request

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from . import config as cfg
from .cache import Cached
from .icons import resolve_icon

_lock = threading.Lock()
_loaded = False


def _ensure():
    global _loaded
    if _loaded:
        return
    with _lock:
        if _loaded:
            return
        try:
            config.load_incluster_config()
        except config.ConfigException:
            import os
            # local dev: KUBE_CONTEXT picks a kubeconfig context without
            # changing the user's global current-context.
            config.load_kube_config(context=os.environ.get("KUBE_CONTEXT") or None)
        _loaded = True


def _co():
    _ensure()
    return client.CustomObjectsApi()


def _core():
    _ensure()
    return client.CoreV1Api()


# --- catalog ----------------------------------------------------------------

_SENT = re.compile(r"(.+?[.!?])(\s|$)")


def _first_sentence(text):
    if not text:
        return ""
    m = _SENT.match(text.strip())
    return (m.group(1) if m else text.strip()).strip()


def _ann(meta, key, default=""):
    return (meta.get("annotations") or {}).get(f"{cfg.ACADEMY_PREFIX}/{key}", default)


def _lbl(meta, key, default=""):
    return (meta.get("labels") or {}).get(f"{cfg.ACADEMY_PREFIX}/{key}", default)


def _git_source(spec):
    """First git file source on the workshop → (url, ref, root) or None.

    Educates keeps it at spec.workshop.files[].git.{url,ref} (+ newRootPath for a
    subfolder). Empty when the source isn't git (e.g. an OCI image — the air-gap
    default useGit=false, so there is NO git source and both links below are '').
    """
    files = (spec.get("workshop", {}) or {}).get("files", []) or []
    for f in files:
        git = f.get("git") or {}
        url = (git.get("url") or "").rstrip("/")
        if not url:
            continue
        if url.endswith(".git"):
            url = url[:-4]
        # Educates stores the ref remote-qualified (origin/<branch>). Strip only the
        # leading remote — NOT every slash — or a branch like 'feature/academy'
        # collapses to 'academy' and the raw/tree URL 404s. origin/feature/academy
        # → feature/academy; origin/main → main; a bare 'main' is left as-is.
        ref = git.get("ref") or "main"
        for remote in ("origin/", "upstream/"):
            if ref.startswith(remote):
                ref = ref[len(remote):]
                break
        ref = ref or "main"
        return url, ref, (f.get("newRootPath") or "").strip("/")
    return None


def _source_url(spec):
    """Public git URL a workshop is built from → a browseable link (repo root, or
    a subfolder deep-link). Handles GitHub and GitLab-style hosts."""
    g = _git_source(spec)
    if not g:
        return ""
    url, ref, root = g
    if not root:
        return url
    if "github.com" in url:
        return f"{url}/tree/{ref}/{root}"
    return f"{url}/-/tree/{ref}/{root}"                         # gitlab-style


def _readme_raw_url(spec):
    """Raw URL of the lab's README.md from its git file source (for the course
    view's rich description). GitHub → raw.githubusercontent.com; any other host
    is assumed GitLab-style (<url>/-/raw/<ref>/<path>) — Airbus PROD is GitLab, not
    github. Empty when there is no git source (useGit=false → OCI image source):
    the course view then falls back to the CR's own (shorter) spec.description."""
    g = _git_source(spec)
    if not g:
        return ""
    url, ref, root = g
    path = f"{root}/README.md" if root else "README.md"
    if "github.com" in url:
        repo = url.split("github.com/", 1)[-1]                 # owner/repo
        return f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
    return f"{url}/-/raw/{ref}/{path}"                          # gitlab-style


def workshop_file_sources(name):
    """Debug: the raw file sources on one Workshop CR — [{type, url, ref, root}].
    Shows whether content comes from git (README fetchable) or an image (not),
    and the exact git url/ref so a wrong-host/wrong-ref is obvious in the logs."""
    try:
        w = _co().get_cluster_custom_object(
            "training.educates.dev", "v1beta1", "workshops", name)
    except Exception as e:            # noqa: BLE001
        return f"<could not read Workshop {name}: {e}>"
    files = ((w.get("spec", {}) or {}).get("workshop", {}) or {}).get("files", []) or []
    out = []
    for f in files:
        if f.get("git"):
            g = f["git"]
            out.append({"type": "git", "url": g.get("url"), "ref": g.get("ref"),
                        "root": f.get("newRootPath")})
        elif f.get("image"):
            out.append({"type": "image", "url": (f["image"] or {}).get("url"),
                        "root": f.get("newRootPath")})
        else:
            out.append({"type": "other", "keys": list(f.keys())})
    return out


def _uses_vcluster(spec):
    """True if the workshop runs a per-session vcluster (session.applications.
    vcluster.enabled). Drives the 'virtual cluster' vs 'namespace' loading copy."""
    apps = ((spec.get("session", {}) or {}).get("applications", {}) or {})
    return bool((apps.get("vcluster", {}) or {}).get("enabled"))


def _module(spec):
    """The lab's module, from the Educates spec.labels list [{name,value}] entry
    name=module (used to group trophies). Empty if unset."""
    for lbl in (spec.get("labels", []) or []):
        if isinstance(lbl, dict) and lbl.get("name") == "module":
            return lbl.get("value", "") or ""
    return ""


def _prettify(name):
    """Fallback display name from a workshop CR name.
    'lab-a02-kubernetes-essentials' → 'Kubernetes Essentials'."""
    import re as _re
    n = _re.sub(r"^lab-[a-z]?\d+-", "", name)      # strip lab-a02- / lab-3- prefixes
    n = n.replace("-", " ").replace("_", " ").strip()
    return n.title() if n else name


def ping():
    """Cheap API round-trip for readiness. Raises on failure."""
    if cfg.DEMO:
        return
    _core().get_api_resources()       # cheap authenticated round-trip


def _list_tracks_live():
    """Track CRs → sorted list of dicts. Empty if the CRD isn't installed.
    Raises on API error so the cache retains last-known-good (see list_tracks)."""
    if cfg.DEMO:
        return _DEMO_TRACKS
    items = _co().list_cluster_custom_object(
        cfg.TRACK_GROUP, cfg.TRACK_VERSION, "tracks").get("items", [])
    out = []
    for t in items:
        spec = t.get("spec", {})
        out.append({
            "name": t["metadata"]["name"],
            "title": spec.get("title") or t["metadata"]["name"],
            "description": spec.get("description", ""),
            "order": int(spec.get("order", 100)),
            "icon": spec.get("icon", "layers"),
        })
    out.sort(key=lambda x: (x["order"], x["title"]))
    return out


def _list_courses_live():
    """Educates Workshop CRs → course dicts, enriched from academy.dcs/* meta.

    Native Educates fields (title, description) are read from spec; difficulty/
    duration/summary/track/order/author/details come from academy.dcs
    annotations+labels (verified: real Workshop CRs don't populate spec.difficulty
    or spec.duration), each with a sensible spec fallback.

    Raises on API error so the cache retains last-known-good (see list_courses).
    """
    if cfg.DEMO:
        return _DEMO_COURSES
    items = _co().list_cluster_custom_object(
        "training.educates.dev", "v1beta1", "workshops").get("items", [])
    out = []
    for w in items:
        meta, spec = w["metadata"], w.get("spec", {})
        desc = spec.get("description", "")
        name = meta["name"]
        # academy.dcs/display-name wins; else a human spec.title (Educates often
        # leaves it equal to the raw name); else a prettified name.
        spec_title = spec.get("title", "")
        title = _ann(meta, "display-name") or (spec_title if spec_title and spec_title != name else _prettify(name))
        out.append({
            "name": name,
            "title": title,
            "summary": _ann(meta, "summary") or _first_sentence(desc),
            "description": desc,
            "details_md": _ann(meta, "details"),
            "difficulty": (_ann(meta, "difficulty") or spec.get("difficulty", "")).lower(),
            "duration": _ann(meta, "duration") or spec.get("duration", ""),
            "author": _ann(meta, "author") or spec.get("vendor", ""),
            "track": _lbl(meta, "track"),
            "module": _module(spec),
            "order": int(_lbl(meta, "order", "100") or "100"),
            "source_url": _source_url(spec),
            "readme_url": _readme_raw_url(spec),
            "vcluster": _uses_vcluster(spec),
            # academy.dcs/icon (FA-style name) → vendored icon; "" → tile falls
            # back to the track's section icon.
            "icon": resolve_icon(_ann(meta, "icon"), default="") if _ann(meta, "icon") else "",
        })
    out.sort(key=lambda x: (x["order"], x["title"]))
    return out


# Cached + background-refreshed (cache.py). Reads serve the last good catalog if
# the API blips, so a transient failure can't blank the landing page or (worse)
# feed request_session an empty catalog. default [] keeps cold reads from 500ing.
_courses = Cached("workshops", _list_courses_live, ttl=cfg.CATALOG_REFRESH_SECONDS, default=[])
_tracks = Cached("tracks", _list_tracks_live, ttl=cfg.CATALOG_REFRESH_SECONDS, default=[])


def list_courses():
    return _courses.get()


def list_tracks():
    return _tracks.get()


# --- Educates portal wiring (robot creds) -----------------------------------

def portal_status():
    """TrainingPortal .status.educates: robot creds + portal-UI namespace + url.
    TrainingPortal is a CLUSTER-scoped CRD — read it cluster-scoped (no namespace)."""
    obj = _co().get_cluster_custom_object(
        "training.educates.dev", "v1beta1", "trainingportals", cfg.PORTAL_NAME)
    return (obj.get("status", {}) or {}).get("educates", {}) or {}


def portal_service_base():
    """In-cluster base URL of the Educates training-portal Service."""
    if cfg.PORTAL_SERVICE_URL:
        return cfg.PORTAL_SERVICE_URL
    ns = portal_status().get("namespace") or f"{cfg.PORTAL_NAME}-ui"
    return f"http://training-portal.{ns}.svc"


# --- sessions + provisioning feed -------------------------------------------

def list_sessions():
    """All WorkshopSession CRs (for metrics + admin/usage)."""
    try:
        return _co().list_cluster_custom_object(
            "training.educates.dev", "v1beta1", "workshopsessions").get("items", [])
    except ApiException:
        return []


def _route_http_ok(url):
    """HTTP-probe the session URL. The router serves a **503** "Application is not
    available" page while an (even admitted) Route has no ready backend; a live route
    answers 200, or a 3xx/401/403 for the oauth handshake. So: reachable & not 503
    == ready. A connection error / timeout == not ready. This is what the client's
    no-cors probe can't tell (an opaque fetch resolves even on the 503 page)."""
    if not url:
        return False
    ctx = None
    if url.startswith("https") and not cfg.SESSION_TLS_VERIFY:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url), timeout=4, context=ctx)
        return resp.getcode() != 503
    except urllib.error.HTTPError as e:
        return e.code != 503                 # 401/403/3xx-not-followed = route is serving
    except Exception:                        # noqa: BLE001 — DNS/conn/timeout = not ready
        return False


def session_route_ready(session_name, url):
    """True once the session's Route actually serves (not the router's 503 page).

    The WorkshopSession reports Ready before its Route is admitted AND before the
    router has loaded the backend — redirecting then lands on "Application is not
    available" (a reload later works). Two-stage gate:
      1. If we can read the Route (RBAC), require it Admitted — a fast, definitive NO
         while it isn't.
      2. Then HTTP-probe the host: even an admitted Route 503s until the backend is up.
    No Routes RBAC → skip step 1 and rely on the probe (never fail open early)."""
    host = url.split("://", 1)[-1].split("/")[0] if url else ""
    if not host:
        return False
    try:
        routes = _co().list_cluster_custom_object(
            "route.openshift.io", "v1", "routes",
            label_selector=f"training.educates.dev/session.name={session_name}").get("items", [])
        admitted = any(
            (r.get("spec", {}) or {}).get("host") == host
            and c.get("type") == "Admitted" and c.get("status") == "True"
            for r in routes
            for ing in ((r.get("status", {}) or {}).get("ingress") or [])
            for c in (ing.get("conditions") or []))
        if not admitted:
            return False                     # route not admitted yet — definitely not ready
    except ApiException:
        pass                                 # no Routes RBAC → rely on the HTTP probe below
    return _route_http_ok(url)


def session_status(name):
    """One WorkshopSession's .status.educates (phase/message/url)."""
    try:
        obj = _co().get_cluster_custom_object(
            "training.educates.dev", "v1beta1", "workshopsessions", name)
    except ApiException:
        return {}
    return (obj.get("status", {}) or {}).get("educates", {}) or {}


def session_pods(session_name):
    """Pods across the session + vcluster namespaces for a session.

    The workshop pod carries training.educates.dev/session.name=<session>, so one
    all-namespace label query finds it. The vcluster pods (my-vcluster-0, coredns)
    live in <session>-vc but are created by the vcluster chart with ITS OWN labels
    — they do NOT carry the Educates session label (pods don't inherit namespace
    labels). So query that namespace directly and merge, else the vcluster is
    invisible and a vcluster lab's readiness gate never sees it.
    """
    sel = f"training.educates.dev/session.name={session_name}"
    try:
        pods = list(_core().list_pod_for_all_namespaces(label_selector=sel).items)
    except ApiException:
        pods = []
    seen = {(p.metadata.namespace, p.metadata.name) for p in pods}
    try:
        for p in _core().list_namespaced_pod(f"{session_name}-vc").items:
            if (p.metadata.namespace, p.metadata.name) not in seen:
                pods.append(p)
    except ApiException:
        pass          # no vcluster ns (non-vcluster lab) or no RBAC → just the workshop pod
    out = []
    for p in pods:
        cs = p.status.container_statuses or []
        ready = sum(1 for c in cs if c.ready)
        out.append({
            "name": p.metadata.name,
            "namespace": p.metadata.namespace,
            "vcluster": p.metadata.namespace.endswith("-vc"),
            "phase": p.status.phase,
            "ready": ready,
            "total": len(cs),
        })
    return out


# --- admin gate (user token) ------------------------------------------------

def user_can_admin(user_token):
    """SelfSubjectAccessReview with the *user's* token. True = admin."""
    if not user_token:
        return False
    _ensure()
    # Build a FRESH Configuration (reusing only the discovered host/CA) rather than
    # copying the default: load_incluster_config() installs a refresh_api_key_hook
    # that re-injects the SA token on every request, so a copied config ignores the
    # user token and the SSAR silently runs as the SA (which lacks delete → admin
    # button never shows). A fresh config has no hook, so the user token stands.
    d = client.Configuration.get_default_copy()
    ucfg = client.Configuration()
    ucfg.host = d.host
    ucfg.ssl_ca_cert = d.ssl_ca_cert
    ucfg.verify_ssl = d.verify_ssl
    ucfg.api_key = {"authorization": user_token}
    ucfg.api_key_prefix = {"authorization": "Bearer"}
    api = client.AuthorizationV1Api(client.ApiClient(ucfg))
    review = client.V1SelfSubjectAccessReview(
        spec=client.V1SelfSubjectAccessReviewSpec(
            resource_attributes=client.V1ResourceAttributes(
                group=cfg.ADMIN_SSAR_GROUP,
                resource=cfg.ADMIN_SSAR_RESOURCE,
                verb=cfg.ADMIN_SSAR_VERB,
                namespace=cfg.ADMIN_SSAR_NAMESPACE,
            )))
    try:
        res = api.create_self_subject_access_review(review)
        return bool(res.status and res.status.allowed)
    except ApiException:
        return False


# --- demo catalog (PORTAL_DEMO=1, no cluster) -------------------------------
_DEMO_TRACKS = [
    {"name": "developer-basics", "title": "Developer — Basics", "order": 10,
     "icon": "code", "description": "Get productive on DCS: namespaces, workloads, registry."},
    {"name": "platform", "title": "Platform & Operations", "order": 20,
     "icon": "cog", "description": "Run and observe workloads on the shared platform."},
]
_DEMO_COURSES = [
    {"name": "lab-a01-what-is-dcs", "title": "What is DCS?", "track": "developer-basics",
     "order": 10, "summary": "Tour the Digital Container Service and where your workloads live.",
     "description": "A gentle introduction to the DCS platform, its layers and self-service model.",
     "details_md": "", "difficulty": "beginner", "duration": "20 min", "author": "DCS Team",
     "source_url": "https://github.com/rummens/Airbus-Educates/tree/main/dcs-academy/workshops/lab-a01-what-is-dcs",
     "vcluster": False, "module": "", "readme_url": "", "icon": "cloud"},
    {"name": "lab-a02-kubernetes-essentials", "title": "Kubernetes Essentials", "track": "developer-basics",
     "order": 20, "summary": "Pods, deployments and services — the objects you use every day.",
     "description": "Hands-on with the core Kubernetes objects on real OpenShift.",
     "details_md": "", "difficulty": "beginner", "duration": "45 min", "author": "DCS Team",
     "source_url": "https://github.com/rummens/Airbus-Educates/tree/main/dcs-academy/workshops/lab-a02-kubernetes-essentials",
     "vcluster": False, "module": "", "readme_url": "", "icon": "box"},
    {"name": "lab-a04-harbor-registry", "title": "Harbor Registry", "track": "platform",
     "order": 10, "summary": "Push and pull images from the on-prem Harbor registry with skopeo.",
     "description": "Work with the air-gapped Harbor registry: projects, pull-through, skopeo copies.",
     "details_md": "", "difficulty": "intermediate", "duration": "40 min", "author": "DCS Team",
     "source_url": "https://github.com/rummens/Airbus-Educates/tree/main/dcs-academy/workshops/lab-a04-harbor-registry",
     "vcluster": True, "module": "", "readme_url": "", "icon": "database"},
]
