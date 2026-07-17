# RBAC, Tenancy & Namespaces

**See the mechanism behind "your namespace" — the RBAC objects that decide who can do what, and prove it yourself.**

Core gave you the words: Tenant, Namespace, "no separate project layer." This lab opens the
hood. You'll go from the answer — `oc auth can-i` — back to the objects that produce it
(Role, ClusterRole, RoleBinding, ClusterRoleBinding), trace a real permission from subject to
rule, then author a Role and RoleBinding of your own in your namespace and prove their exact
effect with impersonation. It closes with the namespace's resource quota and how an increase
actually gets requested on DCS.

- **Track:** Developer — Build on DCS · Lab 5
- **Audience:** Intermediate — you've completed the Core track (Core A06 gave the vocabulary)
- **Duration:** ~45 min
- **Format:** Hands-on, guided — split terminal, editor, and console, runs in your own OpenShift session namespace
- **Prerequisites:** lab-a06-terms-namespaces-tenancy; comfortable with basic `oc` usage and namespaces

## By the end of this lab you'll be able to

- Explain the Tenant → Namespaces model in depth and why there is no separate "project" layer.
- Distinguish Role vs ClusterRole and RoleBinding vs ClusterRoleBinding, and read a role's rules.
- Trace an effective permission from subject → binding → role → rule.
- Create a Role and RoleBinding in your own namespace and prove least privilege with `oc auth can-i --as`.
- Read a namespace's ResourceQuota and explain that an increase is requested, not self-served.

## What you'll do

Start from "can I?" and work backwards to the objects behind the answer, reading a built-in
ClusterRole and the RoleBinding already granting you access to your own namespace. Then author
a Role + RoleBinding of your own, bind it to a ServiceAccount, and use `--as` impersonation to
show the before (denied) and after (granted) state of a permission — including proving what it
does *not* grant. Finish by reading your namespace's ResourceQuota and LimitRange and learning
the ITSM path for a quota increase.
