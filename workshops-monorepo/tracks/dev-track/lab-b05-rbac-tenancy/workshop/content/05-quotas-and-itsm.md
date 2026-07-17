---
title: Quotas and the ITSM Path
---

RBAC decides **what you're allowed to do**. It says nothing about **how much** you can
consume while doing it — that's a separate, budget-based control.

## Read your namespace's budget

Every namespace on {{< param product_short >}} has a default quota — a **Basic** default or
a **Customized** one agreed for that tenant — capping CPU, memory, storage and more via a
[**ResourceQuota**](https://kubernetes.io/docs/concepts/policy/resource-quotas/):

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-quota-present
title: Verify a ResourceQuota is present in your namespace
timeout: 10
```

The output has two columns: **Used** and **Hard** — the current consumption against the
ceiling. Every Deployment or Pod you create draws against this quota; once `Used` reaches
`Hard` for any tracked resource, further creates are rejected until something is freed up or
the quota is raised.

## Read the default per-container limits

A [**LimitRange**](https://kubernetes.io/docs/concepts/policy/limit-range/) works alongside
the quota — it sets the default CPU/memory request and limit **applied automatically** to
any container that doesn't specify its own:

```terminal:execute
command: oc describe limitrange
```

```examiner:execute-test
name: verify-limitrange-present
title: Verify a LimitRange is present in your namespace
timeout: 10
```

This matters at scale: a Deployment with several replicas, none of them setting explicit
resources, can exhaust a quota fast simply by multiplying the LimitRange default per
replica. Setting explicit `resources.requests`/`resources.limits` on your own workloads
avoids that surprise.

## Increasing a quota is an ITSM request

If your namespace's quota is genuinely too small for real work, you don't edit the
ResourceQuota object yourself — you raise an
[**ITSM request**]({{< param dcs_docs_base_url >}}/support/itsm-requests) to the platform
team. {{< param product_short >}} is operated through a service-management workflow:
**Service Requests** cover quota increases (along with image mirroring, catalog additions,
repo creation, and security exceptions), and **Incidents** cover problems. Much of
{{< param product_short >}}'s self-service model runs through this ticketing rather than
direct cluster-admin access — quota increases are one concrete example of where that applies.

That closes the loop: RBAC decides what you can do, the quota and LimitRange decide how much
of it you can do at once, and an ITSM request is how that ceiling gets raised when it's
genuinely too low.
