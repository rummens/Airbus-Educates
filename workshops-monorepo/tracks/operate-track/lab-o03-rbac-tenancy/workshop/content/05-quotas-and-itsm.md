---
title: Quotas and the ITSM Path
---

RBAC decides **what you are allowed to do**. It says nothing about **how much** you may
consume while doing it, which is a separate control.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/quotas
```

## Read your namespace's budget

Every namespace on {{< param product_short >}} has a quota, either the **Basic** default or
a **Customized** one agreed for that tenant. It caps CPU, memory, storage and more through a
[**ResourceQuota**](https://kubernetes.io/docs/concepts/policy/resource-quotas/):

```terminal:execute
command: oc describe quota
```

```examiner:execute-test
name: verify-quota-present
title: Verify a ResourceQuota is present in your namespace
timeout: 10
```

The output has two columns, **Used** and **Hard**: current consumption against the ceiling.
Every Deployment or Pod you create draws against this quota, and once `Used` reaches `Hard`
for any tracked resource, further creates are rejected until something is freed or the quota
is raised.

On {{< param product_short >}} a namespace has **exactly one** ResourceQuota and **one**
LimitRange, both set when the namespace is created. This training namespace lists a few extra
quotas that the Academy's own tooling adds.

## Read the default per-container limits

A [**LimitRange**](https://kubernetes.io/docs/concepts/policy/limit-range/) works alongside
the quota. It sets the default CPU and memory request and limit **applied automatically** to
any container that does not set its own:

```terminal:execute
command: oc describe limitrange
```

```examiner:execute-test
name: verify-limitrange-present
title: Verify a LimitRange is present in your namespace
timeout: 10
```

This matters at scale. A Deployment with several replicas, none of them setting explicit
resources, can fill a quota quickly by multiplying the LimitRange default per replica.
Setting `resources.requests` and `resources.limits` on your own workloads avoids that.

## Increasing a quota is an ITSM request

If your namespace's quota is too small for real work, you do not edit the ResourceQuota
object yourself. You raise an
[**ITSM request**]({{< param dcs_docs_base_url >}}/support/itsm-requests) to the platform
team. **Service Requests** cover quota increases, along with image mirroring, catalog
additions, repository creation and security exceptions; **Incidents** cover problems.

RBAC decides what you can do, the quota and LimitRange decide how much of it you can do at
once, and an ITSM request is how that ceiling is raised.
