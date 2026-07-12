# lab-a05-access-tenancy

**Access & Tenancy** — Foundations (Module A, core) workshop for the DCS Academy.

Learners see how a team onboards to DCS and how their access is scoped: the **Tenant → Namespaces**
model, RBAC basics (`oc auth can-i`, proving tenant isolation), and the resource quota on their
namespace. Read-only inspection, plus one guided RBAC apply as the closing challenge. The RBAC
deep dive (Roles/ClusterRoles/bindings anatomy) is its own later lab. Prerequisite: lab-a01-what-is-dcs.

Runs in the real **OpenShift session namespace** (not a virtual cluster) so the RBAC and quota
the learner inspects are the platform's own.

Built with the `airbus-educates-workshop-authoring` skill. See the plan at
`planning/workshop-plans/lab-a05-access-tenancy.md`.
