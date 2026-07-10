# Workshop Plan: lab-a03-namespace-model

## 1. Workshop Metadata

- **Name:** `lab-a03-namespace-model`
- **Title:** Namespaces & the Prod/Dev Model
- **Description:** Understand the DCS dev and prod namespace types, see them side by side, and learn how workloads move from dev to prod.
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
- **Virtual cluster: enabled** (`spec.session.applications.vcluster.enabled: true`) — gives the learner cluster-scoped rights to create/inspect multiple namespaces, so the dev/prod model is tangible. vcluster component images must be Harbor-mirrored (see air-gapped-images-reference).
- Web console: enabled
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Sample image: reuse `{{< param dcs_registry >}}/samples/hello-dcs:1.0`

## 3. Learning Objectives

- Explain **Namespace as a Service (NaaS)** — namespaces as the DCS consumption unit.
- Distinguish the **DEV** and **PROD** namespace lifecycle types and their differing controls.
- Deploy a workload into a DEV namespace.
- Inspect the constraints that differ in a PROD namespace (incl. that PROD cannot use the Proxy-Cached Catalog).
- Explain promotion (DEV → PROD) at a conceptual level.

## 4. Connection to Previous Workshop

A02 taught Deployments/Services and `oc` inspection. Learner can deploy a workload. This workshop reuses the same `hello-dcs` workload but focuses on **where** it runs and the DCS namespace-type distinction — do not re-teach Deployment mechanics.

## 5. Exercise Files to Create

- `exercises/dev-namespace.yaml` — a Namespace (or DCS namespace request object) labelled as dev type.
- `exercises/prod-namespace.yaml` — a Namespace labelled as prod type (stricter).
- `exercises/hello-dcs.yaml` — combined Deployment+Service (from A02) to deploy into each.
- `exercises/README.md` — placeholder.

*(Customer docs confirm a DEV/PROD namespace **lifecycle** with a documented quick-comparison, but the technical mechanism (labels vs CRD vs request objects) is not in the shared docs — P2 to confirm. Plan assumes labels on Namespaces created in the vcluster, plus a representative PROD policy incl. no Proxy-Cached Catalog access.)*

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific framing: **NaaS / DEV-PROD lifecycle** blurb + link `{{< param dcs_docs_base_url >}}/naas/dev-prod-lifecycle` (placeholder path).
- **`01-naas-and-namespace-types.md`** — concept. NaaS (namespaces as the unit); DEV vs PROD lifecycle: what differs (policy, change control, quotas, catalog access, promotion). Include a **quick-comparison DEV vs PROD** table (mirrors the customer docs). Inline blurb + DCS docs link. `Namespace` construct → [upstream](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/); OpenShift [Project](https://docs.openshift.com/container-platform/latest/rest_api/project_apis/project-project-openshift-io-v1.html) upstream.
  - `oc get namespaces` (in vcluster) → check: command succeeds.
- **`02-deploy-to-dev.md`**
  - `oc apply -f dev-namespace.yaml` → check: dev namespace exists with the dev-type label.
  - `oc apply -n <dev-ns> -f hello-dcs.yaml` → polling check: workload ready in dev namespace.
- **`03-prod-differences.md`**
  - `oc apply -f prod-namespace.yaml` → check: prod namespace exists with prod-type label.
  - Attempt the same deploy into prod / inspect stricter controls → check asserts the expected prod constraint (e.g. a policy that blocks or requires more). Diagnose-style; include hint.
  - Concept: promotion dev → prod (no live promotion tooling in Foundations; conceptual + docs link).
- **`99-workshop-summary.md`** — recap. **Check Your Understanding** (3 Q): which type enforces change control; why two types exist; how work moves dev→prod. Answers link DCS docs.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Commands explicitly `-n <namespace>` because the learner works across two namespaces here (not just the default project). Track which namespace each step targets.

## 8. Design Notes

- **Only Foundations workshop needing vcluster** — it is the cheapest way to give a learner two real namespaces with differing policy. Confirm vcluster sizing/availability on DCS (task in tasks.md).
- The prod-constraint demonstration depends on how DCS actually differentiates prod namespaces — flagged P1. Until confirmed, model it with a representative policy so the learning point (prod is stricter, promote don't edit) lands.
- Reuses the A02 sample app to avoid new images.
- Anchors the DCS mental model that A05 (tenancy) and the Developer track build on.
