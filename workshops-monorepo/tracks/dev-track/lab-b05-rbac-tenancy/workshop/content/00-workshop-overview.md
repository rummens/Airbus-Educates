---
title: "RBAC, Tenancy & Namespaces"
---

Welcome to this workshop, part of **{{< param product_name >}}**. In Core A06 you learned
the *words* — Tenant, Namespace, and that "project" is not a separate layer. Here you open
up the *mechanism* behind them: the RBAC objects that actually decide who can do what, in
which namespace, and why.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the **Tenant → Namespaces** model in depth, and why there is no separate "project" layer.
- Distinguish **Role vs ClusterRole** and **RoleBinding vs ClusterRoleBinding**, and read a role's rules.
- Trace an effective permission from **subject → binding → role → rule**.
- Create a Role and RoleBinding in your own namespace and prove least privilege with `oc auth can-i --as`.
- Read a namespace's ResourceQuota and explain that a quota increase is requested, not self-served.

## Prerequisites

This workshop assumes you've completed **Core A06 — Terms: Namespaces & Tenancy**, so you
already know the *terms* Namespace and Tenant and that access is scoped to your tenant's
namespaces. It also assumes basic comfort with
[`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
and the idea of a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).
No prior RBAC knowledge is required — that's what this lab teaches.

## Your Environment

This session provides a browser-based environment with a split **terminal**, an **editor**
for viewing and editing the Role/RoleBinding manifests, and the **web console** for viewing
roles, bindings and quota visually. You have OpenShift access scoped to your own session
namespace — every object you create here (ServiceAccount, Role, RoleBinding) lives inside
it. Commands are run with `oc`.

## Time and Difficulty

- **Estimated time:** 45 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [OpenShift using RBAC](https://docs.openshift.com/container-platform/latest/authentication/using-rbac.html)
- [ResourceQuota documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
