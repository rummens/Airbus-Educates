# Workshop Plan: lab-a05-access-tenancy

## 1. Workshop Metadata

- **Name:** `lab-a05-access-tenancy`
- **Title:** Access & Tenancy
- **Description:** Learn how teams onboard to DCS — projects, RBAC, quotas, and SSO login — and how access is scoped to your tenant.
- **Duration:** 35m
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A01 (What is DCS?)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (view roles/quota visually)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: trio

## 3. Learning Objectives

- Explain the DCS three-level model: **Namespace → Project → Tenant**.
- Describe how a team becomes a DCS tenant (onboarding, SSO login).
- Inspect the RBAC that scopes what the learner can do in their project, and how **Network Policies** isolate tenants on a shared cluster.
- Read the resource quota (**Basic vs Customized**) on the project and explain its effect, incl. egress IPs.
- Explain that a quota increase is an **ITSM request**, and that access is confined to the tenant's own projects.

## 4. Connection to Previous Workshop

Builds on A01 orientation. A03 (namespaces) is complementary but not required. Learner knows `oc` basics. Focus on **who can do what** and **how much**, not on deploying.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/sample-role.yaml` — a Role/RoleBinding to inspect and (optionally) apply within the learner's project to see RBAC in action.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **tenancy & access** blurb + link `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access`.
- **`01-tenant-model.md`** — concept. The three levels: Kubernetes **Namespace** → OpenShift **Project** → **Tenant** (team). Onboarding + SSO login; multi-tenancy isolation on a shared cluster via RBAC + Network Policies. Inline blurb + DCS docs (`/tenancy/namespaces-projects-tenants`, placeholder). `oc whoami` recap.
- **`02-rbac.md`**
  - `oc auth can-i --list` → check: command returns the learner's permissions.
  - `oc auth can-i create deployments` → check: returns `yes` for own project.
  - `oc auth can-i get pods -n kube-system` (or another tenant's ns) → check: returns `no` (isolation demonstrated). Diagnose-style; hint explains why.
  - `oc get rolebindings` → check: bindings listed. [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) upstream link.
- **`03-quotas.md`**
  - `oc describe quota` → check: a ResourceQuota is present; assert a limit value. Explain **Basic vs Customized** default quotas and effect (ties to A02 scaling within budget); mention egress IPs are quota'd. [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) upstream.
  - `oc describe limitrange` → check: limit range present.
  - Concept: a **quota increase is an ITSM request** (`/quotas/limits-and-requests`, placeholder) — no live change in the workshop; model the process.
- **`99-workshop-summary.md`** — recap tenant/RBAC/quota. **Check Your Understanding** (3 Q): what a tenant is on DCS; how isolation is enforced; what a quota controls. Answers link DCS docs / upstream appropriately.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Mostly read-only `oc` commands scoped to the session project. The cross-namespace `can-i` check intentionally targets another namespace to prove isolation (expected `no`).

## 8. Design Notes

- Heavily read/observe — appropriate for a Foundations concept workshop; the "every command verified" rule is satisfied by asserting the observable state (permissions, quota) each command reveals.
- The isolation demonstration (`can-i ... -n other-ns` → `no`) is a memorable proof point; keep it.
- Relevant to all three tracks, especially Security (C) and Architect (D) — this is the tenancy grounding they extend.
- Confirm how DCS onboarding/SSO is actually described so the concept page matches reality (link to DCS docs).
