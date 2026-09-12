---
title: Three Objects, One Image
---

A build on {{< param product_short >}} involves three objects. Keeping them apart is what
makes the error messages readable later.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/objects
```

![A BuildConfig is the recipe; each run creates a Build, which runs as a Pod and pushes the finished image to a registry; an ImageStream tracks that image by tag so workloads can reference it by name](build-objects.svg)

- **BuildConfig** is the **recipe**: where the input comes from, which strategy builds it,
  and where the output goes. You create it once.
- **Build** is **one run** of that recipe. It runs as a Pod, it has logs, it succeeds or
  fails, and it stays afterwards as the record. Every rebuild is a new Build.
- **ImageStream** is a **name for the result**. It tracks image tags inside the cluster, so a
  Deployment can say `hello-built:latest` instead of a registry URL with a digest.

## Two strategies worth knowing

- **Docker strategy:** you provide a `Containerfile` (a Dockerfile) and the build runs it.
  You control everything that goes into the image, and you are responsible for all of it.
- **Source strategy (S2I):** you provide *source code only*, and a platform-supplied builder
  image compiles it into a runnable image. There is no Containerfile.

S2I is less work when your language has a supported builder. This lab uses the Docker
strategy because it makes every step visible.

## Where the input comes from

Two sources, and the distinction matters on an air-gapped platform:

- **Git:** the BuildConfig points at a repository, and a push can trigger a rebuild. On
  {{< param product_short >}} that repository is one the platform can reach, which means your
  tenant's in-cluster GitLab rather than github.com.
- **Binary:** you hand the files to the build yourself, from wherever you are standing.

This lab uses a **binary** build because it needs nothing outside your session. Everything
else about the object is the same.

{{< warning >}}
**⚠️ Watch out:** a build is not free. It runs as a Pod in your namespace and spends your
budget while it runs, and the first build of a large base image is slow. The arithmetic from
**Health & Resources** applies here too.
{{< /warning >}}

Next: build something.
