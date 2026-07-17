---
title: "Operators on DCS"
---

Welcome to this workshop, part of **{{< param product_name >}}**. Every earlier lab had
you own a resource end to end — you wrote the Deployment, you own its lifecycle. This lab
introduces a different shape: an **Operator**, installed once by the platform, that watches
a **Custom Resource** you create and manages a whole application on your behalf. It's the
Developer track's capstone, and your on-ramp to {{< param product_short >}}'s dedicated
Operators track.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain the [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/): a controller that reconciles a Custom Resource toward its desired state.
- Distinguish a [CustomResourceDefinition (CRD)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) — a new resource *type* — from a Custom Resource (CR), an *instance* of that type.
- Explain [OLM](https://olm.operatorframework.io/) and OperatorHub at a high level, and why {{< param product_short >}}'s catalog is curated and air-gapped.
- State the {{< param product_short >}} ownership model: the platform installs and updates the operator; you own and operate the instance it manages.
- Create a Custom Resource, watch the operator reconcile it, and read its status.

## Prerequisites

This workshop assumes familiarity with:

- Deployments, labels and selectors, and the declarative apply/inspect loop (Core track).
- Basic [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) and how a ServiceAccount's permissions scope what runs in your namespace (**RBAC, Tenancy & Namespaces**, B05) — an operator-managed instance runs with permissions in *your* namespace.
- Comfortable reading YAML and `oc get`/`oc describe` output; no prior exposure to Operators or CRDs is assumed.

## Your Environment

A browser-based session with a split **terminal**, an **editor**, and a **console** view,
all scoped to your own OpenShift namespace — the same namespace model as every earlier
lab, no cluster-admin required. The CloudNativePG operator this lab uses is already
installed cluster-wide by the platform; you only create and inspect an *instance* of it.
Commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Advanced

## Further Reading

- [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [OpenShift Operators overview](https://docs.openshift.com/container-platform/latest/operators/understanding/olm-what-operators-are.html)
- [CloudNativePG](https://cloudnative-pg.io/docs/)
