# RBAC Deep Dive

**Go under the hood of access control — read the chain, then wire one up yourself.**

Access & Tenancy showed you *that* your access is scoped; this lab shows you *how*. Roles and
ClusterRoles define permissions, and bindings grant them to subjects — once you can read that
chain, RBAC stops being magic. You'll learn how rules compose from apiGroups, resources, and
verbs, trace an effective permission from subject through binding to rule, then create a Role
and RoleBinding in your own namespace and prove it takes effect.

- **Track:** Core — DCS Foundations · Lab 8 of 9
- **Audience:** Intermediate — you've run `oc auth can-i` and seen tenant isolation
- **Duration:** ~45 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a05-access-tenancy

## By the end of this lab you'll be able to

- Distinguish a Role (namespaced) from a ClusterRole (cluster-wide).
- Read a role's rules (apiGroups × resources × verbs) and predict what they allow.
- Distinguish a RoleBinding from a ClusterRoleBinding, and identify subjects.
- Trace an effective permission from subject → binding → role → rule.
- Create a Role + RoleBinding in your namespace and prove it takes effect.

## What you'll do

You'll dissect existing roles and bindings to predict what they permit, trace a permission
end to end through the RBAC chain, then create your own Role and RoleBinding in your namespace
and verify the grant with impersonation.
