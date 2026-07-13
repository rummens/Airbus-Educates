# Workshop Plan: lab-c05-data-residency

## 1. Workshop Metadata

- **Name:** `lab-c05-data-residency`
- **Title:** EU Data-Residency & Compliance
- **Description:** Understand DCS data-classification and multi-national residency guarantees, see how workload placement is expressed, and walk the governance workflows a tenant is responsible for.
- **Duration:** 35m
- **Difficulty:** intermediate
- **Type:** Elective (Module C — Security & Compliance)
- **Prerequisites:** Module A (esp. A05 tenancy/quotas). Mostly conceptual + observe.
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- Console: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Run location: **native OpenShift session namespace** (vcluster `enabled: false`). Read/observe only. `budget: medium`.
- Workshop image: **`dcs-workshop-base`** — `oc` + `jq`/`yq`.
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.
- Governance artefacts are **fixtures** in `exercises/` (classification matrix, a classified workload manifest) — real residency labels on cluster nodes aren't guaranteed in the test env, so observe-steps read fixtures + best-effort `oc get nodes`. Rationale in Design Notes.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain the DCS **Data Classification** scheme and multi-national (e.g. Germany/Spain) **data-residency** guarantees.
- Describe how workload **placement** is expressed (region/zone labels + `nodeSelector`/affinity) and inspect it.
- Read the **Responsibility Matrix (RACI)** to tell platform duties from tenant duties.
- Describe the **Security Exception Process** and the **Terms & Conditions** governing data/registry use.
- Identify the compliance workflows a tenant follows (classification tagging, exception requests via ITSM).

## 4. Connection to Previous Workshop

Elective — assumes Module A (tenancy). **Already known:** namespaces, tenant model, ITSM as the self-service channel, `oc get`/`jsonpath`. **New here:** data classification, residency, placement labels, RACI split, exception process, T&Cs. **Do NOT re-teach:** the Tenant→Namespaces model (reference from A05) — and never introduce a "project" layer.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/data-classification-matrix.md` — a sample DCS classification matrix (levels, examples, allowed regions per level) for the learner to read.
- `exercises/workload-classified.yaml` — a Deployment (`$DCS_REGISTRY/samples/hello-dcs:1.0`) carrying a `data.dcs/classification` label/annotation and a `nodeSelector` pinning it to a region (e.g. `topology.kubernetes.io/region: eu-de`). Read with `yq`; not required to schedule (region nodes may be absent).
- `exercises/raci.md` — a sample Responsibility Matrix (platform vs tenant rows) for the read step.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — overview + first-time note. DCS blurb: **Governance & compliance** (classification, RACI, exceptions, T&Cs) → `{{< param dcs_docs_base_url >}}/governance/overview`; standard [labels/selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) + [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) → upstream.
- **`01-data-classification-and-residency.md`** — concept.
  - `editor:open-file` `data-classification-matrix.md`; `terminal:execute` `grep -c '|' data-classification-matrix.md` *(or `yq`/`jq` if structured)* → examiner `verify-matrix-present` (fixture readable / rows found). Explain classification levels and multi-national residency (data for a classification must stay in permitted region(s)); air-gap + on-prem underpins the guarantee.
- **`02-where-your-workload-runs.md`** —
  - `editor:open-file` `workload-classified.yaml`; explain the classification annotation + region `nodeSelector`.
  - `terminal:execute` `yq '.spec.template.metadata.annotations, .spec.template.spec.nodeSelector' workload-classified.yaml` → examiner `verify-placement-expressed` (annotation + nodeSelector printed). Explain placement is *expressed in the spec* and enforced by the scheduler + platform policy.
  - `terminal:execute` `oc get nodes -o jsonpath='{range .items[*]}{.metadata.labels.topology\.kubernetes\.io/region}{"\n"}{end}' | sort -u` → examiner `verify-node-topology` (command returns node topology info; tolerant of empty region on test clusters via diagnostic hint). Observe how the platform advertises regions. `{{< note >}}` residency is a platform guarantee, not something the tenant edits directly.
- **`03-responsibility-and-exceptions.md`** — concept + read.
  - `editor:open-file` `raci.md`; `terminal:execute` `grep -i 'tenant' raci.md` → examiner `verify-raci-tenant-rows` (tenant-owned rows found). Explain the **RACI** split (platform owns residency/infra controls; tenant owns classifying + tagging data and requesting exceptions).
  - **Security Exception Process** + **T&Cs** — blurbs + DCS docs (`/governance/overview`). When a workload can't meet a control, the exception is a governed ITSM request, time-boxed and approved — not a config toggle.
- **`04-compliance-workflow.md`** — concept.
  - The tenant compliance loop: classify data → tag the workload → place it in permitted region → request an exception via **ITSM** if needed → renew/close. Ties classification (p01), placement (p02), and RACI/exceptions (p03) together. ITSM blurb → `{{< param dcs_docs_base_url >}}/support/itsm-requests`. *(Concept page; the summary examiner covers the knowledge check.)*
- **`98-your-feedback.md`** — standard (workshop=lab-c05-data-residency).
- **`99-workshop-summary.md`** — recap; **Check Your Understanding** (3 Q): what data classification + residency guarantee; how placement is expressed and who enforces it; what the exception process is for and who owns it. Final examiner (`verify-placement-expressed`-style) as the knowledge-check action.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. `oc`/`yq`/`grep` on fixtures + read-only cluster queries — no `cd`.

## 8. Design Notes

- **Observe/concept-heavy by design** (module plan: "mostly conceptual + observe"). Governance artefacts are fixtures so every page still has an examiner-verifiable step air-gapped, even though residency is a platform guarantee the tenant can't mutate.
- **No new image; no scheduling dependency:** `workload-classified.yaml` is *read* with `yq`, not required to schedule onto a region node (test clusters may lack region labels — the node-topology check is tolerant + diagnostic). Task in `tasks.md`: tighten `verify-node-topology` once the target cluster exposes region labels.
- Closes the Security track: C01–C04 harden the image/runtime/supply chain; **C05 places it in the EU governance + residency frame**. Governance thread connects back to C02's exception concept.
- Never introduce a "project" layer (see [[dcs-domain-corrections]]): Tenant → Namespaces only.
