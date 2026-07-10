# DCS Concepts Reference

The Digital Container Service (DCS) is Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. Some concepts learners meet are **DCS-specific** — they are not standard Kubernetes/OpenShift and must be explained on DCS terms, linking to the DCS documentation portal rather than upstream docs.

This reference is the shared source of truth for those concepts, using DCS's own terminology. When a workshop introduces one:

1. Give the **inline blurb** below (or a workshop-tailored version) so an air-gapped learner understands it without following any link.
2. Link the DCS docs via the `dcs_docs_base_url` param: `[<concept>]({{< param dcs_docs_base_url >}}<path>)`. **The `<path>` values below are placeholder patterns, not real URLs** — align them to the live portal when known. See [documentation-links-reference.md](documentation-links-reference.md) and [workshop-variables-reference.md](workshop-variables-reference.md).

Standard constructs mentioned alongside these (Deployment, Secret, ServiceAccount, Route…) still link to **upstream** docs — only the DCS-specific concept links to the DCS portal.

## DCS terminology (use these exact terms)

- **Namespace as a Service (NaaS)** — DCS's core offering; a namespace is the unit teams consume.
- **Tenant** — a team/organisation; owns one or more Projects/Namespaces.
- **DEV namespace** / **PROD namespace** — the two namespace lifecycle types, with different controls.
- **Shared cluster** (default, recommended) vs **Dedicated Managed cluster**.
- **Catalog** — how images are made available: DCS Catalogs, Allowed External Registries, and the Proxy-Cached Catalog.
- **Robot account** — non-human credential for pushing/pulling to Harbor.
- **ITSM request / incident** — the self-service ticket workflow for quota increases, image mirroring, repo requests, and security exceptions.

## Core DCS concepts

### Tenancy: Namespace, Project, Tenant

**Blurb:** DCS uses a three-level model. A **Kubernetes Namespace** is the low-level isolation boundary; an **OpenShift Project** wraps a namespace with additional access controls; a **Tenant** is the team/organisation that owns one or more projects. Isolation between tenants on a shared cluster is enforced with RBAC and Network Policies. Access is via SSO; a tenant only ever sees its own projects.

- Path (placeholder): `/tenancy/namespaces-projects-tenants`
- Taught in: Foundations A05. Underpins every track.

### Namespace as a Service (NaaS) — DEV vs PROD lifecycle

**Blurb:** DCS delivers namespaces as a service. Each namespace is a **DEV** or **PROD** type with a distinct lifecycle. DEV favours fast iteration and looser controls; PROD enforces stricter policy and change control. Work is **promoted** from DEV to PROD rather than edited in place. (Notably, PROD namespaces cannot pull from the Proxy-Cached Catalog — see Registry.)

- Path (placeholder): `/naas/dev-prod-lifecycle`
- Taught in: Foundations A03. Represented in-session via a virtual cluster so both types are visible.

### Cluster types (shared vs dedicated)

**Blurb:** Workloads run on a **shared cluster** by default — the most resource-efficient option, with tenants isolated by RBAC and Network Policies. A **Dedicated Managed cluster** is available where isolation or capacity needs demand it. Choice affects cost/recharging.

- Path (placeholder): `/clusters/types`
- Taught in: Foundations A01 (orientation); Architect track (design/cost).

### Registry (Harbor) — catalogs, robot accounts, mirroring

**Blurb:** DCS provides a Harbor registry as the single source of images (the platform is air-gapped). Images reach it through **catalogs**: the **DCS Catalogs**, a set of **Allowed External Registries**, and a **Proxy-Cached Catalog** (a caching proxy for permitted upstreams; not usable from PROD namespaces). External images are brought in by **image mirroring**, requested via an **ITSM ticket** (External→DCS Harbor, or DCS Harbor→DCS Harbor). Harbor organises content into projects, stores container images **and Helm charts**, uses **robot accounts** for automation, and manages repos/permissions **the GitOps way**. Images are gated by vulnerability scanning.

- Path (placeholder): `/registry/overview`
- Taught in: Foundations A04; deepened in Security C01 (scan gates) and C04 (supply chain / mirroring).
- All image references in workshops resolve to Harbor — see [air-gapped-images-reference.md](air-gapped-images-reference.md).

### Networking — Service, Route, Load Balancer, Network Policies

**Blurb:** An app is reached in-cluster via a **Service**, exposed externally via an OpenShift **Route**, which is fronted by an **External Load Balancer** at the cluster edge, using DCS-managed DNS. On the shared cluster, **Network Policies** (matching on labels) control which workloads may talk to each other — the default posture is restrictive, and egress is limited (air-gapped).

- Path (placeholder): `/networking/overview`
- Taught in: Foundations A06. Network Policies revisited in Security track.
- Follow the Route/session-proxy guidance in [openshift-reference.md](openshift-reference.md).

### Resource quotas & requests

**Blurb:** Each namespace has a default quota (a **Basic** default or a **Customized** one) capping CPU, memory, storage, egress IPs, etc. Platform capacity is finite; workloads set requests/limits within the quota. A **quota increase** is requested via an **ITSM ticket**.

- Path (placeholder): `/quotas/limits-and-requests`
- Taught in: Foundations A05; applied in Developer B03. `ResourceQuota`/`LimitRange` constructs → upstream.

### ITSM requests & incidents

**Blurb:** DCS is operated through a service-management workflow. **Service Requests** (ITSM tickets) cover quota increases, image mirroring, catalog additions, repo creation, and security exceptions; **Incidents** are raised for problems. Much of DCS self-service runs through this ticketing rather than direct cluster admin.

- Path (placeholder): `/support/itsm-requests`
- Referenced wherever a workshop step would, in real life, require a ticket (mirroring, quota increase). In workshops, model the outcome; point at the ITSM process via docs.

### Governance & compliance

**Blurb:** DCS defines a **Responsibility Matrix (RACI)** splitting duties between the platform and tenants, a **Data Classification** scheme (multi-national — e.g. Germany and Spain), a **Security Exception Process**, and **Terms & Conditions** covering access, storage/data, and image/registry policies.

- Path (placeholder): `/governance/overview`
- Taught in: Security & Compliance track (C02, C05). Architect track references the responsibility split.

## Adding a new DCS concept

When a workshop needs a DCS-specific concept not listed here, add it (blurb + placeholder path + where taught) so it is defined once and reused consistently, rather than re-explained divergently across workshops.

## Checklist

- [ ] Every DCS-specific concept a workshop mentions has a blurb inline and a `{{< param dcs_docs_base_url >}}` link
- [ ] DCS terminology is used exactly (NaaS, DEV/PROD namespace, Tenant, Catalog, Proxy-Cached Catalog, robot account, ITSM request)
- [ ] Standard Kubernetes/OpenShift constructs are not mislinked to the DCS portal
- [ ] New DCS concepts introduced by a workshop are added here
