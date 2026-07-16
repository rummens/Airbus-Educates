---
title: Containers and Images
---

Everything you run on {{< param product_short >}} runs in a **container**. Before you
deploy anything, it's worth a minute on what that actually means — and how it differs
from the virtual machines you may already know.

## From Virtual Machines to Containers

Think of a **virtual machine** like a private house: it brings its own foundation,
plumbing, and walls — a full operating system — which is powerful but heavy. A
[container](https://kubernetes.io/docs/concepts/containers/) is more like an apartment
in a modern building: it carries only what your application needs and shares the
building's infrastructure. Containers start in seconds, are lightweight, and run the
same way everywhere.

## Image vs Container

Two words that are easy to mix up:

- An [image](https://kubernetes.io/docs/concepts/containers/images/) is the **built
  artifact** — a packaged, read-only template of your application and everything it
  needs to run. Think of it as the blueprint.
- A **container** is a **running instance** of that image. One image can start many
  containers, the same way one blueprint can build many identical apartments.

You build an image once, then run it as a container wherever you need it.

![One image, many running containers](image-vs-container.svg)

## Where DCS images come from

Because {{< param product_short >}} is air-gapped, images don't come from the public
internet. They live in the platform's own registry (Harbor, at `{{< param dcs_registry >}}`),
and in Foundations you **pull** from it — you don't push. That's all you need for now;
the registry gets a workshop of its own later in the course.

## Next

Next: if a container just runs on one machine, why do we need Kubernetes at all?
