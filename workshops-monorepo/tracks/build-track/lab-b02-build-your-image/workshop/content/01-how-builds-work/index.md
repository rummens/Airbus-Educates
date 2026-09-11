---
title: Three Objects, One Image
---

A build on {{< param product_short >}} involves three objects, and keeping them straight makes
every later error message readable.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/objects
```

![A BuildConfig is the recipe; each run creates a Build, which runs as a Pod and pushes the finished image to a registry; an ImageStream tracks that image by tag so workloads can reference it by name](build-objects.svg)

- **BuildConfig** — the **recipe**. Where the input comes from, which strategy builds it, and
  where the output goes. You create it once.
- **Build** — **one run** of that recipe. It runs as a Pod, it has logs, it succeeds or fails,
  and it stays afterwards as the record. Every rebuild is a new Build.
- **ImageStream** — a **name for the result**. It tracks image tags inside the cluster, so a
  Deployment can say `hello-built:latest` instead of a registry URL with a digest.

## Two strategies worth knowing

- **Docker strategy** — you provide a `Containerfile` (a Dockerfile), and the build runs it.
  Total control, and total responsibility for what goes in the image.
- **Source strategy (S2I)** — you provide *source code only*, and a platform-supplied builder
  image compiles it into a runnable image. No Containerfile at all.

S2I is the tidier path when your language has a supported builder; this lab uses the Docker
strategy, because it makes every step visible.

## Where the input comes from

Two sources, and the distinction matters on an air-gapped platform:

- **Git** — the BuildConfig points at a repository, and a rebuild can be triggered by a push.
  On {{< param product_short >}} that repository is one the platform can reach: your tenant's
  in-cluster GitLab, not github.com.
- **Binary** — you hand the files to the build yourself, from wherever you are standing.

This lab uses a **binary** build, because it needs nothing outside your session. The object
you create is otherwise identical, which is the point.

{{< warning >}}
**⚠️ Watch out:** a build is not free. It runs as a Pod in your namespace, draws on your
budget, and a build that pulls a large base image is slow the first time. The **Health &
Resources** lab's arithmetic applies here too.
{{< /warning >}}

Next: build something.
