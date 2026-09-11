---
title: "From Docker to Kubernetes"
---

If you run containers today with `docker run` or `docker compose up`, none of that
knowledge is wasted on **{{< param product_name >}}**.

Kubernetes gives the same ideas different names and a **declarative** shape. This lab takes
a small `docker-compose.yml` for the `hello-dcs` sample and migrates it, piece by piece,
into the **Deployment**, **Service** and **ConfigMap** you would use on
{{< param product_short >}}.

Then it shows you the lines that do not survive the trip, and why the platform refuses them.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Map compose concepts to Kubernetes objects — container → [Pod](https://kubernetes.io/docs/concepts/workloads/pods/)/[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), `ports:` → [Service](https://kubernetes.io/docs/concepts/services-networking/service/), `environment:` → [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/), `volumes:` → [Volume](https://kubernetes.io/docs/concepts/storage/volumes/).
- Explain the difference between an **imperative** `docker run` and a **declarative** Deployment.
- Turn a compose service into a working Deployment, Service and ConfigMap on {{< param product_short >}}.
- Name the four compose lines {{< param product_short >}} rejects, and the control behind each.

## Prerequisites

- The Core labs **Deploy Your First App** and **Configure & Troubleshoot Your App** — you
  know what a Deployment, Service and ConfigMap *are*, and how a config change rolls out.
- Comfort reading a `docker run` command or a `docker-compose.yml` file. This lab assumes
  that background rather than teaching it.

This lab does **not** re-teach those objects. It teaches the **mapping** onto them, and the
constraints {{< param product_short >}} adds along the way.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. Everything you need is created here,
in your own namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/) — the object model this lab maps onto.
- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/) — the source format you are migrating from.
