# Module F — Operators / Platform Services (Elective)

For tenants who consume the **operator-provided platform services** DCS offers. DCS provides these as **OpenShift operators, not managed/aaS** — so the platform installs and upgrades the *operator*, but **the tenant owns and operates the application instance** (sizing, config, backups, CR upgrades, monitoring, incident response). This module makes that ownership split concrete, one service at a time.

The currently offered operators (v1 of this module): **GitLab**, **Argo CD**, **CloudNativePG**. Each workshop is independent — take the one(s) for the service you use.

## Workshop Structure Conventions

Same conventions as [course-module-a.md](course-module-a.md). Names: `lab-f0N-name`. All follow the house standards (intro page, `oc`, hybrid doc links, param trio, air-gapped Harbor images, examiner + knowledge check).

**Prerequisite for the whole module:** A09 (Operators on DCS) — the operator pattern, CRD vs CR, and the platform-owns-operator / tenant-owns-instance model. Each workshop assumes the operator is **already installed by the platform team**; the learner creates and operates an **instance** (Custom Resource) in their own namespace.

**Air-gapped note:** every operator's operand images (the workloads the operator spins up) must be **Harbor-mirrored** via `{{< param dcs_registry >}}`. Operator install (OLM subscription) is out of tenant scope — labs observe the installed operator and manage instances only.

**Cross-cutting theme — ownership / day-2:** every workshop ends by mapping the service to the **Responsibility Matrix (RACI)**: what DCS owns (operator lifecycle, CRD versions, platform patching) vs what the tenant owns (the instance and its data). This is the reason the module exists.

---

### Workshop F01: GitLab on DCS

**Directory name:** `lab-f01-gitlab`
**Covers ideas:** 24
**Type:** Elective (Operators)
**Prerequisites:** A09
**Learning objectives:** Explain that DCS provides GitLab via the **GitLab operator** (you own the instance, not a hosted SaaS); provision/inspect a GitLab instance CR in your namespace; understand what you own (config, backups, upgrades of the instance) vs what the platform owns (the operator).
**Narrative arc:** "I need source control / CI on DCS" → DCS offers the GitLab *operator*, not gitlab.com → inspect/create the GitLab CR → reach the GitLab UI (session dashboard tab) → understand your day-2 responsibilities.
**Code exercises:** Inspect the GitLab CRDs; apply a minimal GitLab instance CR (or inspect a pre-provisioned one); check reconcile/health; open the GitLab UI tab.
**Key code examples:** A GitLab operator Custom Resource with operand images via `{{< param dcs_registry >}}`. DCS-specific: `/services/gitlab`; [GitLab Operator](https://docs.gitlab.com/operator/) upstream.
**Design notes:** GitLab is heavy — prefer a **pre-provisioned instance the learner inspects and configures**, rather than a full live install per session (resource + time). Emphasise: tenant owns runners, backups, and instance upgrades.

### Workshop F02: GitOps with Argo CD on DCS

**Directory name:** `lab-f02-argocd`
**Covers ideas:** 25
**Type:** Elective (Operators)
**Prerequisites:** A09 (B01 helpful — you deploy an app via GitOps)
**Learning objectives:** Explain that DCS provides Argo CD via the **OpenShift GitOps / Argo CD operator** (tenant owns the Argo CD instance and its Applications); create an Argo CD instance CR scoped to your namespace; define an `Application` that syncs a manifest from a Git source to your namespace; understand ownership of the GitOps control loop.
**Narrative arc:** "How do I do GitOps on DCS?" → DCS gives you the Argo CD operator → create your Argo CD instance → point an `Application` at a repo (the tenant's GitLab from F01, or a sample) → watch it sync → own the instance.
**Code exercises:** Inspect the Argo CD CRDs; apply an `ArgoCD` instance CR; apply an `Application`; trigger/observe a sync; open the Argo CD UI tab.
**Key code examples:** `ArgoCD` CR + `Application` CR; images via `{{< param dcs_registry >}}`; Git source air-gapped/in-cluster. DCS-specific: `/services/argocd`; [OpenShift GitOps](https://docs.openshift.com/gitops/latest/) / [Argo CD](https://argo-cd.readthedocs.io/) upstream.
**Design notes:** Keep the synced app tiny (reuse `hello-dcs`). Air-gapped: the Git source is the in-cluster GitLab or a pre-seeded repo, not github.com. Emphasise: tenant owns the Argo CD instance, its RBAC, and the Applications.

### Workshop F03: PostgreSQL with CloudNativePG on DCS

**Directory name:** `lab-f03-cloudnative-pg`
**Covers ideas:** 26
**Type:** Elective (Operators)
**Prerequisites:** A09 (A07 storage helpful — a database needs a PVC)
**Learning objectives:** Explain that DCS provides PostgreSQL via the **CloudNativePG operator** (tenant owns the database cluster instance, its data, and backups — not a managed DBaaS); create a `Cluster` CR; connect to the database; understand HA/backup responsibilities that are **yours**.
**Narrative arc:** "I need a database on DCS" → not a managed DBaaS — DCS gives you the CloudNativePG *operator* → create a `Cluster` CR (with a storage class from A07) → connect and write data → understand that backups/HA/upgrades of *this* database are the tenant's job.
**Code exercises:** Inspect the CNPG CRDs; apply a small `Cluster` CR (storage via `{{< param dcs_sc_block >}}`/`{{< param dcs_sc_file >}}`); wait for the cluster to be ready; connect with `psql` and write/read a row; inspect a backup config (concept).
**Key code examples:** A CloudNativePG `Cluster` CR with operand images via `{{< param dcs_registry >}}` and a variabilised storage class. DCS-specific: `/services/postgresql`; [CloudNativePG](https://cloudnative-pg.io/docs/) upstream.
**Design notes:** CNPG is the lightest of the three → best candidate for a **fully live hands-on** (and it's reused as the demo operator in A09). Emphasise the DBaaS-vs-operator ownership contrast hardest here — it's the most common expectation mismatch.

## Notes

- **Why this module exists:** customers sometimes expect "aaS" (provider owns day-2). DCS offers the **operators**, so the tenant owns the app instance the operator manages. Every workshop reinforces that split explicitly (RACI mapping in each summary).
- **Ownership deep-dive** is established once in A09 (Foundations) and applied per-service here — don't re-teach the operator pattern, apply it.
- **Air-gapped:** all operand images Harbor-mirrored; operator install is platform-side (OLM), not in tenant scope.

## Future Expansion Ideas

- Additional operators as DCS's catalog grows (add a `lab-f0N-<service>` per operator).
- A capstone tying F01→F02→F03: source in GitLab → GitOps deploy via Argo CD → app backed by a CloudNativePG database.
- Day-2 operations deep-dive per operator (backup/restore drills, version upgrades) once the basics land.
