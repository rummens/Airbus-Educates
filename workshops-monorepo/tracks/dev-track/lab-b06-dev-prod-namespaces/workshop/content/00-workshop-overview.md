---
title: "DEV vs PROD Namespaces & Policies"
---

Welcome to this workshop, part of **{{< param product_name >}}**. Back in the Core track's
**Expose Your App** lab, your [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html)
needed a **PROD-type namespace** — you were told the rule, but not the reason. In this
workshop you get two real namespaces, one DEV and one PROD, and you'll watch the same
Route get rejected in one and admitted in the other — live, not as a slide.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Distinguish DCS's **DEV** and **PROD** namespace types by their **policy posture**, not just their names.
- Explain the two concrete differences: PROD enforces harsher policies ([Kyverno](https://kyverno.io/docs/)) **and** can host a Route; DEV has looser policies **but** cannot host a Route.
- Deploy a workload to DEV, watch a Route get rejected there, then create the same Route successfully in PROD.
- Read a Kyverno [`ClusterPolicy`](https://kyverno.io/docs/policy-types/cluster-policy/overview/) that PROD enforces and explain what it checks.
- Describe **promotion** — moving a workload from DEV to PROD instead of editing PROD in place — and the trade-off the split buys you.

## Prerequisites

This workshop assumes you've completed **RBAC, Tenancy & Namespaces** (lab-b05) — or
already understand the [Tenant → Namespace model]({{< param dcs_docs_base_url >}}/tenancy/tenants-and-namespaces)
and basic [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) — and
**Expose Your App** (lab-a04), so a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/),
a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and a Route
are already familiar shapes. Comfort with [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
is assumed throughout.

## Your Environment

This session gives you a **terminal**, an **editor**, and a **web console** to
browse what you create — and, unlike most labs so far, two full namespaces of your own to
create and compare, with cluster-admin rights over both. Commands are run with `oc`
exactly as in earlier labs; nothing about how you invoke them changes here.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Kyverno documentation](https://kyverno.io/docs/) — the policy engine behind PROD's enforcement
- [OpenShift Routes](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html)
- [DCS namespace types]({{< param dcs_docs_base_url >}}/naas/dev-prod-lifecycle)
