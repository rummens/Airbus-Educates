# Course Topics

Topic inventory for the DCS Academy, organised by module. Topics are an inventory, not a 1:1 map to workshops — the mapping is in the `course-module-*.md` files.

## Module A — Foundations

1. **Containers & images** — what a container is, images, the OCI model (upstream).
2. **Kubernetes essentials** — Pods, Deployments, Services, config/secrets (upstream).
3. **DCS namespace types** — prod vs dev, differences, promotion (DCS-specific).
4. **DCS registry (Harbor)** — pull/push, projects, robot accounts, scan gates (DCS-specific).
5. **Tenancy & access** — onboarding, SSO/OAuth login, RBAC, quotas, self-service (DCS-specific).
6. **Networking on DCS** — Routes, DNS naming, egress restrictions (DCS-specific).

## Module B — Developer

7. **Deploying an app** — from image to running workload on DCS.
8. **Configuration & secrets** — externalising config, mounting secrets.
9. **Scaling, health & resources** — replicas, probes, requests/limits under quota.
10. **Debugging & logs** — inspecting pods, logs, events, common failures.
11. **Stateful workloads / storage** *(optional)* — PVCs, storage classes on DCS.

## Module C — Security & Compliance

12. **Image scanning & Harbor gates** — vulnerability scanning, gate policies.
13. **Pod security / SCC** — restricted policy, arbitrary UID, when baseline is needed.
14. **Secrets management** — good practice, avoiding secrets in images/logs.
15. **Supply chain & provenance** — signing, trusted sources, air-gapped supply.
16. **EU data-residency & compliance** — data locality, compliance workflows on DCS.

## Module D — Architect / Onboarding

17. **DCS service catalog** — what DCS offers and when to use each capability.
18. **Tenancy / landing-zone design** — structuring projects, quotas, environments.
19. **Reference architectures / golden paths** — recommended patterns for tenant apps.

## Module E — Observability

20. **Metrics & dashboards** — Prometheus/Thanos, Grafana for tenant apps.
21. **Logs** — accessing and querying application logs.
22. **Alerts** — defining and routing alerts for tenant apps.

## Notes on Topic Selection

- Topics 1–2 are the only pure-upstream fundamentals; keep them lean — most learners have some exposure.
- Topics 3–6 are the DCS-specific spine; they anchor the whole academy and are prerequisites for every track.
- Topic 17 (service catalog) is conceptual — deliver as orientation on the Architect track's intro, not a standalone text workshop.
- Observability (20–22) reuses a deployed app; sequence it after Developer B01.

### Future expansion ideas (deferred from v1)

- CI/CD & GitOps module — Tekton/OpenShift Pipelines, Argo CD, image promotion.
- Advanced networking — service mesh, network policies, multi-cluster.
- Stateful deep-dive — databases, backups, storage classes.
