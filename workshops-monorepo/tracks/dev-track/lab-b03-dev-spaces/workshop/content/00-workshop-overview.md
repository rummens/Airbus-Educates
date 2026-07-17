---
title: "Cloud Development with OpenShift Dev Spaces"
---

Welcome to this workshop, part of **{{< param product_name >}}**. So far you've
deployed a ready-made image straight to your namespace (A02, reinforced in **From
Docker to Kubernetes on DCS**), and connected git as a **build source** so the
cluster turns your code into an image (**Building Images with BuildConfigs**). Neither
of those lets you edit and run your code *while it's inside the cluster*. This
workshop closes that gap, and answers one question: **how do I develop *on*
{{< param product_short >}}, not just deploy to it?**

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain what OpenShift Dev Spaces is (a browser-based, in-cluster IDE, built on
  upstream Eclipse Che) and why it fits an air-gapped, regulated platform like DCS.
- Read a `devfile.yaml` and identify its dev image, its source, and its run command.
- Walk through launching a workspace from a devfile and making a code change run
  **inside the cluster**, not on your laptop.
- Place Dev Spaces correctly among the Educates editor (this workshop), a
  BuildConfig (code → image), and `oc apply` (deploy) — same git, three different jobs.

## Prerequisites

This workshop assumes you've completed **From Docker to Kubernetes on DCS**
(`lab-b01-docker-to-k8s`) and are comfortable with `oc apply`-style deployment and
basic [git](https://git-scm.com/doc) usage. It builds directly on **Building
Images with BuildConfigs** (`lab-b02-image-buildconfigs`) for contrast, but does not
require you to have completed it first.

## Your Environment

A browser-based session with a **terminal**, an **editor**, and a
Kubernetes/OpenShift **console**, pointed at your own namespace. All commands run
with `oc`. Partway through the workshop a **Dev Spaces** tab is added to your
dashboard, pointing at the platform's Dev Spaces instance.

## Time and Difficulty

- **Estimated time:** 18 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Eclipse Che documentation](https://eclipse.dev/che/docs/stable/overview/introduction-to-eclipse-che/)
- [Red Hat OpenShift Dev Spaces](https://developers.redhat.com/products/openshift-dev-spaces/overview)
- [The Devfile specification](https://devfile.io/docs/2.2.0/what-is-a-devfile)
