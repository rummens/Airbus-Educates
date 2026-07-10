# DCS Concepts Reference

The Digital Container Service (DCS) is Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. Some concepts learners meet are **DCS-specific** — they are not standard Kubernetes/OpenShift and must be explained on DCS terms, linking to the DCS documentation portal rather than upstream docs.

This reference is the shared source of truth for those concepts. When a workshop introduces one:

1. Give the **inline blurb** below (or a workshop-tailored version) so an air-gapped learner understands it without following any link.
2. Link the DCS docs via the `dcs_docs_base_url` param: `[<concept>]({{< param dcs_docs_base_url >}}<path>)`. See [documentation-links-reference.md](documentation-links-reference.md) and [workshop-variables-reference.md](workshop-variables-reference.md).

Standard constructs mentioned alongside these (Deployment, Secret, ServiceAccount, Route…) still link to **upstream** docs — only the DCS-specific concept links to the DCS portal.

## The four core DCS concepts

### Namespace types (prod vs dev)

**Blurb:** On DCS, a project is provisioned as a *dev* or *prod* namespace type. The types differ in guarantees and controls — dev namespaces favour fast iteration and looser limits; prod namespaces enforce stricter policy, change control, and resource commitments. Workloads are promoted from dev to prod rather than edited in place.

- Docs path (param-relative): `/concepts/namespace-types`
- Taught in: Foundations A03. Referenced wherever workshops deploy to a specific namespace type.
- Represented in sessions via a **virtual cluster** so learners see the two namespace types side by side.

### Registry (Harbor)

**Blurb:** DCS provides a Harbor image registry as the single source of container images. All images are pulled from and pushed to Harbor; the platform is air-gapped, so external registries are not reachable. Harbor organises images into projects, uses robot accounts for automation, and gates images through vulnerability scanning.

- Docs path: `/concepts/registry`
- Taught in: Foundations A04; deepened in Security C01 (scan gates).
- All image references in workshops resolve to Harbor — see [air-gapped-images-reference.md](air-gapped-images-reference.md).

### Tenancy & access

**Blurb:** Teams onboard to DCS as tenants. Access is via SSO/OAuth; permissions are granted through RBAC roles scoped to the team's projects. Each project carries resource quotas and is requested through a self-service workflow. A user only ever sees and acts within their own tenant's projects.

- Docs path: `/concepts/tenancy-and-access`
- Taught in: Foundations A05.
- In-session, the Educates session namespace models a single tenant project; the vcluster provides tenant-scoped RBAC realism.

### Networking on DCS

**Blurb:** Applications are exposed on DCS through OpenShift Routes with DCS-managed DNS naming. Egress from workloads is restricted (air-gapped), so apps reach only in-cluster and explicitly-allowed endpoints. Ingress hostnames follow DCS naming conventions.

- Docs path: `/concepts/networking`
- Taught in: Foundations A06. Referenced wherever workshops expose a service.
- Follow the Route/session-proxy guidance in [openshift-reference.md](openshift-reference.md).

## Adding a new DCS concept

When a workshop needs a DCS-specific concept not listed here, add it to this reference (blurb + docs path + where taught) so it is defined once and reused consistently, rather than re-explained divergently across workshops.

## Checklist

- [ ] Every DCS-specific concept a workshop mentions has a blurb inline and a `{{< param dcs_docs_base_url >}}` link
- [ ] Standard Kubernetes/OpenShift constructs are not mislinked to the DCS portal
- [ ] New DCS concepts introduced by a workshop are added here
