# Workshop Plan: lab-b08-operators

## 1. Workshop Metadata

- **Name:** `lab-b08-operators`
- **Title:** Operators on DCS
- **Description:** Understand the OpenShift Operator pattern — a controller that reconciles a Custom Resource toward its desired state — and the DCS ownership split: the platform runs the operator, you own the instance it manages.
- **Duration:** 40m
- **Difficulty:** advanced
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B05 (RBAC, Tenancy & Namespaces)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view + apply a CR)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (OperatorHub / Installed Operators views)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: the trio.
- **vcluster decision:** `false` — session namespace. Operator install is cluster-scoped (platform team's job); this lab **observes** an already-installed operator and creates a CR **instance** in the learner's own namespace. No cluster-admin needed.
- **Operator:** reuse **CloudNativePG** (also a Module F track) so Foundations/Developer/Module F share the mirror footprint; images via `{{< param dcs_registry >}}`.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain the **Operator pattern**: a controller that encodes operational knowledge and drives a **Custom Resource (CR)** toward its desired state (reconciliation loop).
- Distinguish **CRD vs CR**: an operator installs CRDs (new resource *types*); you create CRs (*instances*).
- Explain **OLM / OperatorHub** at a high level and that operators are installed once, cluster-wide (curated/air-gapped on DCS).
- State the **DCS ownership model**: the platform installs and updates the operator; the tenant owns and operates the application instance (sizing, config, backups, day-2).
- Create a CR, watch the operator reconcile it, and inspect its status.

## 4. Connection to Previous Workshop

**What the learner already knows** (from B05: RBAC, Tenancy & Namespaces, and Module A Core):
- Built-in resources (Deployment/Service) and the declarative apply/inspect loop.
- RBAC and ServiceAccounts — relevant because an operator-managed instance runs with permissions in the learner's namespace.
- The Tenant → Namespaces ownership boundary (B05) — this lab extends it to "who owns the operator vs the instance."

**What is new in this workshop:**
- Operators + Custom Resources — the same declarative model, extended to whole applications.
- The reconciliation loop as a live thing you watch.
- The DCS platform-owns-operator / tenant-owns-instance split.

**What should NOT be re-taught:**
- Do not re-teach Deployment/Service mechanics (Core A02) — contrast built-in resources with CRs in one line.
- Do not re-teach RBAC (B05) — reference it where ServiceAccount permissions matter.

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the Operators on DCS workshop."

### exercises/sample-cr.yaml
**Purpose:** The minimal Custom Resource the learner applies (page 03).
**Initial contents:** A tiny CloudNativePG `Cluster` CR (single instance, smallest storage), image refs via `${DCS_REGISTRY}` so the operator pulls from Harbor.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame the capstone.
**Content outline:**
- `{{< param product_name >}}` framing + first-time note; position as the Developer-track capstone and the gateway to Module F. What You'll Learn; 40m / advanced. DCS-specific blurb + link `{{< param dcs_docs_base_url >}}/concepts/operators`. No actions.

### 01-operator-pattern.md
**Purpose:** The concept — controller + reconciliation.
**Content outline:**
- Controller + reconciliation loop; operators encode ops knowledge ("a human operator, automated"). Analogy (tapering, advanced audience — keep it brief): an operator is an experienced sysadmin-in-software for one app. **SVG diagram**: CR (desired) → Operator (controller) → managed workloads (actual), with the reconcile arrow.
- [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) upstream; OpenShift [Operators overview](https://docs.openshift.com/container-platform/latest/operators/understanding/olm-what-operators-are.html). No commands.

### 02-crds-olm-operatorhub.md
**Purpose:** CRD vs CR, and how operators get installed.
**Content outline:**
- CRD (new type) vs CR (instance); OLM installs/updates operators; OperatorHub is the catalog — on DCS it's curated/air-gapped (mirrored operators only).
- `oc get crds | grep <operator-group>` (`terminal:execute`) → check: the operator's CRDs are present (proof it's installed).
- `oc api-resources | grep <kind>` → check: the CR kind is available.
- `dashboard:open-dashboard` Console → **Installed Operators** view (observe; guide back to terminal after).

### 03-create-an-instance.md
**Purpose:** Apply a CR and watch reconciliation.
**Content outline:**
- `editor:open-file` `sample-cr.yaml`; explain the spec fields (what you, the owner, control).
- `envsubst < sample-cr.yaml | oc apply -f -` (image refs use `${DCS_REGISTRY}` — never plain `oc apply`) → polling check: CR created and the operator has reconciled it (managed Pods/StatefulSet ready).
- `oc get <kind>` / `oc describe <kind> <name>` → check: status/conditions show healthy; point at the reconcile status.

### 04-the-dcs-ownership-model.md
**Purpose:** The DCS-specific heart of the lab.
**Content outline:**
- DCS offers **operators, not aaS**: platform owns operator install/upgrade + CRD versions; **tenant owns the instance** — sizing, config, backups, CR-version upgrades, monitoring, incident response for the app. Contrast with a managed database/SaaS where the provider owns day-2. Map to the Responsibility Matrix (RACI). DCS docs link `{{< param dcs_docs_base_url >}}/concepts/operators`. No new commands (recap the `oc get <kind>` ownership boundary).

### 99-workshop-summary.md
**Purpose:** Recap and hand off to Module F.
**Content outline:**
- Recap the operator pattern, CRD vs CR, OLM/OperatorHub, and the ownership split.
- **Check Your Understanding** (3 Q): what an operator reconciles; CRD vs CR; on DCS, who owns the app instance an operator manages.
- Bridge: this lab is the conceptual prerequisite for **Module F** (Operators / Platform Services — GitLab, Argo CD, CloudNativePG), where these operators are used in depth.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes. Manifests by relative name, scoped to `$SESSION_NAMESPACE`. The CR is created in the learner's namespace; the operator itself runs cluster-wide (observe only).
- Command patterns: `oc get crds` / `oc api-resources` inspection; `envsubst < sample-cr.yaml | oc apply -f -` for the CR (image refs); `oc get`/`oc describe <kind>` for reconcile status; split-terminal `watch oc get pods` on `execute-2` while the operator provisions.

## 8. Design Notes

- **Renumbered from old A09 (Operators on DCS) → B08**; retyped from beginner Core lab to the **Advanced capstone** of the Developer track (course-module-b idea 6c). Prereq is now **B05** (RBAC) since ServiceAccount permissions matter for operator-managed instances.
- **Ownership model is the point** — err toward over-explaining the platform-owns-operator / tenant-owns-instance split; it's the recurring source of DCS support confusion and the reason Module F exists.
- **Prerequisite for Module F.** Reuse the CloudNativePG operator/images here so Foundations/Developer and Module F share the mirror footprint.
- Operator install is cluster-scoped and pre-done by the platform; the lab never installs an operator (air-gapped OperatorHub, no tenant cluster-admin). **If no operator can be pre-installed in the test cluster, fall back** to inspecting CRDs + annotated console **screenshots** for pages 02–03.
- **Carry-forward bug:** the CR (`sample-cr.yaml`) has `${DCS_REGISTRY}` image refs — apply with `envsubst < f.yaml | oc apply -f -`, never plain `oc apply`.
