---
title: "Operators on DCS"
---

Every earlier lab had you own a resource end to end: you wrote the Deployment, and you own
its lifecycle.

This lab is a different shape. An **Operator** is installed once by the platform, watches a
**Custom Resource** you create, and manages a whole application from it. That is how every
platform service on **{{< param product_name >}}** is offered.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You will Learn

By the end of this workshop you will be able to:

- Explain the [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/): a controller that reconciles a Custom Resource toward its desired state.
- Distinguish a [CustomResourceDefinition (CRD)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) — a new resource *type* — from a Custom Resource (CR), an *instance* of that type.
- Explain [OLM](https://olm.operatorframework.io/) and OperatorHub at a high level, and why {{< param product_short >}}'s catalog is curated and air-gapped.
- State the {{< param product_short >}} ownership model: the platform installs and updates the operator; you own and operate the instance it manages.
- Create a Custom Resource, watch the operator reconcile it, and read its status.

## Prerequisites

This workshop assumes familiarity with:

- Deployments, labels and selectors, and the declarative apply/inspect loop (Core track).
- Basic [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) and how a ServiceAccount's permissions scope what runs in your namespace (**RBAC & Tenancy**), because an operator-managed instance runs with permissions in *your* namespace.
- Reading YAML and `oc get` / `oc describe` output. No prior exposure to Operators or CRDs is assumed.

## Your Environment

A browser-based session with a split **terminal** and an **editor**, scoped to your own
namespace. No cluster-admin is required. The CloudNativePG operator this lab uses is already
installed cluster-wide by the platform, and you create and inspect an *instance* of it. All
commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Advanced

## Further Reading

- [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [OpenShift Operators overview](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/operators/understanding-operators#olm-what-operators-are)
- [CloudNativePG](https://cloudnative-pg.io/docs/)
