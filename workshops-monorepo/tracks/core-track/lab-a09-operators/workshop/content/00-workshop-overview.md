---
title: Workshop Overview
---

In this workshop, part of **{{< param product_name >}}**, you'll meet **Operators** — the
pattern behind the platform services {{< param product_short >}} offers — and learn the one
thing about them that trips people up most: who owns what.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, and the clickable actions you'll use here.
{{< /note >}}

You already know built-in resources like Deployments and Services. Operators extend
Kubernetes with *new* resource types that represent whole applications — a database, a Git
server — and a controller that runs them for you. On {{< param product_short >}} these are
offered as **operators, not managed services**, which changes who is responsible for the
running instance. That distinction is the heart of this lab.

## What You'll Learn

By the end you will be able to:

- Explain the **Operator pattern**: a controller reconciling a Custom Resource toward its desired state.
- Distinguish a **CRD** (a new resource *type*) from a **CR** (an *instance*).
- Explain **OLM** and **OperatorHub** at a high level.
- Create a Custom Resource and watch the operator reconcile it.
- State the **DCS ownership model**: the platform owns the operator; **you** own the instance it manages.

## Prerequisites

- **lab-a02-kubernetes-essentials** — you should be comfortable applying manifests and inspecting resources with `oc`.

## Your Environment

A **split terminal**, an editor, the web console, and your own {{< param product_short >}}
namespace. A lightweight operator (CloudNativePG) is pre-installed by the platform; you'll
create an instance of it. Operand images come from the {{< param product_short >}} Harbor
registry.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Beginner

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
