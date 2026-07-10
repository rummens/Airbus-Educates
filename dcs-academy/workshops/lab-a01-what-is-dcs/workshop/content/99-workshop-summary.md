---
title: Summary
---

You're oriented on **{{< param product_name >}}**. You now know what the platform is,
how containers differ from virtual machines, and how to work in your environment with
`oc`.

## What You Did

- Learned what {{< param product_short >}} is: an on-prem, air-gapped, OpenShift-based
  Namespace as a Service platform.
- Saw how containers and images relate.
- Confirmed your identity, cluster access, and project with `oc`.
- Explored the web console.

## Check Your Understanding

1. What makes {{< param product_short >}} **air-gapped**, and what does that mean for where images come from?

{{< note >}}
**Answer:** {{< param product_short >}} runs on-premises with no internet access from
workloads. All images are provided from within the platform (the Harbor registry) — you
can't pull from public registries.
{{< /note >}}

2. What is the difference between a container **image** and a **container**?

{{< note >}}
**Answer:** The image is the blueprint (a packaged, read-only template); the container
is a running instance of that image.
{{< /note >}}

3. Which command shows the project you are currently working in?

{{< note >}}
**Answer:** `oc project -q`. Your project name is also in `$SESSION_NAMESPACE`.
{{< /note >}}

## Next Steps

Continue with **Kubernetes Essentials on DCS**, where you'll deploy your first
application and expose it — using the [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
skills you just practised.
