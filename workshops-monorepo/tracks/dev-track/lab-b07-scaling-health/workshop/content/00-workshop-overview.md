---
title: "Scaling, Health & Resources"
---

Welcome to this workshop, part of **{{< param product_name >}}**. Your `hello-dcs` app has
so far run as one, unmonitored replica — fine for a demo, not fine for anything real. In
this lab you scale it, teach it to prove its own health, and make it fit the resource
budget its namespace was actually given.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Scale a Deployment and reason about replica count against a namespace quota.
- Read a namespace's `ResourceQuota` to tell whether a rollout has room to land.
- Diagnose a quota rejection from cluster events, and fix it by right-sizing requests/limits.
- Add liveness and readiness probes, and explain what each one actually protects.
- Delete a Pod and confirm the platform reconciles it back to the desired replica count.

## Prerequisites

- **A01 — Deploy Your First App.** You know Deployments, `oc scale`, and the
  Deployment → ReplicaSet → Pod chain.
- **A02 — Configure & Troubleshoot Your App.** You know how to trigger a rollout and read
  `oc describe` / `oc get events` when something goes wrong.

This lab does **not** re-teach `oc scale` mechanics or basic quota vocabulary — it assumes
you have them and puts them to work. If you've also done **B05 — Tenancy & RBAC**, you've
already read your namespace's `ResourceQuota` and `LimitRange` once; this lab is where that
budget stops being an abstract reading exercise and starts rejecting things.

## Your Environment

A browser-based session with a split **terminal**, an **editor**, and a **console** tab so
you can watch replica counts and events land as you scale and apply manifests. The
`hello-dcs` app is already running — one replica, no probes, no explicit resources — and
you'll open the manifest you grow it into during the exercises.

All commands run with `oc` against your own session namespace, which carries a `medium`
resource budget — deliberately sized so you can hit it on purpose before you learn to fit
inside it.

## Time and Difficulty

- **Estimated time:** 28 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Managing Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) — requests, limits, and how the scheduler and kubelet use them.
- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — the upstream how-to this lab's probes are based on.
- [ResourceQuotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) — the object behind every "exceeded quota" event you'll see today.
