---
title: Workshop Overview
---

In this workshop, part of **{{< param product_name >}}**, you'll go under the hood of
access control. You already asked "can I?" — now you'll see the objects that decide the
answer, and wire one up yourself.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, and the clickable actions you'll use here.
{{< /note >}}

The Access & Tenancy workshop showed you *that* your access is scoped. This one shows you
*how*: Roles and ClusterRoles define permissions, and bindings grant them to subjects. Once
you can read that chain, RBAC stops being magic.

## What You'll Learn

By the end you will be able to:

- Distinguish a **Role** (namespaced) from a **ClusterRole** (cluster-wide).
- Read a role's **rules** (apiGroups × resources × verbs) and predict what they allow.
- Distinguish a **RoleBinding** from a **ClusterRoleBinding**, and identify **subjects**.
- Trace an effective permission from **subject → binding → role → rule**.
- Create a **Role + RoleBinding** in your namespace and prove it takes effect.

## Prerequisites

- **lab-a05-access-tenancy** — you should have run `oc auth can-i` and seen tenant isolation.

## Your Environment

A **split terminal**, an editor, the web console, and your own {{< param product_short >}}
namespace where you can safely create Roles and RoleBindings.

## Time and Difficulty

- **Estimated time:** 45 minutes
- **Difficulty:** Intermediate

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
