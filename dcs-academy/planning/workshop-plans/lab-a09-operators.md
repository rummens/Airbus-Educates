# Workshop Plan: lab-a09-operators

## 1. Workshop Metadata

- **Name:** `lab-a09-operators`
- **Title:** Operators on DCS
- **Description:** Understand the OpenShift Operator pattern and how DCS offers operators — the platform runs the operator, you own the instances (Custom Resources) it manages.
- **Duration:** 40m
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A02 (Kubernetes Essentials on DCS)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (OperatorHub / Installed Operators views)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: trio
- **Note:** operator install is cluster-scoped (platform team's job) — this lab **observes** an already-installed operator and creates a Custom Resource **instance** in the learner's namespace. No cluster-admin needed. Use a lightweight, Harbor-mirrorable operator for the hands-on instance (candidate: CloudNativePG, since it's also a Module F track — reuse its images).

## 3. Learning Objectives

- Explain the **Operator pattern**: a controller that encodes operational knowledge for an application, driving a **Custom Resource (CR)** toward its desired state (reconciliation loop).
- Describe **CRDs vs CRs**: an Operator installs CRDs (new resource *types*); you create CRs (*instances*).
- Explain **OLM** (Operator Lifecycle Manager) and **OperatorHub** at a high level, and how operators are installed once, cluster-wide.
- State the **DCS operator model clearly**: DCS provides the **OpenShift operators** (not managed/aaS), so **the platform installs & updates the operator, but the tenant owns and operates the application instance** the operator manages (backups, sizing, upgrades of the CR, day-2). This ownership split is the key takeaway.
- Create and inspect a CR instance, and watch the operator reconcile it.

## 4. Connection to Previous Workshop

A02 taught built-in resources (Deployment/Service). This lab introduces **Operators + Custom Resources** — the same declarative model, extended to whole applications. It is the conceptual foundation for **Module F (Platform Services / Operators)** where GitLab, Argo CD, and CloudNativePG are used in depth.

## 5. Exercise Files to Create

- `exercises/sample-cr.yaml` — a minimal Custom Resource for the chosen demo operator (e.g. a tiny CloudNativePG `Cluster`), image refs via `{{< param dcs_registry >}}`.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **operators on DCS** blurb + link `{{< param dcs_docs_base_url >}}/concepts/operators`.
- **`01-operator-pattern.md`** — concept. Controller + reconciliation loop; operators encode ops knowledge ("a human operator, automated"). Analogy (tapering): an Operator is like an experienced sysadmin-in-software for one app. **SVG diagram**: CR (desired) → Operator (controller) → managed workloads (actual), with the reconcile arrow. [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) upstream; OpenShift [Operators overview](https://docs.openshift.com/container-platform/latest/operators/understanding/olm-what-operators-are.html).
- **`02-crds-olm-operatorhub.md`** — concept. CRD (new type) vs CR (instance); OLM installs/updates operators; OperatorHub is the catalog. On DCS, OperatorHub is curated/air-gapped (mirrored operators only).
  - `oc get crds | grep <operator-group>` → check: the operator's CRDs are present (proof it's installed).
  - `oc api-resources | grep <kind>` → check: the CR kind is available.
  - `dashboard:open-dashboard` Console → **Installed Operators** view (observe; guide back to terminal after).
- **`03-create-an-instance.md`**
  - `editor:open-file` sample-cr.yaml; explain the spec fields (what you, the owner, control).
  - `oc apply -f sample-cr.yaml` → polling check: CR created and the operator has reconciled it (managed pods/statefulset ready).
  - `oc get <kind>` / `oc describe <kind> <name>` → check: status/conditions show healthy; point at the reconcile status.
- **`04-the-dcs-ownership-model.md`** — concept (the DCS-specific heart of the lab). DCS offers **operators, not aaS**: platform owns operator install/upgrade + CRD versions; **tenant owns the instance** — sizing, config, backups, CR-version upgrades, monitoring, incident response for the app. Contrast with a managed database/SaaS where the provider owns day-2. Map to the **Responsibility Matrix (RACI)**. DCS docs link. No new commands (recap `oc get <kind>` ownership boundary).
- **`99-workshop-summary.md`** — recap operator pattern, CRD vs CR, OLM/OperatorHub, and the ownership split. **Check Your Understanding** (3 Q): what an Operator reconciles; CRD vs CR; on DCS, who owns the app instance an operator manages. Answers link DCS docs / upstream. Point forward to Module F.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`; manifests by relative name, scoped to `$SESSION_NAMESPACE`. The CR is created in the learner's namespace; the operator itself runs cluster-wide (observe only).

## 8. Design Notes

- **Task 5 — "explain the OpenShift operator concept once, in the fundamentals":** this is that lab. Kept concept-first with one hands-on CR so the pattern is concrete without needing cluster-admin.
- **Prerequisite for Module F (Operators track).** Reuse the CloudNativePG operator/images here so Foundations and Module F share the mirror footprint.
- **Ownership model is the point** — err toward over-explaining the platform-owns-operator / tenant-owns-instance split; it's the recurring source of DCS support confusion and the reason Module F exists.
- Operator install is cluster-scoped and pre-done by the platform; the lab never installs an operator (air-gapped OperatorHub, no tenant cluster-admin). If no operator can be pre-installed in the test cluster, fall back to inspecting CRDs + annotated console screenshots for pages 02–03.
- Placement: after A02; can run any time in Foundations before Module F.
