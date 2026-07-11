# Workshop Plan: lab-a08-rbac-deep-dive

## 1. Workshop Metadata

- **Name:** `lab-a08-rbac-deep-dive`
- **Title:** RBAC Deep Dive
- **Description:** Go beyond "can I?" — understand Roles, ClusterRoles, and their bindings, and how DCS composes them to scope what your tenant can do.
- **Duration:** 45m
- **Difficulty:** intermediate
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A05 (Access & Tenancy)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (view roles/bindings visually)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: trio

## 3. Learning Objectives

- Distinguish **Role** vs **ClusterRole**, and **RoleBinding** vs **ClusterRoleBinding** — namespace-scoped vs cluster-scoped.
- Read a Role/ClusterRole's rules (apiGroups / resources / verbs) and predict what it allows.
- Trace an effective permission from a **subject** (user/group/ServiceAccount) → binding → role → rule.
- Explain how DCS composes RBAC to scope a tenant to its own namespaces (built on A05's isolation proof).
- Create a Role + RoleBinding within your own namespace and prove it takes effect (`oc auth can-i`).

## 4. Connection to Previous Workshop

A05 answered "what can I do?" (`oc auth can-i`, isolation across namespaces). This lab answers **"why, and how is that wired?"** — the objects behind the answer. Reuses the A05 tenant framing; do not re-teach the tenant model.

## 5. Exercise Files to Create

- `exercises/role-viewer.yaml` — a namespace `Role` granting read-only on a couple of resource types.
- `exercises/rolebinding-viewer.yaml` — a `RoleBinding` binding the role to a ServiceAccount in the learner's namespace.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **RBAC on DCS** blurb + link `{{< param dcs_docs_base_url >}}/concepts/rbac`.
- **`01-roles-vs-clusterroles.md`** — concept. Role (namespaced) vs ClusterRole (cluster-wide, reusable); rules = apiGroups × resources × verbs. **SVG diagram**: subject → binding → role → rules (structural concept → page bundle). [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) upstream; OpenShift [default cluster roles](https://docs.openshift.com/container-platform/latest/authentication/using-rbac.html).
  - `oc get clusterroles | head` → check: cluster roles listed.
  - `oc describe clusterrole view` → check: rules shown (read-only pattern).
- **`02-bindings-and-subjects.md`**
  - `oc get rolebindings -o wide` → check: bindings + subjects listed in the namespace.
  - `oc describe rolebinding <name>` → check: subject → roleRef traced. Explain user vs group vs ServiceAccount subjects.
- **`03-create-a-role.md`**
  - `editor:open-file` role-viewer.yaml; `oc apply -f role-viewer.yaml` → check: Role created.
  - `oc apply -f rolebinding-viewer.yaml` → check: RoleBinding created.
  - `oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:<sa>` → check: returns `yes` for granted verb.
  - `oc auth can-i delete pods --as=...` → check: returns `no` (least privilege demonstrated). Diagnose-style + hint.
- **`99-workshop-summary.md`** — recap the four object types and the subject→binding→role→rule trace. **Challenge**: grant the ServiceAccount one additional verb via an edited Role and prove it (examiner-validated + hint + reveal). **Check Your Understanding** (3 Q): Role vs ClusterRole; what a RoleBinding connects; how to test an effective permission.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Manifests by relative name, scoped to `$SESSION_NAMESPACE`. `--as` impersonation stays within the learner's own namespace so no elevated rights are needed.

## 8. Design Notes

- **Split out of A05 on author's request** (review comment): A05 keeps RBAC at "inspect + prove isolation"; the object-level depth lives here so A05 stays ~35m.
- Tenant-facing scope only: creating Roles/RoleBindings **within your own namespace** is in-tenant; ClusterRoles/ClusterRoleBindings are **read-only observe** (tenants don't self-manage cluster-scoped RBAC on DCS).
- Feeds the Security (C) and Architect (D) tracks, and is a prerequisite mindset for the Operators track (Module F) where ServiceAccount permissions matter.
- Placement: after A05; can be positioned as the last "spine" lab or an optional-but-recommended Foundations lab depending on audience depth.
