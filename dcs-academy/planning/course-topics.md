# Course Topics

Topic inventory for the DCS Academy, organised by module. Topics are an inventory, not a 1:1 map to workshops — the mapping is in the `course-module-*.md` files.

## Module A — Foundations

1. **Containers & images** — what a container is, images, the OCI model (upstream). DCS framing: containers vs VMs, the Airbus OpenShift journey.
2. **Kubernetes essentials** — Pods, Deployments, Services, config/secrets (upstream). Aligns to the DCS "Kubernetes Fundamentals" 4-layer model.
3. **NaaS & namespace lifecycle** — Namespace as a Service; DEV vs PROD lifecycle, differences, promotion; shared vs dedicated clusters (DCS-specific).
4. **DCS registry (Harbor)** — catalogs (DCS / Allowed External / Proxy-Cached), robot accounts, GitOps-managed repos, Helm charts, mirroring via ITSM, scan gates (DCS-specific).
5. **Tenancy & access** — **Tenant → Namespaces** model (no separate "project" layer; project = namespace in OpenShift wording), onboarding, SSO login, RBAC basics, Network Policy isolation, quotas (Basic/Customized) + ITSM increase, egress IPs (DCS-specific).
5b. **RBAC depth** — Roles vs ClusterRoles, RoleBindings vs ClusterRoleBindings, rules (apiGroups/resources/verbs), subject→binding→role trace; create a Role in-namespace (split out of topic 5 → lab A08).
6. **Networking on DCS** — Service→Route→External Load Balancer (Route requires a PROD-type namespace), DNS naming, Network Policies (observe-only until tenant self-service lands), egress restrictions (DCS-specific).
6b. **Storage on DCS** — PVC → StorageClass → PV; **File vs Block** via PVC (SC names variabilised); classification-driven SC choice; **S3 via ITSM ticket** (DCS-specific → lab A07).
6c. **Operators concept** — the OpenShift Operator pattern (controller + reconcile), CRD vs CR, OLM/OperatorHub; the **DCS ownership model** (platform owns the operator, tenant owns the instance). Prerequisite for Module F (→ lab A09).

## Module B — Developer

7. **Deploying an app** — from image to running workload on DCS.
8. **Configuration & secrets** — externalising config, mounting secrets.
9. **Scaling, health & resources** — replicas, probes, requests/limits under quota.
10. **Debugging & logs** — inspecting pods, logs, events, common failures.
11. **Stateful workloads / storage** *(optional)* — PVCs, storage classes on DCS.
11b. **Cloud development (OpenShift Dev Spaces)** — in-cluster, browser-based dev environments (Eclipse Che) on an air-gapped platform; devfiles; developing *on* DCS vs deploying to it (→ lab B06).

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

- Topics 1–2 are the only pure-upstream fundamentals; keep them lean — most learners have some exposure.
- Topics 3–6 are the DCS-specific spine; they anchor the whole academy and are prerequisites for every track.
- Topic 17 (service catalog) is conceptual — deliver as orientation on the Architect track's intro, not a standalone text workshop.
- Observability (20–22) reuses a deployed app; sequence it after Developer B01.

### Future expansion ideas (deferred from v1)

- CI/CD & GitOps module — Tekton/OpenShift Pipelines, Argo CD, image promotion.
- Advanced networking — service mesh, network policies, multi-cluster.
- Stateful deep-dive — databases, backups, storage classes.
