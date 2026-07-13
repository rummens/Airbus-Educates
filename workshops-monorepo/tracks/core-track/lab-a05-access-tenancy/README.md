# Access & Tenancy

**Who you are on DCS, and exactly what you're allowed to do.**

Every earlier lab quietly assumed you had a namespace and the rights to work in it. This lab
shows where those come from: how a team onboards as a tenant, how your access is scoped to
your own namespaces, and how much of the cluster you're allowed to consume. The work is
inspection, not deployment — you ask the cluster about your identity, permissions, and quota
and read the answers, because access and tenancy are things you observe and reason about.

- **Track:** Core — DCS Foundations · Lab 5 of 9
- **Audience:** Beginner — comfortable running basic `oc` commands; no RBAC knowledge required
- **Duration:** ~35 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a01-what-is-dcs

## By the end of this lab you'll be able to

- Explain the DCS tenancy model — a Tenant owns one or more Namespaces — and why "project" is just OpenShift's word for a namespace, not a separate layer.
- Describe how a team onboards as a tenant and logs in with SSO.
- Use `oc auth can-i` to inspect what you may do in your own namespace, and prove that your access stops at its boundary.
- Read the ResourceQuota and LimitRange on your namespace and explain what they cap.
- Explain that a quota increase is an ITSM request, not a command you run.

## What you'll do

You'll run against your real OpenShift session namespace — real RBAC, real quota, not a
mock-up. You'll query your own permissions with `oc auth can-i`, prove tenant isolation by
hitting the boundary of what you can reach, and read the ResourceQuota and LimitRange that
cap your namespace. The full anatomy of Roles and bindings is the next lab, A08.
