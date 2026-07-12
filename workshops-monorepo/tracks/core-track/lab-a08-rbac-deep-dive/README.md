# lab-a08-rbac-deep-dive

**RBAC Deep Dive** — a DCS Academy Foundations workshop.

Go beyond `oc auth can-i`: understand Roles vs ClusterRoles, RoleBindings vs
ClusterRoleBindings, how rules (apiGroups × resources × verbs) compose, and trace a
permission from subject → binding → role → rule. Create a Role + RoleBinding in your own
namespace and prove it with impersonation.

Part of Module A (Foundations). Prerequisite: lab-a05-access-tenancy. Split out of A05 to
keep that lab short.
