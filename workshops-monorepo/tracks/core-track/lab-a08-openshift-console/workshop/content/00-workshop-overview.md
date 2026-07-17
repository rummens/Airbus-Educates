---
title: "The OpenShift Console — A Guided Tour"
---

You've done the whole Core happy path with `oc`. Here's the thing: **every one of those
actions has a visual equivalent** in the {{< param product_name >}} web console. This
closing lab tours it and maps each view back to the command you already know — so you can
switch between UI and CLI without missing a beat.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide).
{{< /note >}}

{{< warning >}}
**Rough draft.** The session **Console** tab is the [Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/),
usable as your session account. The full **OpenShift** web console can't be embedded in an
air-gapped session, so some of its views appear here as placeholder screenshots.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Navigate the [OpenShift web console](https://docs.openshift.com/container-platform/latest/web_console/web-console-overview.html) — perspectives, Workloads, Networking, Storage, Config.
- Map each console view to its `oc` equivalent (console ↔ CLI parity).
- Decide when the console is the faster tool and when the CLI wins.

## Prerequisites

- **A02 — Deploy Your First App** (A03–A05 helpful). This lab *locates* the objects you
  already know in the UI; it doesn't re-explain them.

## Time and Difficulty

- **Estimated time:** 15 minutes
- **Difficulty:** Beginner
