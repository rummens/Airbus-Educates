---
title: "From Docker to Kubernetes on DCS"
---

Welcome to this workshop, part of **{{< param product_name >}}**. If you already run
containers with `docker run` or `docker compose up`, you don't need to unlearn any of
that — Kubernetes just gives the same ideas different names and a declarative shape. This
lab takes a small docker-compose file for the `hello-dcs` sample and migrates it, piece by
piece, into the Deployment, Service and ConfigMap you'd use on {{< param product_short >}}.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Map `docker run` / docker-compose concepts to their Kubernetes equivalents — container
  → Pod/Deployment, `-p`/`ports` → Service, `-e`/`environment` → ConfigMap, `-v` → Volume.
- Turn a docker-compose service definition into an equivalent Deployment + Service +
  ConfigMap, and deploy it.
- Identify what does **not** translate on DCS and why: `privileged`/host mounts, the
  `latest` tag, running as root, and images from outside Harbor.
- Confirm the migrated app runs "the Kubernetes way" — self-healing, declarative, reachable
  by a stable name.

## Prerequisites

- **A01 — Deploy Your First App.** You know Deployments, Pods, and the
  Deployment → ReplicaSet → Pod chain.
- **A02 — Configure & Troubleshoot Your App.** You know ConfigMaps and how a config
  change triggers a rollout.
- Comfort reading a `docker run` command or a `docker-compose.yml` file — this lab assumes
  that background rather than teaching it.

This lab does **not** re-teach what a Deployment, Service or ConfigMap *is* — A01/A02
already covered that. It's about the *mapping* from the Docker world onto those objects,
and the constraints DCS adds along the way.

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace, plus a **console** tab so you can watch the Deployment, Pod and Service land as
you apply each manifest. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/) — the object model this lab maps onto.
- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/) — the source format you're migrating from.
