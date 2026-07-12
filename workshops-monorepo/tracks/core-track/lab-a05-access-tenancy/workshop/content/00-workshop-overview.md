---
title: Workshop Overview
---

Welcome back. This workshop, part of **{{< param product_name >}}**, is about *who you are*
on the platform and *what you're allowed to do*. Every earlier lab quietly assumed you had a
namespace and the rights to work in it — here you'll see where those come from: how a team
onboards as a tenant, how your access is scoped to your own namespaces, and how much of the
cluster you're allowed to consume.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

Unlike most Foundations labs, you won't deploy anything here. The work is *inspection* — you'll
ask the cluster questions about your identity, your permissions, and your quota, and read the
answers. That's deliberate: access and tenancy are things you observe and reason about, not
things you build.

## What You'll Learn

By the end you will be able to:

- Explain the {{< param product_short >}} tenancy model — a **Tenant** owns one or more **Namespaces** — and why "project" is just OpenShift's word for a namespace, not a separate layer.
- Describe how a team onboards as a tenant and logs in with SSO.
- Use `oc auth can-i` to inspect what you may do in your own namespace, and prove that your access stops at its boundary.
- Read the [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) and [LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/) on your namespace and explain what they cap.
- Explain that a quota increase is an **ITSM request**, not a command you run.

## Prerequisites

- **lab-a01-what-is-dcs** — you should know what {{< param product_short >}} is and be comfortable running basic [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) commands.

No prior knowledge of [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) is
required — we keep it to the basics here. The full RBAC deep dive is a later lab.

## Your Environment

A **split terminal**, an editor, and the OpenShift web console, connected to your own
{{< param product_short >}} namespace with **real** RBAC and quota — so everything you inspect
is the platform's actual configuration, not a mock-up. Commands are run with `oc` in the terminal.

## Time and Difficulty

- **Estimated time:** 35 minutes
- **Difficulty:** Beginner

## Further Reading

- [Tenancy on {{< param product_short >}}]({{< param dcs_docs_base_url >}}/tenancy/tenants-and-namespaces)
- [Using RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
