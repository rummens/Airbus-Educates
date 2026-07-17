# DCS Concepts Reference

The Digital Container Service (DCS) is Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. Some concepts learners meet are **DCS-specific** — they are not standard Kubernetes/OpenShift and must be explained on DCS terms, linking to the DCS documentation portal rather than upstream docs.

This reference is the shared source of truth for those concepts, using DCS's own terminology. When a workshop introduces one:

1. Give the **inline blurb** below (or a workshop-tailored version) so an air-gapped learner understands it without following any link.
2. Link the DCS docs via the `dcs_docs_base_url` param: `[<concept>]({{< param dcs_docs_base_url >}}<path>)`. **The `<path>` values below are placeholder patterns, not real URLs** — align them to the live portal when known. See [documentation-links-reference.md](documentation-links-reference.md) and [workshop-variables-reference.md](workshop-variables-reference.md).

Standard constructs mentioned alongside these (Deployment, Secret, ServiceAccount, Route…) still link to **upstream** docs — only the DCS-specific concept links to the DCS portal.

## DCS terminology (use these exact terms)

- **Namespace as a Service (NaaS)** — DCS's core offering; a namespace is the unit teams consume.
- **Tenant** — a team/organisation (org level, used for recharging & accountability); owns one or more **Namespaces**. There is **no separate "project" layer** — "project" is just OpenShift's word for a namespace.
- **DEV namespace** / **PROD namespace** — the two namespace lifecycle types, with different controls. The concrete difference: **PROD enforces Kyverno admission policies; DEV does not.**
- **Shared cluster** (default, recommended) vs **Dedicated Managed cluster**.
- **Catalog** — how images are made available: DCS Catalogs, Allowed External Registries, and the Proxy-Cached Catalog.
- **Robot account** — non-human credential for pulling from (and, with a dedicated project, pushing to) Harbor. Foundations uses read-only pull.
- **ITSM request / incident** — the self-service ticket workflow for quota increases, image mirroring, repo requests, security exceptions, and S3 storage provisioning.

## Core DCS concepts

### Tenancy: Tenant → Namespaces

**Blurb:** DCS uses a **two-level** model. A **Tenant** is the team/organisation — the org-level unit used for recharging and accountability — and it owns one or more **Namespaces** (DEV/PROD types). There is **no separate "project" layer**: on OpenShift, "project" is simply another word for a namespace, not a distinct level. Isolation between tenants on a shared cluster is enforced with RBAC and Network Policies. Access is via SSO; a tenant only ever sees its own namespaces.

- Path (placeholder): `/tenancy/tenants-and-namespaces`
- Taught in: Foundations A05 (basics) and A08 (RBAC depth). Underpins every track.
- **Do not** teach a Namespace→Project→Tenant three-level model (an earlier draft did — it is wrong).

### Namespace as a Service (NaaS) — DEV vs PROD lifecycle

**Blurb:** DCS delivers namespaces as a service. Each namespace is a **DEV** or **PROD** type with a distinct lifecycle. DEV favours fast iteration and looser controls; **PROD enforces Kyverno admission policies** (the concrete DEV-vs-PROD difference) plus stricter change control. Work is **promoted** from DEV to PROD rather than edited in place. (Notably, PROD namespaces cannot pull from the Proxy-Cached Catalog — see Registry — and an OpenShift Route requires a PROD-type namespace — see Networking.)

- Path (placeholder): `/naas/dev-prod-lifecycle`
- Taught in: Foundations A03. Represented in-session via a virtual cluster so both types are visible.
- **Kyverno** is a standard construct → link [kyverno.io](https://kyverno.io/docs/) upstream; the DCS *policy set* is DCS-specific.

### Cluster types (shared vs dedicated)

**Blurb:** Workloads run on a **shared cluster** by default — the most resource-efficient option, with tenants isolated by RBAC and Network Policies. A **Dedicated Managed cluster** is available where isolation or capacity needs demand it. Choice affects cost/recharging.

- Path (placeholder): `/clusters/types`
- Taught in: Foundations A01 (orientation); Architect track (design/cost).

### Registry (Harbor) — catalogs, robot accounts, mirroring

**Blurb:** DCS provides a Harbor registry as the single source of images (the platform is air-gapped). Images reach it through **catalogs**: the **DCS Catalogs**, a set of **Allowed External Registries**, and a **Proxy-Cached Catalog** (a caching proxy for permitted upstreams; not usable from PROD namespaces). External images are brought in by **image mirroring**, requested via an **ITSM ticket** (External→DCS Harbor, or DCS Harbor→DCS Harbor). Harbor organises content into projects, stores container images **and Helm charts**, uses **robot accounts** for automation, and manages repos/permissions **the GitOps way**. Images are gated by vulnerability scanning.

- Path (placeholder): `/registry/overview`
- Taught in: Foundations A04; deepened in Security C01 (scan gates) and C04 (supply chain / mirroring).
- **Foundations A04 is pull-only** and uses **`skopeo`** (daemonless — no `docker`/`podman` inside a workshop container, to avoid double-virtualization). **Pushing** needs a dedicated Harbor project + push-capable robot account and is taught as a concept only. The read-only robot account is provided to the session.
- All image references in workshops resolve to Harbor — see [air-gapped-images-reference.md](air-gapped-images-reference.md).

### Networking — Service, Route, Load Balancer, Network Policies

**Blurb:** An app is reached in-cluster via a **Service**, exposed externally via an OpenShift **Route**, which is fronted by an **External Load Balancer** at the cluster edge, using DCS-managed DNS. The external load balancer is **not** a native Kubernetes object — it is a DCS **security requirement** placing a controlled, monitored edge in front of the cluster so outside traffic never hits it directly. **A Route requires a PROD-type namespace** on DCS. On the shared cluster, **Network Policies** (matching on labels) control which workloads may talk to each other — the default posture is restrictive. Egress is **deny-by-default** (air-gapped): there is no open path to the internet, but specific external destinations *can* be reached through a **managed egress proxy** when **explicitly whitelisted and enabled** per request — it is never on by default.

Accuracy notes (do not overstate):
- Don't say "no internet, ever" — say egress is deny-by-default and approved destinations are reachable via the managed proxy once enabled.
- Network Policies are **observe-only** for tenants today (self-service authoring is on the roadmap) — teach them as "inspect", not "author".

- Path (placeholder): `/networking/overview`
- Taught in: Foundations A06. Network Policies revisited in Security track.
- **Tenants cannot self-create Network Policies yet** (on the DCS roadmap) — teach NetworkPolicy as observe/concept (inspect a pre-provisioned one), not a hands-on create.
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

### Storage — PVCs, storage classes, S3

**Blurb:** DCS offers persistent storage through standard Kubernetes **PersistentVolumeClaims (PVCs)** backed by DCS **StorageClasses**. Two access types are available via PVC: **File** storage (shareable, RWX-capable) and **Block** storage (single-writer, RWO). The right storage class is driven by **data and security classification** — less about which *country* and more about the **classification level**: some data (e.g. **NATO** or otherwise international-restricted) must sit on **physically separated** disks, kept apart from national data, which means its own dedicated StorageClass. **Object (S3) storage is available on DCS** — it's just not self-service like a PVC: you request a bucket **via an ITSM ticket to the storage team** and consume it over the S3 API. So: File and Block via a PVC; S3 by request — same platform, different path.

Accuracy notes (do not overstate):
- Frame the S3 story as *available, provisioned differently* — not "there is no S3 / don't look for it". Avoid harsh dead-ends.
- Classification framing is national vs international (NATO) → physical separation → dedicated SC, not simply "DE vs ES residency".
- A **non-root** app cannot write a root-owned PV mounted at a root path like `/data` — mount under the image's writable home (e.g. `/opt/app-root/src/data`). See [openshift-reference.md](openshift-reference.md).

- Path (placeholder): `/storage/overview`
- Taught in: Foundations A07 (concept + persistence); Developer B05 (stateful deep dive).
- Storage-class **names are variabilised** (`dcs_sc_file`, `dcs_sc_block`) — never hardcode them. `PersistentVolume`/`StorageClass`/`PersistentVolumeClaim` constructs → upstream.

### RBAC on DCS

**Blurb:** Access on DCS is scoped with Kubernetes **RBAC**: **Roles**/**ClusterRoles** define permissions (rules over apiGroups × resources × verbs), and **RoleBindings**/**ClusterRoleBindings** grant them to subjects (users, groups, ServiceAccounts). A tenant's access is confined to its own namespaces. Tenants may manage Roles/RoleBindings **within their own namespaces**; cluster-scoped RBAC is platform-managed (read-only to tenants).

- Path (placeholder): `/concepts/rbac`
- Taught in: Foundations A05 (basics — `oc auth can-i`, isolation) and A08 (depth — the objects). RBAC construct → upstream.

### Operators & the DCS ownership model

**Blurb:** DCS offers several platform services as **OpenShift Operators**, not as managed/aaS. An **Operator** is a controller that watches a **Custom Resource (CR)** — an instance of a type defined by a **CRD** — and continuously reconciles the managed application toward the desired state. Operators are installed cluster-wide by the platform via **OLM** (Operator Lifecycle Manager), surfaced through **OperatorHub**. The key DCS distinction: **the platform owns the operator (install, upgrades, CRD versions); the tenant owns the application instance** the operator manages — its sizing, config, data, backups, CR upgrades, and day-2 operations. This is *not* a managed DBaaS/SaaS where the provider owns day-2.

- Path (placeholder): `/concepts/operators`
- Taught in: Foundations A09 (concept + one CR). Applied per service in the Operators track (Module F: GitLab, Argo CD, CloudNativePG).
- Operator pattern / CRD / CR / OLM / OperatorHub are standard constructs → link upstream (kubernetes.io Operator pattern, OpenShift Operators docs). The **ownership split** is the DCS-specific point → DCS docs + the Responsibility Matrix (see Governance).

## Adding a new DCS concept

When a workshop needs a DCS-specific concept not listed here, add it (blurb + placeholder path + where taught) so it is defined once and reused consistently, rather than re-explained divergently across workshops.

## Checklist

- [ ] Every DCS-specific concept a workshop mentions has a blurb inline and a `{{< param dcs_docs_base_url >}}` link
- [ ] DCS terminology is used exactly (NaaS, DEV/PROD namespace, Tenant, Catalog, Proxy-Cached Catalog, robot account, ITSM request)
- [ ] Standard Kubernetes/OpenShift constructs are not mislinked to the DCS portal
- [ ] New DCS concepts introduced by a workshop are added here
