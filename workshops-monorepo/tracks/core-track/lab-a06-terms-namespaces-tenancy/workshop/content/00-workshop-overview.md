---
title: Workshop Overview
---

Everything you've deployed so far lived *somewhere* — a place that isolated it, held its
objects, and had a name you kept seeing in prompts and commands. This workshop, part of
**{{< param product_name >}}**, names that place: the **Namespace**. Then it makes
isolation concrete — you'll run the *same* app in two namespaces at once and watch them
stay completely out of each other's way.

This is vocabulary plus a hands-on demo, not the deep governance model — that lands later
in the Developer track.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Define a [**Namespace**](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) — the unit of isolation and consumption on {{< param product_short >}} — and say what makes one the *active* namespace.
- **See isolation for real**: deploy the same app into two namespaces and observe that identical names coexist and actions don't leak.
- List concrete reasons a tenant splits workloads across multiple namespaces.
- Explain the **Tenant → Namespaces** model (and why there is no separate "project" layer).
- State that **DEV** and **PROD** namespace types exist and differ.

## Prerequisites

- **A02 — Deploy Your First App.** You should be comfortable running `oc` and deploying a workload. This lab reuses that skill; it doesn't re-teach it.

## Your Environment

A browser-based session with a split **terminal** and an **editor**. Two extra
namespaces have already been created for you (`app-a` and `app-b`) — you'll use them in
the isolation demo. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Beginner
