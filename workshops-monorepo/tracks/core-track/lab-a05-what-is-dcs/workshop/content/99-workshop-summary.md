---
title: Summary
---

You're oriented on **{{< param product_name >}}**. You now know what the platform is,
how it's delivered as Sandbox and PROD clusters, how containers differ from virtual
machines, why Kubernetes beats plain Docker, and how to work in your session with `oc`.

## What You Did

- Learned what {{< param product_short >}} is: an on-prem, air-gapped, OpenShift-based
  Namespace as a Service platform.
- Saw the {{< param product_short >}} cluster model — Sandbox and PROD — and that the
  only difference is feature-rollout timing and maintenance notice/SLA.
- Saw how containers and images relate.
- Learned why Kubernetes adds scheduling, self-healing, scaling, and declarative
  desired-state over plain Docker.
- Confirmed your identity, cluster access, and project with `oc`.

## Check Your Understanding

1. What makes {{< param product_short >}} **air-gapped**, and what does that mean for where images come from?

{{< note >}}
**Answer:** {{< param product_short >}} runs on-premises with no internet access from
workloads. All images are provided from within the platform (the Harbor registry) — you
can't pull from public registries.
{{< /note >}}

2. What is the **one real difference** between the Sandbox and PROD clusters?

{{< note >}}
**Answer:** Feature-rollout timing and maintenance notice/SLA. New platform features
reach Sandbox first and PROD about a month later; Sandbox announces maintenance
shorter-term (slightly lower SLA), PROD with longer notice (higher SLA). Otherwise the
two clusters are identical — same platform, same capabilities.
{{< /note >}}

3. What is the difference between a container **image** and a **container**?

{{< note >}}
**Answer:** The image is the blueprint (a packaged, read-only built artifact); the
container is a running instance of that image.
{{< /note >}}

4. Name **one thing Kubernetes gives you that plain Docker doesn't**.

{{< note >}}
**Answer:** Any of: scheduling (the platform picks where a workload runs), self-healing
(crashed containers are restarted/rescheduled automatically), scaling (ask for N replicas
up or down), or declarative desired-state (you describe the target and the platform
continuously reconciles to it, versus a one-shot `docker run`).
{{< /note >}}

## Next Steps

If you haven't already, do **Deploy Your First App** — it gets an application running on
{{< param product_short >}} in minutes using the [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
skills you just practised. From here the orientation labs (**Terms**, the **ITSM console**,
the **OpenShift console**) round out the picture.
