---
title: "Build Your Image on DCS"
---

Every lab so far ran an image somebody else built. This one builds yours.

There is **no Docker daemon** on **{{< param product_name >}}** — not on the cluster, and not
in this session. Building a container image the usual way needs privileged access to a host,
which is precisely what a shared platform will not give you.

So the platform builds it **for** you, inside the cluster, from a
[**BuildConfig**](https://docs.openshift.com/container-platform/latest/cicd/builds/understanding-buildconfigs.html).

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

- **From Docker to Kubernetes** — you know why the Docker workflow does not transfer, and what
  the restricted SCC means for an image.
- The Core lab **Deploy Your First App**.

{{< note >}}
**📌 Note:** your session is entitled to create builds in **your own namespace**. That is a
grant, like every other permission on this platform — a namespace without it cannot build.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with `oc`.

The build's output goes to the **cluster's own registry**. On {{< param product_short >}} it
goes to your tenant's Harbor project instead — the last page covers what changes and what does
not.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Understanding BuildConfigs](https://docs.openshift.com/container-platform/latest/cicd/builds/understanding-buildconfigs.html) — the object, its strategies and its triggers.
- [Managing image streams](https://docs.openshift.com/container-platform/latest/openshift_images/image-streams-manage.html) — what an ImageStream tracks, and why you reference it rather than a URL.
