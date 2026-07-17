---
title: "Building Images with BuildConfigs"
---

Welcome to this workshop, part of **{{< param product_name >}}**. Every lab so far
deployed an image someone else already built. This one answers a different question:
**how do I get *my own* code into an image, on an air-gapped platform, with no Docker
installed on my laptop?** You'll point a BuildConfig at a git repository, let
{{< param product_short >}} build the image on-cluster, push it to Harbor, and deploy it.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain how DCS builds images **on the cluster** — a BuildConfig and a Build Pod — instead of on a laptop.
- Connect a git repository as a **build source** and choose between the **S2I** and **Dockerfile** strategies.
- Build an image and watch it land in Harbor.
- Deploy the image you just built, using the Deployment skills from earlier labs.
- Trigger a rebuild and confirm a fresh image replaces the old one.

## Prerequisites

- **B01 — From Docker to Kubernetes on DCS.** You know Deployments, and how to apply a
  manifest with `envsubst < file.yaml | oc apply -f -` when it references
  `${DCS_REGISTRY}`.
- Comfort reading a [YAML](https://kubernetes.io/docs/concepts/configuration/overview/) manifest — this lab reuses, rather than re-teaches, the Deployment shape from A02/B01.

This lab does **not** re-teach how to write or apply a Deployment, or how to reach a
Service — B01 already covered that. It's about the *build* step that produces the image
those manifests reference.

## Your Environment

A browser-based session with a split **terminal**, an **editor**, and a **console** tab
so you can watch the Build Pod and the resulting Deployment/Pod land as each step
completes. All commands run with `oc`. Take a first look at the BuildConfig you'll run:

```editor:open-file
file: ~/exercises/buildconfig-s2i.yaml
```

## Time and Difficulty

- **Estimated time:** 45 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Understanding image builds](https://docs.openshift.com/container-platform/latest/cicd/builds/understanding-image-builds.html) — the OpenShift Builds concept this lab is built on.
- [Source-to-Image (S2I) build](https://docs.openshift.com/container-platform/latest/cicd/builds/build-strategies.html) — the strategy this lab runs.
