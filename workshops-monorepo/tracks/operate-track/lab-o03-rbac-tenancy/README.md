# RBAC & Tenancy

**Read the RBAC objects that decide why you cannot see another team's Pods.**

Core gave you the words: **Tenant**, **Namespace**, and the fact that "project" is not a
separate layer. This lab opens the mechanism underneath, the RBAC objects that decide who may
do what, and where.

You start from `oc auth can-i`, then go behind the answer to the **Role**, **RoleBinding** and
**rule** that produced it.

Then you build that chain yourself: create a ServiceAccount, check that it can do
**nothing**, grant it a read-only Role, and check again with `--as`, before and after.

The lab ends on quotas: what your namespace was given, and why an increase is a request rather than a
setting you can edit.

> **💡 Tip:** `oc auth can-i --as` tests any subject's access without you logging in as
> them.

- **Track:** Operate & Observe
- **Audience:** Intermediate, no prior RBAC knowledge needed
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Terms — Namespaces & Tenancy**.

## By the end of this lab you will be able to

- Explain the **Tenant → Namespaces** model, and why there is no separate "project" layer.
- Tell **Role** from **ClusterRole**, and **RoleBinding** from **ClusterRoleBinding**.
- Trace an effective permission from subject → binding → role → rule.
- Create a Role and RoleBinding, and prove least privilege with `oc auth can-i --as`.
- Read your namespace's quota, and say what happens when you need more.

## What you will do

1. **Ask** what you may do, and what you may not.
2. **Read** the objects that produced those answers.
3. **Create** a ServiceAccount with no access at all.
4. **Grant** it a read-only Role and prove what changed.
5. **Read** the quota your namespace was given.
