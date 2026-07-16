# Course Topics

Topic inventory for the DCS Academy, organised by module. Topics are an inventory, not a 1:1 map to workshops — the mapping is in the `course-module-*.md` files.

> **Rework note (2026-07-16).** Modules A and B were restructured: Core (A) is now a lean quick-win path (deploy → configure/fix → expose → storage → terms → consoles) with theory folded into labs; the Developer track (B) pivots to build & platform integration (Docker→K8s, BuildConfigs, Dev Spaces, Harbor+scanning, RBAC/tenancy, DEV/PROD policies, scaling, operators). Topic **numbers are stable** (this is an inventory), but which module *teaches* a topic changed — see `course-module-a.md` / `course-module-b.md` for the authoritative mapping. The headings below group topics by their *original* module for continuity; annotations flag where a topic is now taught.

## Module A — Core / Fundamentals

1. **Containers & images** — what a container is, images, the OCI model (upstream). DCS framing: containers vs VMs, the Airbus OpenShift journey.
2. **Kubernetes essentials** — Pods, Deployments, Services, config/secrets (upstream). Aligns to the DCS "Kubernetes Fundamentals" 4-layer model.
3. **NaaS & namespace lifecycle** — Namespace as a Service; DEV vs PROD lifecycle, differences, promotion; shared vs dedicated clusters (DCS-specific). *Vocabulary in Core A06; the deep DEV/PROD policy model (PROD=Kyverno+Routes, DEV=loose+no-Routes) → lab B06.*
4. **DCS registry (Harbor)** — catalogs (DCS / Allowed External / Proxy-Cached), robot accounts, GitOps-managed repos, Helm charts, mirroring via ITSM, scan gates (DCS-specific). *→ lab B04.*
5. **Tenancy & access** — **Tenant → Namespaces** model (no separate "project" layer; project = namespace in OpenShift wording), onboarding, SSO login, RBAC basics, Network Policy isolation, quotas (Basic/Customized) + ITSM increase, egress IPs (DCS-specific). *Vocabulary + self-service/ITSM in Core A06/A07; deep RBAC/tenancy → lab B05.*
5b. **RBAC depth** — Roles vs ClusterRoles, RoleBindings vs ClusterRoleBindings, rules (apiGroups/resources/verbs), subject→binding→role trace; create a Role in-namespace. *→ lab B05.*
6. **Networking on DCS** — Service→Route→External Load Balancer (Route requires a PROD-type namespace), DNS naming, Network Policies (observe-only until tenant self-service lands), egress restrictions (DCS-specific). *→ Core A04 (expose properly: real Route + session tab).*
6b. **Storage on DCS** — PVC → StorageClass → PV; **File vs Block** via PVC (SC names variabilised); classification-driven SC choice; **S3 via ITSM ticket** (DCS-specific). *→ Core A05.*
6c. **Operators concept** — the OpenShift Operator pattern (controller + reconcile), CRD vs CR, OLM/OperatorHub; the **DCS ownership model** (platform owns the operator, tenant owns the instance). Prerequisite for Module F. *→ lab B08.*

## Module B — Developer

7. **Deploying an app** — from image to running workload on DCS *(now taught in Core A02, the quick win)*.
7b. **Docker → Kubernetes migration** — mapping docker/compose concepts to K8s objects; what doesn't translate on DCS (SCC, Harbor, no `latest`) (→ lab B01, Intermediate).
7c. **Building images with BuildConfigs** — git as a build source; S2I/Dockerfile builds on-cluster; output to Harbor (→ lab B02).
8. **Configuration & secrets** — externalising config, mounting secrets *(now taught in Core A03)*.
9. **Scaling, health & resources** — replicas, probes, requests/limits under quota (→ lab B07).
10. **Debugging & logs** — inspecting pods, logs, events, common failures *(now taught in Core A03)*.
11. **Stateful workloads / storage** — PVCs, storage classes on DCS *(now taught in Core A05)*.
11b. **Cloud development (OpenShift Dev Spaces)** — in-cluster, browser-based dev environments (Eclipse Che) on an air-gapped platform; devfiles; developing *on* DCS vs deploying to it (→ lab B03).

## Module C — Security & Compliance

12. **Image scanning & Harbor gates** — vulnerability vs compliance scanning, per-image/project/global scans, gate policies, reading reports, remediation.
13. **Pod security / SCC** — restricted policy, arbitrary UID, when baseline is needed.
14. **Secrets management** — good practice, avoiding secrets in images/logs.
15. **Supply chain & provenance** — catalogs, allowed external registries, mirroring via ITSM, trusted sources, air-gapped supply.
16. **Governance, data classification & residency** — Data Classification Matrix (multi-national, e.g. DE/ES), Responsibility Matrix (RACI), Security Exception Process, Terms & Conditions (image/registry policies), compliance workflows on DCS.

## Module D — Architect / Onboarding

17. **DCS service catalog & capabilities** — the DCS Services Overview (mission, service catalog, core capabilities, deployment locations); why Red Hat OpenShift (strategic rationale).
18. **Tenancy / landing-zone design** — structuring tenants/projects/namespaces, shared vs dedicated clusters, quotas, DEV/PROD environments.
19. **Costing & recharging** — resource tiers, shared vs dedicated cost model, capacity planning, the cost calculator.
20. **Reference architectures / golden paths** — recommended patterns for tenant apps.

## Module E — Observability

21. **Metrics & dashboards** — Prometheus/Thanos, Grafana for tenant apps.
22. **Logs** — accessing and querying application logs.
23. **Alerts** — defining and routing alerts for tenant apps.

## Module F — Operators / Platform Services

DCS offers these as **OpenShift operators, not aaS** — the platform owns the operator lifecycle; the **tenant owns the application instance** the operator manages (config, data, backups, upgrades, day-2). Foundations topic 6c (operator concept, lab A09) is the prerequisite.

24. **GitLab on DCS** — GitLab provided via the GitLab operator; provision/own a GitLab instance (source control/CI) in your tenant (DCS-specific).
25. **Argo CD / GitOps on DCS** — Argo CD via the OpenShift GitOps operator; own an Argo CD instance and its Applications; sync from an in-cluster Git source (DCS-specific).
26. **PostgreSQL on DCS (CloudNativePG)** — Postgres via the CloudNativePG operator; own a database `Cluster` instance, its storage and backups — not a managed DBaaS (DCS-specific).

## Notes on Topic Selection

- Topics 1–2 are the only pure-upstream fundamentals; keep them lean — most learners have some exposure. They anchor the Core quick win (A01/A02).
- **Rework:** the DCS-specific depth (topics 3, 4, 5, 5b, 6c) is no longer Core — Core teaches the *terms* (A06) and the *happy path* (deploy/expose/store), the Developer track teaches the *mechanisms* (B04 Harbor, B05 RBAC/tenancy, B06 DEV/PROD policies, B08 operators). Core keeps only topics 1, 2, 6, 6b + the vocabulary slices of 3/5, plus the two console tours (A07 ITSM, A08 OpenShift) and self-service/ITSM.
- Topic 12 (image scanning) is now taught in **Developer B04** (all scanning consolidated there per the 2026-07-16 decision); the built Security C01/C04 overlap and need reconciliation (see tasks.md).
- Topic 17 (service catalog) is conceptual — deliver as orientation on the Architect track's intro, not a standalone text workshop.
- Observability (20–22) reuses a deployed app; sequence it after Core A02 (or Developer).

### Future expansion ideas (deferred from v1)

- CI/CD & GitOps module — Tekton/OpenShift Pipelines, Argo CD, image promotion.
- Advanced networking — service mesh, network policies, multi-cluster.
- Stateful deep-dive — databases, backups, storage classes.
