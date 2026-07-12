---
title: Workshop Overview
---

Welcome back. In this workshop, part of **{{< param product_name >}}**, you'll learn the
core Kubernetes building blocks you use in every {{< param product_short >}} project —
by deploying a real application and taking it apart to see how it works.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

It helps to picture Kubernetes in four layers:

- **Infrastructure** — the cluster and its nodes (managed for you on {{< param product_short >}}).
- **Workloads** — your application: Deployments, ReplicaSets, Pods.
- **Networking** — how workloads are reached: Services (and, later, Routes).
- **Configuration & Storage** — settings and data (covered in later workshops).

This workshop lives mostly in the **Workloads** layer, with a first look at
**Networking** at the end. We don't just run commands — for each concept you'll learn
*what* it is, *why* it exists, and *how* it fits with the others.

## What You'll Learn

By the end you will be able to:

- Choose between [imperative and declarative](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/) resource management, and preview changes with `--dry-run`.
- Create and manage a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), and explain how it owns [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) and [Pods](https://kubernetes.io/docs/concepts/workloads/pods/).
- Use [labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) to identify and query resources.
- Inspect resources with `oc get`, `oc describe`, and `oc explain`.
- Scale a Deployment and watch Kubernetes **self-heal** a deleted Pod.
- Read logs and exec into a running container to debug.
- Give an application a stable address with a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and reach it in-cluster by DNS.

## Prerequisites

- **lab-a01-what-is-dcs** — you should be comfortable running `oc` and finding your project.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} project. The sample application image is served from the
{{< param product_short >}} Harbor registry.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Beginner → Intermediate
