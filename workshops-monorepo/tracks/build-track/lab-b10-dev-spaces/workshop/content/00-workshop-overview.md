---
title: "Dev Spaces"
---

So far this track has deployed a ready-made image into your namespace
(**Deploy Your First App**, then **From Docker to Kubernetes**) and used your files as a
**build source** so the cluster turns them into an image (**Build Your Image on DCS**).

Neither lets you edit code and run it while it is inside the cluster. This lab covers the
tool that does: **OpenShift Dev Spaces**.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain what OpenShift Dev Spaces is (a browser-based, in-cluster IDE, built on
  upstream Eclipse Che) and why it fits an air-gapped, regulated platform like DCS.
- Read a `devfile.yaml` and identify its dev image, its source, and its run command.
- Walk through launching a workspace from a devfile and making a code change run
  **inside the cluster**, not on your laptop.
- Place Dev Spaces correctly among the Educates editor (this workshop), a
  BuildConfig (code → image), and `oc apply` (deploy), which all use the same git repository for different jobs.

## Prerequisites

This lab assumes **From Docker to Kubernetes** (`lab-b01-docker-to-k8s`), comfort with
`oc apply`, and basic [git](https://git-scm.com/doc) usage. It contrasts itself with
**Build Your Image on DCS** (`lab-b02-build-your-image`), which you do not have to have done
first.

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
