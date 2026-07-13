# HANDOVER — OpenShift console in the workshop "Console" tab + user-usable session namespace

Investigation for the request: *"make the session namespace usable by the human learner,
not just the service account, and open the OpenShift web console inside the Console tab so
the learner can choose the console over the CLI."*

Date: 2026-07-13. Cluster checked: `ocp-test.demo.rummens.de` + local CRC. Educates **3.7.2**.

## TL;DR

- The **Console tab already works today** and already lets a learner drive their session
  namespace from a GUI instead of the CLI — it is the **Kubernetes Dashboard**, bound to the
  session namespace, running as the session ServiceAccount which holds `admin` on that
  namespace. Every workshop already sets `spec.session.applications.console.enabled: true`.
  The functional goal ("use the console instead of the CLI") is **met**.
- Putting the **actual OpenShift-branded web console** in that tab, and making the namespace
  usable **as the human's own OpenShift identity**, are both **blocked by platform-level
  constraints outside this repo (tenant-side GitOps) and outside Educates 3.7.2**. Details
  below. No workshop change ships for this — it needs a platform decision.

## Why the OpenShift console can't be embedded

1. **Educates has no `openshift` console vendor.** In 3.7.2 the console app is the k8s
   Dashboard; `spec.session.applications.console.vendor` accepts only `kubernetes` (default)
   or `octant`. Source: `base-environment/.../profile.d/02-console.sh` (case switch on
   `.spec.session.applications.console.vendor`, default `kubernetes`). The console binary is
   `/opt/console/dashboard` (`sbin/start-console`).
2. **The OpenShift console refuses to be framed.** Measured on the console route:
   ```
   x-frame-options: DENY
   content-security-policy(-report-only): … frame-ancestors 'none'
   ```
   Educates dashboard tabs render the target URL in an **iframe**, so the console tab would be
   blank/refused. Allowing the academy origin means editing the cluster's console CSP via
   `consoles.operator.openshift.io` — a **cluster-admin** change on the managed Airbus cluster,
   not something the tenant GitOps in this repo can do. (Same class as, but harder than, the
   editor self-signed-cert gotcha — that was a trust prompt; this is a hard refusal.)

## Why the namespace isn't usable "as the human"

Educates does **not** propagate the SSO/OpenShift user identity into the session. The session
identity **is** the per-session ServiceAccount (`dcst-dcs-backend-<id>` SA); the terminal's
`oc` and the Console both act as that SA. The learner is SSO-gated only at the **portal edge**
by oauth-proxy (see `HANDOVER-oauth-gating.md`) — that identity never reaches the cluster
session. To RBAC-grant the human on the session namespace you'd need their OpenShift username
available inside `spec.session.objects`, which Educates 3.7.2 does not expose. So even opening
the real OpenShift console in a separate browser tab (where they'd be their SSO self) wouldn't
show their session namespace — the human user has no RBAC there.

Net: for all practical purposes in Educates, **the human *is* the session SA**. The SA has
namespace `admin`, so the namespace is fully usable through the session's own terminal + Console.

## Options (need a platform decision — pick one)

| # | Option | Cost | Gives |
|---|--------|------|-------|
| A | **Keep as-is** (k8s Dashboard console, already enabled) | none | GUI CRUD in the namespace as the SA. Recommended default. |
| B | Switch `console.vendor: octant` | small, per-workshop | Richer k8s GUI; still not OpenShift-branded; octant is upstream-deprecated. |
| C | Cluster-admin edits console CSP `frame-ancestors` to allow the academy origin **+** an Educates feature/patch to propagate the SSO user + per-session RBAC | large, cluster-admin + upstream | The literal request. Out of tenant control; not worth it for ephemeral sessions. |
| D | Content link that opens the OpenShift console in a **new browser tab** (not embedded) | small | Learner sees the console as their SSO self — but **not** their session namespace (no RBAC). Confusing; not recommended. |

**Recommendation: Option A.** The Console tab already satisfies "choose the console over the
CLI." The OpenShift-branded console is a cluster-platform feature request, not a workshop change.
Teach the k8s Dashboard as "the visual console" in the environment guide; note it is the
Kubernetes web console, not the OpenShift console.
