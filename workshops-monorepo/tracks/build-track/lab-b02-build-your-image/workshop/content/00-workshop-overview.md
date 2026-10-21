---
title: "Build Your Image on DCS"
---

In this lab you build your own image.

There is **no Docker daemon** on **{{< param product_name >}}**, on the cluster or in this
session. Building an image the usual way needs privileged access to a host, and a shared
platform does not hand that out.

So the platform builds it **for** you, inside the cluster, from a
[**BuildConfig**]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/buildconfig-and-imagestreams/).

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain what a **BuildConfig**, a **Build** and an **ImageStream** each are, and how they relate.
- Build an image on the cluster from files in your session — no daemon, no privileged tooling.
- Read a build log, and tell a build failure from a deploy failure.
- Deploy an image by its **ImageStream tag** instead of a registry URL.
- Say what triggers a rebuild on a real project, and where the image goes on {{< param product_short >}}.

## Prerequisites

- **From Docker to Kubernetes**, so you know why the Docker workflow does not transfer and
  what the restricted SCC means for an image.
- The Core lab **Deploy Your First App**.

{{< note >}}
**📌 Note:** your session is entitled to create builds in **your own namespace**. That is a
grant like every other permission on this platform, and a namespace without it cannot build.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with `oc`.

The build's output goes to the **cluster's own registry**. On {{< param product_short >}} it
goes to your tenant's Harbor project instead, and the last page covers what changes with it.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Understanding BuildConfigs]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/buildconfig-and-imagestreams/) — the object, its strategies and its triggers.
- [Managing image streams]({{< param dcs_docs_base_url >}}/services/namespace_aas/concepts/buildconfig-and-imagestreams/) — what an ImageStream tracks, and why you reference it instead of a URL.
