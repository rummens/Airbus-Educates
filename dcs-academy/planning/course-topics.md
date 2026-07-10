# Course Topics

Topic inventory for the DCS Academy, organised by module. Topics are an inventory, not a 1:1 map to workshops — the mapping is in the `course-module-*.md` files.

## Module A — Foundations

1. **Containers & images** — what a container is, images, the OCI model (upstream). DCS framing: containers vs VMs, the Airbus OpenShift journey.
2. **Kubernetes essentials** — Pods, Deployments, Services, config/secrets (upstream). Aligns to the DCS "Kubernetes Fundamentals" 4-layer model.
3. **NaaS & namespace lifecycle** — Namespace as a Service; DEV vs PROD lifecycle, differences, promotion; shared vs dedicated clusters (DCS-specific).
4. **DCS registry (Harbor)** — catalogs (DCS / Allowed External / Proxy-Cached), robot accounts, GitOps-managed repos, Helm charts, mirroring via ITSM, scan gates (DCS-specific).
5. **Tenancy & access** — Namespace→Project→Tenant model, onboarding, SSO login, RBAC, Network Policy isolation, quotas (Basic/Customized) + ITSM increase, egress IPs (DCS-specific).
6. **Networking on DCS** — Service→Route→External Load Balancer, DNS naming, Network Policies, egress restrictions (DCS-specific).

## Module B — Developer

7. **Deploying an app** — from image to running workload on DCS.
8. **Configuration & secrets** — externalising config, mounting secrets.
9. **Scaling, health & resources** — replicas, probes, requests/limits under quota.
10. **Debugging & logs** — inspecting pods, logs, events, common failures.
11. **Stateful workloads / storage** *(optional)* — PVCs, storage classes on DCS.

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

## Notes on Topic Selection

- Topics 1–2 are the only pure-upstream fundamentals; keep them lean — most learners have some exposure.
- Topics 3–6 are the DCS-specific spine; they anchor the whole academy and are prerequisites for every track.
- Topic 17 (service catalog) is conceptual — deliver as orientation on the Architect track's intro, not a standalone text workshop.
- Observability (20–22) reuses a deployed app; sequence it after Developer B01.

### Future expansion ideas (deferred from v1)

- CI/CD & GitOps module — Tekton/OpenShift Pipelines, Argo CD, image promotion.
- Advanced networking — service mesh, network policies, multi-cluster.
- Stateful deep-dive — databases, backups, storage classes.
