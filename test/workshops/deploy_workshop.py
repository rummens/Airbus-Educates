#!/usr/bin/env python3
"""Deploy a DCS workshop to OpenShift, portal-less, from git.

Creates the three CRs (Workshop + WorkshopEnvironment + WorkshopSession) that
session-manager reconciles directly (portal-less is a speed/isolation choice, not a
limitation — see README.md). Files are pulled from the repo's git remote using the monorepo
`newRootPath` pattern, so no image publish is needed.

By default the workshop container image override is DROPPED (uses the default
base-environment, which has kubectl) so it starts without the custom
dcs-workshop-base image. Pass --keep-image once that image exists.

Examples:
  ./deploy_workshop.py lab-a02-kubernetes-essentials
  ./deploy_workshop.py lab-a03-namespace-model --vcluster
  ./deploy_workshop.py lab-a02-kubernetes-essentials --delete
"""
import os
import re
import argparse, json, subprocess, sys, time, pathlib
try:
    import yaml                       # to lift the authored session block (objects/ingresses)
except ImportError:
    yaml = None

def _repo_root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True,
                       cwd=str(pathlib.Path(__file__).resolve().parent))
    if r.returncode == 0 and r.stdout.strip():
        return pathlib.Path(r.stdout.strip())
    return pathlib.Path(__file__).resolve().parents[2]   # test/workshops/x.py -> repo root

REPO_ROOT = _repo_root()
DEFAULT_BASE = "tracks/core-track"


def _default_context():
    """Return the current oc context name, falling back to 'logged-user'."""
    r = subprocess.run(["oc", "config", "current-context"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    return "logged-user"


def default_git_ref():
    """Read the configured git ref (`workshopContent.gitRef`) from the workspace values.yaml.

    Fall back to 'origin/main' if the file or key is missing/unreadable. This keeps the
    smoke/deploy tools pulling the same workshop content the catalog actually serves.
    """
    values = REPO_ROOT / "values.yaml"
    if values.exists():
        try:
            text = values.read_text()
            m = re.search(r"^\s*gitRef:\s*(\S+)\s*$", text, re.MULTILINE)
            if m:
                return m.group(1)
        except OSError:
            pass
    return "origin/main"


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def git_remote_url():
    r = sh(["git", "-C", str(REPO_ROOT), "config", "--get", "remote.origin.url"])
    url = r.stdout.strip()
    if url.startswith("git@github.com:"):          # normalise ssh -> https
        url = "https://github.com/" + url[len("git@github.com:"):]
    return url.removesuffix(".git")


def oc_apply(ctx, obj):
    r = sh(["oc", "--context", ctx, "apply", "-f", "-"], input=json.dumps(obj))
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stderr.write(r.stderr)
        sys.exit(f"apply failed for {obj['kind']}/{obj['metadata']['name']}")


def oc_delete(ctx, kind, name):
    sh(["oc", "--context", ctx, "delete", kind, name, "--ignore-not-found", "--wait=false"])


def authored_session_extras(subpath):
    """Lift `session.objects` + `session.ingresses` from the workshop's real
    resources/workshop.yaml so labs that pre-provision RBAC / extra namespaces /
    NetworkPolicies / app ingresses (e.g. A04, A06) deploy faithfully.

    The synthesized session spec below omits these; without them those labs'
    examiner checks fail for reasons that would NOT happen on the real cluster.

    The file is Helm-templated, but only spec.workshop.{image,files} carry `{{ }}`
    — the session block (the last key under spec) is plain YAML, so we parse just
    that fragment. Returns {} when there's nothing to add (or yaml is unavailable).
    """
    if yaml is None:
        return {}
    f = REPO_ROOT / subpath / "resources" / "workshop.yaml"
    if not f.exists():
        return {}
    text = f.read_text()
    idx = text.find("\n  session:")
    if idx < 0:
        return {}
    frag = text[idx + 1:]                                 # from the '  session:' line to EOF
    frag = "\n".join(l[2:] if l.startswith("  ") else l for l in frag.splitlines())  # dedent 2
    try:
        sess = (yaml.safe_load(frag) or {}).get("session", {}) or {}
    except yaml.YAMLError:
        return {}
    return {k: sess[k] for k in ("objects", "ingresses") if k in sess}


def build_workshop(name, url, ref, subpath, budget, apps, vcluster, image, registry, title, desc):
    inc = [f"/{subpath}/workshop/**", f"/{subpath}/exercises/**", f"/{subpath}/README.md"]
    application = {a: {"enabled": True} for a in apps}
    if "terminal" in application:
        application["terminal"]["layout"] = "split"
    session = {
        "namespaces": {"budget": budget, "security": {"token": {"enabled": True}}},
        "applications": application,
    }
    if registry:                                     # DCS_REGISTRY for exercise manifests
        session["env"] = [{"name": "DCS_REGISTRY", "value": registry}]
    if vcluster:
        application["vcluster"] = {"enabled": True}
        session["namespaces"]["budget"] = "large"      # vcluster needs large
        session["objects"] = [{                          # privileged SCC for the -vc ns
            "apiVersion": "rbac.authorization.k8s.io/v1", "kind": "RoleBinding",
            "metadata": {"name": "educates-vcluster-scc", "namespace": "$(vcluster_namespace)"},
            "roleRef": {"apiGroup": "rbac.authorization.k8s.io", "kind": "ClusterRole",
                        "name": "educates-privileged-scc"},
            "subjects": [{"apiGroup": "rbac.authorization.k8s.io", "kind": "Group",
                          "name": "system:serviceaccounts:$(vcluster_namespace)"}],
        }]
    # Merge the authored session extras (RBAC, extra namespaces, NetworkPolicies,
    # app ingresses) so labs that pre-provision them test faithfully.
    extras = authored_session_extras(subpath)
    if extras.get("objects"):
        session.setdefault("objects", []).extend(extras["objects"])
    if extras.get("ingresses"):
        session["ingresses"] = extras["ingresses"]
    workshop = {"files": [{"git": {"url": url, "ref": ref},
                           "includePaths": inc, "newRootPath": subpath}]}
    if image:
        workshop["image"] = image
    return {
        "apiVersion": "training.educates.dev/v1beta1", "kind": "Workshop",
        "metadata": {"name": name},
        "spec": {"title": title, "description": desc, "workshop": workshop, "session": session},
    }


def is_workshop_dir(d):
    return (d / "resources" / "workshop.yaml").exists()


def resolve_targets(name, base):
    """Map the positional into a list of (workshop_name, repo_relative_subpath).

    Accepts a single workshop dir name (under --base), OR a path to a parent
    folder holding several workshop dirs (deploy them all). The subpath must be
    inside the repo — the git file source pulls from there.
    """
    by_base = REPO_ROOT / base / name
    if is_workshop_dir(by_base):                       # single workshop under --base
        return [(name, f"{base}/{name}")]

    given = pathlib.Path(name)
    given = given if given.is_absolute() else (REPO_ROOT / given)

    for cand in (by_base, given):                      # parent folder → all child workshops
        if cand.is_dir():
            try:
                rel_parent = cand.resolve().relative_to(REPO_ROOT)
            except ValueError:
                sys.exit(f"{cand} is outside the repo ({REPO_ROOT}); the git source can only pull in-repo paths.")
            kids = sorted(d for d in cand.iterdir() if d.is_dir() and is_workshop_dir(d))
            if kids:
                return [(d.name, f"{rel_parent}/{d.name}") for d in kids]

    if is_workshop_dir(given):                          # a path straight to one workshop
        return [(given.name, str(given.resolve().relative_to(REPO_ROOT)))]

    cross = all_workshop_paths().get(name)              # any track (dev-/security-track)
    if cross:
        return [(name, cross)]

    return [(name, f"{base}/{name}")]                   # fall back to single name (may be built elsewhere)


def all_workshop_paths():
    """Every workshop in the monorepo, across all tracks → {name: repo_relative_subpath}."""
    root = REPO_ROOT / "tracks"
    out = {}
    if root.is_dir():
        for track in sorted(root.iterdir()):
            if not track.is_dir():
                continue
            for d in sorted(track.iterdir()):
                if d.is_dir() and is_workshop_dir(d):
                    out[d.name] = str(d.relative_to(REPO_ROOT))
    return out


def find_subpath(name):
    """Repo-relative subpath of a workshop by name, searching ALL tracks (not just --base).
    Returns None if not found."""
    return all_workshop_paths().get(name)


# Label that hides a Workshop CR from the TrainingPortal catalog. The throwaway
# MR-test Workshop sets this so it never shows up as a launchable course, even though
# it lives in the Educates namespace alongside the Argo-managed catalog Workshops.
DISABLE_LABEL = "training.educates.dev/disable.workshop"


def throwaway_name(name, ref=None):
    """Deterministic name for a throwaway (MR-test) Workshop: <lab>-mr-<suffix>.

    Suffix is derived from the git ref so the same MR branch reuses (overwrites) its own
    throwaway but never collides with another branch's, nor with the Argo-managed catalog
    Workshop of the same lab (which keeps its plain <lab> name). Idempotent: already-throwaway
    names are returned unchanged, so it's safe to call from both smoke_test and deploy_one.
    """
    if "-mr-" in name:
        return name
    return f"{name}-mr-{_ref_suffix(ref)}"


def _ref_suffix(ref=None):
    """Short sanitised suffix from a git ref. Defaults to configured gitRef / GIT_REF."""
    ref = ref or os.environ.get("GIT_REF") or default_git_ref()
    ref = re.sub(r"[^A-Za-z0-9]", "", ref)
    return (ref or "x")[:8].lower()


def list_labs(ctx):
    """Print all deployed workshop sessions with their phase and URL."""
    r = sh(["oc", "--context", ctx, "get", "workshopsessions.training.educates.dev",
            "-o", "custom-columns=SESSION:.metadata.name,ENVIRONMENT:.spec.environment.name,"
            "PHASE:.status.educates.phase,URL:.status.educates.url", "--no-headers"])
    if r.returncode:
        sys.stderr.write(r.stderr)
        sys.exit("could not list workshop sessions")
    rows = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not rows:
        print("no workshop sessions deployed.")
        return
    print(f"{'SESSION':<40} {'PHASE':<12} URL")
    for ln in rows:
        parts = ln.split()
        sess = parts[0] if parts else "?"
        phase = parts[2] if len(parts) > 2 else "-"
        url = parts[3] if len(parts) > 3 and parts[3] != "<none>" else ""
        print(f"{sess:<40} {phase:<12} {url}")
    print(f"\n{len(rows)} session(s).")


def delete_one(ctx, name, sid, throwaway=False, ref=None):
    # In throwaway mode everything was deployed under the throwaway name; delete that.
    ws_name = throwaway_name(name, ref=ref) if throwaway else name
    oc_delete(ctx, "workshopsessions.training.educates.dev", f"{ws_name}-w{sid}")
    oc_delete(ctx, "workshopenvironments.training.educates.dev", ws_name)
    if throwaway:
        # The throwaway Workshop CR was created by us (not Argo), so we own its
        # teardown too. Leave the catalog Workshop of the same lab untouched.
        oc_delete(ctx, "workshops.training.educates.dev", ws_name)
    # Don't delete the namespace — the workshop controller manages its lifecycle.
    # Deleting it causes the next environment creation to fail ("namespace already exists").
    print(f"deleted {ws_name} (env, session" + (", throwaway workshop)" if throwaway else ")"))


def deploy_one(args, name, subpath):
    ctx, sid = args.context, args.id
    throwaway = bool(getattr(args, "throwaway", False))
    # The effective Workshop/namespace name: a throwaway MR-test Workshop gets a
    # unique <lab>-mr-<ref> name (hidden from the portal), everything else uses the
    # catalog Workshop name.
    ws_name = throwaway_name(name, args.ref) if throwaway else name
    session_name = f"{ws_name}-w{sid}"
    url = args.git_url or git_remote_url()
    apps = [a.strip() for a in args.apps.split(",") if a.strip()]

    # idempotent: drop any prior env/session so content re-pulls fresh. Wait for the
    # env namespace to actually disappear before recreating — recreating while the
    # old ns is still Terminating makes the new session stick in Pending.
    oc_delete(ctx, "workshopsessions.training.educates.dev", session_name)
    oc_delete(ctx, "workshopenvironments.training.educates.dev", ws_name)
    ns_deadline = time.time() + 180
    while time.time() < ns_deadline:
        r = sh(["oc", "--context", ctx, "get", "namespace", ws_name,
                "--no-headers", "-o", "custom-columns=STATUS:.status.phase"])
        if r.returncode != 0:
            break  # namespace no longer exists
        status = r.stdout.strip()
        if not status:
            break  # namespace exists but has no status (deleted)
        print(f"  waiting for namespace {ws_name} to be deleted (status: {status})...")
        time.sleep(2)

    if throwaway:
        # MR-mode: build a throwaway Workshop CR that pulls the MR branch's content.
        # It has its own name (so it never shadows / collides with the Argo-managed
        # catalog Workshop), carries the disable label (hidden from the portal), and is
        # owned by us — deleted on teardown.
        tw = build_workshop(ws_name, url, args.ref, subpath, args.budget, apps,
                            args.vcluster, args.image, args.registry,
                            title=f"{name} (MR test)", desc=f"{name} (MR test, ref {args.ref})")
        tw["metadata"].setdefault("labels", {})[DISABLE_LABEL] = "true"
        oc_apply(ctx, tw)
    else:
        # Reuse the existing catalog Workshop CR (portal pattern): create only the
        # Environment and Session. The Workshop CR is already reconciled by Argo/the
        # catalog, so we don't create a new one here.
        pass

    oc_apply(ctx, {"apiVersion": "training.educates.dev/v1beta1", "kind": "WorkshopEnvironment",
                   "metadata": {"name": ws_name}, "spec": {"workshop": {"name": ws_name}}})

    # Wait for the environment to reach Running before creating the session. The
    # workshop controller populates status.educates.workshop asynchronously, and the
    # session handler reads that key — creating the session too early fails with
    # KeyError: 'workshop' until the environment status is ready.
    env_deadline = time.time() + 120
    while time.time() < env_deadline:
        r = sh(["oc", "--context", ctx, "get", "workshopenvironments.training.educates.dev", ws_name,
                "-o", "jsonpath={.status.educates.phase}"])
        phase = r.stdout.strip()
        if phase == "Running":
            break
        print(f"  waiting for environment {ws_name} to reach Running (phase: {phase or '(unknown)'})")
        time.sleep(5)
    else:
        sys.exit(f"environment {ws_name} did not reach Running in time (phase: {phase or '(unknown)'})")

    oc_apply(ctx, {"apiVersion": "training.educates.dev/v1beta1", "kind": "WorkshopSession",
                   "metadata": {"name": session_name},
"spec": {"environment": {"name": ws_name},
                             "session": {"id": sid, "username": "educates", "password": "educates"}}})

    print(f"git: {url}  ref: {args.ref}  path: {subpath}")
    if not args.wait:
        return
    deadline = time.time() + args.wait
    phase = url_ = ""
    while time.time() < deadline:
        print(f"Still deploying {session_name} (phase: {phase or '(unknown)'})")
        r = sh(["oc", "--context", ctx, "get", "workshopsessions.training.educates.dev", session_name,
                "-o", "jsonpath={.status.educates.phase} {.status.educates.url}"])
        phase, _, url_ = r.stdout.strip().partition(" ")
        if phase == "Running":
            break
        time.sleep(5)
    print(f"phase: {phase or '(unknown)'}")
    if phase != "Running":
        sys.exit("session did not reach Running in time; check "
                 f"'oc --context {ctx} get workshopsessions.training.educates.dev {session_name} -o yaml'")

    # App routes are created per enabled application (editor-/console-<session>).
    # phase=Running can precede the app backends being ready, so wait for the
    # editor to actually answer before declaring done — that's the "editor page
    # temporarily down" the user hit when opening it too early.
    editor = url_.replace("https://", "https://editor-", 1)
    console = url_.replace("https://", "https://console-", 1)
    if url_:
        end = time.time() + 90
        while time.time() < end:
            code = sh(["curl", "-sk", "-m", "5", "-o", "/dev/null", "-w", "%{http_code}",
                       "-u", "educates:educates", editor]).stdout.strip()
            # 200 = served; 3xx = redirect (Educates dashboard 302s to its own path / login)
            # — both mean the endpoint is up. A dead endpoint gives 000/502/503.
            if code and code[0] in "23":
                break
            print(f"waiting for editor to be ready (http {code or '...'})")
            time.sleep(5)
    print("login: educates / educates  (accept the self-signed cert)")
    print(f"dashboard: {url_}")
    if "editor" in apps:
        print(f"editor:    {editor}")
    if "console" in apps:
        print(f"console:   {console}")
    if "editor" in apps or "console" in apps:
        print("note: editor/console are separate hosts; if the dashboard\n"
              "      tab shows 'temporarily down', open the editor/console URL in a new tab and\n"
              "      accept the cert (or trust the cluster ingress CA once).")


def main():
    p = argparse.ArgumentParser(description="Deploy a DCS workshop portal-less, from git.")
    p.add_argument("name", nargs="?",
                   help="workshop dir name (e.g. lab-a02-kubernetes-essentials) OR a parent "
                        "folder holding several workshop dirs (deploys all of them). Omit with --list.")
    p.add_argument("--id", default="01")
    p.add_argument("--context", default=_default_context())
    p.add_argument("--git-url", default=None, help="default: repo origin remote")
    p.add_argument("--ref", default=default_git_ref())
    p.add_argument("--base", default=DEFAULT_BASE, help="path prefix of workshops in the repo")
    p.add_argument("--budget", default="medium")
    p.add_argument("--apps", default="terminal,editor,console,examiner",
                   help="comma list of session applications")
    p.add_argument("--vcluster", action="store_true", help="run in a per-session vcluster")
    p.add_argument("--image", default="ghcr.io/rummens/dcs-workshop-base:develop",
                   help="workshop container image; pass '' to use the default base-environment")
    p.add_argument("--registry", default="registry.dcs.aircloud.common.airbusds.corp/dcs-internal-images/dcs-academy",
                   help="DCS_REGISTRY value for exercise image refs; pass '' to omit")
    p.add_argument("--wait", type=int, default=300, help="seconds to wait for Running (0=don't)")
    p.add_argument("--delete", action="store_true", help="tear down instead of deploy")
    p.add_argument("--throwaway", action="store_true",
                   help="deploy a throwaway Workshop (MR mode): a <lab>-mr-<ref> Workshop, "
                        "hidden from the portal, pulling content from --ref; never touches the "
                        "Argo-managed catalog Workshop of the same lab.")
    p.add_argument("--list", action="store_true", help="list all deployed workshop sessions and exit")
    args = p.parse_args()

    if args.list:
        list_labs(args.context)
        return

    if not args.name:
        p.error("a workshop name or parent folder is required (or use --list)")

    targets = resolve_targets(args.name, args.base)
    if len(targets) > 1:
        print(f"{'deleting' if args.delete else 'deploying'} {len(targets)} workshops: "
              f"{', '.join(n for n, _ in targets)}\n")

    for i, (name, subpath) in enumerate(targets, 1):
        if len(targets) > 1:
            print(f"===== [{i}/{len(targets)}] {name} =====")
        if args.delete:
            delete_one(args.context, name, args.id,
                       throwaway=args.throwaway, ref=args.ref)
        else:
            deploy_one(args, name, subpath)
        if len(targets) > 1:
            print()


if __name__ == "__main__":
    main()
