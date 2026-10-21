---
title: "RBAC & Tenancy"
---

The Core lab **Terms — Namespaces & Tenancy** gave you the words: Tenant, Namespace, and the
fact that "project" is not a separate layer.

This lab opens the mechanism underneath: the RBAC objects that decide who can do what, in
which namespace.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You will Learn

By the end of this workshop you will be able to:

- Explain the **Tenant → Namespaces** model in depth, and why there is no separate "project" layer.
- Distinguish **Role vs ClusterRole** and **RoleBinding vs ClusterRoleBinding**, and read a role's rules.
- Trace an effective permission from **subject → binding → role → rule**.
- Create a Role and RoleBinding in your own namespace and prove least privilege with `oc auth can-i --as`.
- Read a namespace's ResourceQuota and explain that a quota increase is requested, not self-served.

## Prerequisites

This lab assumes the Core lab **Terms — Namespaces & Tenancy**, so you know the terms
Namespace and Tenant and that access is scoped to your tenant's namespaces. It also assumes
basic comfort with
[`oc`](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/cli_tools/openshift-cli-oc#cli-getting-started)
and the idea of a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).
No prior RBAC knowledge is required.

## Your Environment

A browser-based session with a **terminal** and an **editor** for the Role and RoleBinding
manifests. Your access is scoped to your own session namespace, and every object you create
here (ServiceAccount, Role, RoleBinding) lives inside it. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [OpenShift using RBAC](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/authentication_and_authorization/using-rbac)
- [ResourceQuota documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
