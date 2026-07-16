# Workshop Plan: lab-b05-rbac-tenancy

## 1. Workshop Metadata

- **Name:** `lab-b05-rbac-tenancy`
- **Title:** RBAC, Tenancy & Namespaces
- **Description:** Go past the terms from Core — see the mechanism. The Tenant → Namespaces model in depth, the RBAC objects behind "can I?", tracing subject → binding → role → rule, and proving least privilege by creating a Role + RoleBinding of your own.
- **Duration:** 45m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** Module A (Core A06 gave the vocabulary)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view + edit RBAC manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (view roles/bindings/quota visually)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **vcluster decision:** `false` — session namespace. All RBAC work (create Role + RoleBinding, impersonate a ServiceAccount) stays inside the learner's own namespace; no cluster-scoped rights needed.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain the **Tenant → Namespaces** model in depth (org-level Tenant owns one or more Namespaces; no separate "project" layer — "project" is OpenShift's word for a namespace).
- Distinguish **Role vs ClusterRole** and **RoleBinding vs ClusterRoleBinding** (namespace-scoped vs cluster-scoped) and read a role's rules (apiGroups / resources / verbs).
- Trace an effective permission from **subject → binding → role → rule**.
- Create a Role + RoleBinding in their own namespace and prove least privilege with `oc auth can-i --as`.
- Read the namespace ResourceQuota and explain that an increase is an **ITSM request**.

## 4. Connection to Previous Workshop

**What the learner already knows** (from Module A, Core A06 — Terms: Namespaces & Tenancy):
- The *terms*: Namespace, Tenant, and that "project" is not a separate layer.
- That access is scoped to their tenant's namespaces — as a fact, not a mechanism.

**What is new in this workshop:**
- The *mechanism* behind those terms: the RBAC objects (Role/ClusterRole, bindings, rules) that actually enforce scoping.
- Reading and reasoning about RBAC, then authoring a Role + RoleBinding and proving its effect.
- Quotas as readable objects and the ITSM increase path.

**What should NOT be re-taught:**
- Do not re-define Namespace/Tenant vocabulary (A06 owns it) — reference it in one line.
- Do not re-teach `oc` orientation basics (`oc whoami`, `oc project`).

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the RBAC, Tenancy & Namespaces workshop."

### exercises/role-viewer.yaml
**Purpose:** The Role the learner inspects then applies on page 04.
**Initial contents:** A namespaced `Role` granting read-only verbs (`get`, `list`, `watch`) on a couple of resource types (e.g. `pods`, `configmaps`) — a clean least-privilege example.

### exercises/rolebinding-viewer.yaml
**Purpose:** Binds the Role to a ServiceAccount in the learner's namespace.
**Initial contents:** A `RoleBinding` referencing `role-viewer` and a subject `system:serviceaccount:$SESSION_NAMESPACE:<sa>`.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame the lab as "Core named these; now see how they actually work."
**Content outline:**
- `{{< param product_name >}}` framing + first-time note; pick up from A06 ("you know the words Tenant and Namespace — now let's open up who-can-do-what and why").
- What You'll Learn; 45m / intermediate. DCS-specific blurb + link `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access`. No actions.

### 01-tenant-to-namespaces.md
**Purpose:** The Tenant → Namespaces model in depth.
**Content outline:**
- Two levels only: **Tenant** (org-level — recharging, accountability) owns one or more **Namespaces** (DEV/PROD, etc.). Dispel the "project is a third layer" confusion explicitly.
- How isolation on a shared cluster is enforced — RBAC scopes *what*, and this is the lab's focus.
- `oc project` + `oc get namespace $(oc project -q) -o jsonpath='{.metadata.labels}'` (`terminal:execute`) → examiner check: current project reported and its tenant/type labels printed.
- DCS tenancy → `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access` + blurb.

### 02-can-i.md
**Purpose:** Start from the answer — "can I?" — before opening the objects.
**Content outline:**
- `oc auth can-i --list` (`terminal:execute`) → examiner check: the learner's permissions are listed.
- `oc auth can-i create deployments` → check: returns `yes` for own namespace.
- `oc auth can-i get pods -n kube-system` → check: returns `no` (isolation across namespaces; diagnose-style, hint explains why). Sets up "why?" for the next page.

### 03-the-objects-behind-the-answer.md
**Purpose:** Read the RBAC objects that produce the answer — subject → binding → role → rule.
**Content outline:**
- Role (namespaced) vs ClusterRole (cluster-wide, reusable); RoleBinding vs ClusterRoleBinding. Rules = apiGroups × resources × verbs. **SVG diagram**: subject → binding → role → rules.
- `oc describe clusterrole view` (`terminal:execute`) → check: read-only rule pattern shown.
- `oc get rolebindings -o wide` → check: bindings + subjects listed in the namespace.
- `oc describe rolebinding <name>` → check: subject → roleRef traced. Note user vs group vs ServiceAccount subjects.
- RBAC → [upstream](https://kubernetes.io/docs/reference/access-authn-authz/rbac/); OpenShift [default cluster roles](https://docs.openshift.com/container-platform/latest/authentication/using-rbac.html).

### 04-create-a-role-prove-least-privilege.md
**Purpose:** Author a Role + RoleBinding and prove its exact effect.
**Content outline:**
- `editor:open-file` `role-viewer.yaml`; explain the rules. `oc apply -f role-viewer.yaml` (`terminal:execute`) → check: Role created.
- `oc apply -f rolebinding-viewer.yaml` → check: RoleBinding created.
- `oc auth can-i get pods --as=system:serviceaccount:$SESSION_NAMESPACE:<sa>` → check: returns `yes` (granted verb).
- `oc auth can-i delete pods --as=...` → check: returns `no` (least privilege — the diagnose-style proof point; hint explains the rule granted only read verbs).

### 05-quotas-and-itsm.md
**Purpose:** Read the namespace budget and understand the increase path.
**Content outline:**
- `oc describe quota` (`terminal:execute`) → check: a ResourceQuota is present; assert a limit value. Explain **Basic vs Customized** defaults and effect (ties to B07 scaling within budget).
- `oc describe limitrange` → check: limit range present.
- Concept: a **quota increase is an ITSM request** — no live change here, model the process. `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access` (quotas) + [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) upstream.

### 99-workshop-summary.md
**Purpose:** Recap the mechanism and bridge forward.
**Content outline:**
- Recap: Tenant → Namespaces; the four RBAC object types; the subject → binding → role → rule trace; least privilege proven with `--as`; quotas + ITSM.
- **Check Your Understanding** (3 Q): Role vs ClusterRole; what a RoleBinding connects; how to test an effective permission for another subject.
- Bridge to **B06** (DEV vs PROD namespaces & policy posture — the *other* half of "what your namespace can do"), and note B05 is the prerequisite for **B08** (Operators), where ServiceAccount permissions matter.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes. Manifests referenced by relative name, scoped to `$SESSION_NAMESPACE`.
- Command patterns: read-only `oc auth can-i` / `oc describe` inspection; `oc apply -f <file>` for the Role + RoleBinding; `--as` impersonation stays within the learner's own namespace (no elevated rights). The cross-namespace `can-i -n kube-system` check intentionally returns `no` to prove isolation.

## 8. Design Notes

- **Consolidates old A05 (Access & Tenancy) + old A08 (RBAC Deep Dive)** into one Developer-track lab (course-module-b ideas 5, 5b). Core A06 now owns the vocabulary, so this lab drops the term-teaching and goes straight to the mechanism — the arc is deliberately "answer (`can-i`) → why (read the objects) → prove (author + `--as`)".
- **Tenant-facing scope only:** creating Roles/RoleBindings *within your own namespace* is in-tenant; ClusterRoles/ClusterRoleBindings are read-only observe (tenants don't self-manage cluster-scoped RBAC on DCS).
- Session namespace, not vcluster — no cluster-scoped work is needed and impersonation is same-namespace.
- Prerequisite mindset for **B08** (Operators, ServiceAccount permissions) and feeds the Security (C) and Architect (D) tracks.
