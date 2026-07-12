#!/usr/bin/env python3
"""Deploy a DCS workshop to the local CRC cluster, portal-less, from git.

Creates the three CRs (Workshop + WorkshopEnvironment + WorkshopSession) that
session-manager reconciles directly (the portal SIGILLs on CRC arm64 — see
README.md). Files are pulled from the repo's git remote using the monorepo
`newRootPath` pattern, so no image publish is needed.

By default the workshop container image override is DROPPED (uses the default
base-environment, which has kubectl) so it starts on CRC without the custom
dcs-workshop-base image. Pass --keep-image once that image exists.

Examples:
  ./deploy_workshop.py lab-a02-kubernetes-essentials
  ./deploy_workshop.py lab-a03-namespace-model --vcluster
  ./deploy_workshop.py lab-a02-kubernetes-essentials --delete
"""
import argparse, json, subprocess, sys, time, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_BASE = "workshops-monorepo/tracks/core-track"


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

    return [(name, f"{base}/{name}")]                   # fall back to single name (may be built elsewhere)


def list_labs(ctx):
    """Print all deployed workshop sessions with their phase and URL."""
    r = sh(["oc", "--context", ctx, "get", "workshopsession",
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


def delete_one(ctx, name, sid):
    oc_delete(ctx, "workshopsession", f"{name}-w{sid}")
    oc_delete(ctx, "workshopenvironment", name)
    oc_delete(ctx, "workshop", name)
    print(f"deleted {name} (workshop, env, session)")


def deploy_one(args, name, subpath):
    ctx, sid = args.context, args.id
    session_name = f"{name}-w{sid}"
    url = args.git_url or git_remote_url()
    apps = [a.strip() for a in args.apps.split(",") if a.strip()]
    ws = build_workshop(name, url, args.ref, subpath, args.budget, apps, args.vcluster,
                        args.image, args.registry, title=name, desc=f"{name} (CRC test, git source)")

    # idempotent: drop any prior env/session so content re-pulls fresh
    oc_delete(ctx, "workshopsession", session_name)
    oc_delete(ctx, "workshopenvironment", name)
    time.sleep(2)

    oc_apply(ctx, ws)
    oc_apply(ctx, {"apiVersion": "training.educates.dev/v1beta1", "kind": "WorkshopEnvironment",
                   "metadata": {"name": name}, "spec": {"workshop": {"name": name}}})
    oc_apply(ctx, {"apiVersion": "training.educates.dev/v1beta1", "kind": "WorkshopSession",
                   "metadata": {"name": session_name},
                   "spec": {"environment": {"name": name},
                            "session": {"id": sid, "username": "educates", "password": "educates"}}})

    print(f"git: {url}  ref: {args.ref}  path: {subpath}")
    if not args.wait:
        return
    deadline = time.time() + args.wait
    phase = url_ = ""
    while time.time() < deadline:
        print(f"Still deploying {session_name} (phase: {phase or '(unknown)'})")
        r = sh(["oc", "--context", ctx, "get", "workshopsession", session_name,
                "-o", "jsonpath={.status.educates.phase} {.status.educates.url}"])
        phase, _, url_ = r.stdout.strip().partition(" ")
        if phase == "Running":
            break
        time.sleep(5)
    print(f"phase: {phase or '(unknown)'}")
    if phase != "Running":
        sys.exit("session did not reach Running in time; check "
                 f"'oc --context {ctx} get workshopsession {session_name} -o yaml'")

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
            if code == "200":
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
        print("note: editor/console are separate hosts with the CRC self-signed cert. If their\n"
              "      dashboard tab shows 'temporarily down', open the URL above once and accept\n"
              "      the cert (or trust the CRC ingress CA once — see crc-local-testing/README).")


def main():
    p = argparse.ArgumentParser(description="Deploy a DCS workshop to CRC (portal-less, git source).")
    p.add_argument("name", nargs="?",
                   help="workshop dir name (e.g. lab-a02-kubernetes-essentials) OR a parent "
                        "folder holding several workshop dirs (deploys all of them). Omit with --list.")
    p.add_argument("--id", default="01")
    p.add_argument("--context", default="crc-admin")
    p.add_argument("--git-url", default=None, help="default: repo origin remote")
    p.add_argument("--ref", default="origin/main")
    p.add_argument("--base", default=DEFAULT_BASE, help="path prefix of workshops in the repo")
    p.add_argument("--budget", default="medium")
    p.add_argument("--apps", default="terminal,editor,console,examiner",
                   help="comma list of session applications")
    p.add_argument("--vcluster", action="store_true", help="run in a per-session vcluster")
    p.add_argument("--image", default="ghcr.io/rummens/dcs-workshop-base:dev",
                   help="workshop container image; pass '' to use the default base-environment")
    p.add_argument("--registry", default="ghcr.io/rummens",
                   help="DCS_REGISTRY value for exercise image refs; pass '' to omit")
    p.add_argument("--wait", type=int, default=300, help="seconds to wait for Running (0=don't)")
    p.add_argument("--delete", action="store_true", help="tear down instead of deploy")
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
            delete_one(args.context, name, args.id)
        else:
            deploy_one(args, name, subpath)
        if len(targets) > 1:
            print()


if __name__ == "__main__":
    main()
