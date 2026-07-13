---
title: Workshop Overview
---

In this workshop, part of **{{< param product_name >}}**, you'll meet the two kinds of
namespace {{< param product_short >}} gives you — **DEV** and **PROD** — and see, side by
side, exactly how they differ and how your work moves from one to the other.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, and the clickable actions you'll use here.
{{< /note >}}

On {{< param product_short >}}, a namespace is the unit you consume — this is
**Namespace as a Service**. Every namespace is either a **DEV** or a **PROD** type, and
they are deliberately not the same: PROD is guarded so that what runs in production is
controlled and repeatable. You'll create both types in your own virtual cluster and feel
the difference first-hand.

## What You'll Learn

By the end you will be able to:

- Explain **Namespace as a Service (NaaS)** — why the namespace is the {{< param product_short >}} consumption unit.
- Distinguish the **DEV** and **PROD** namespace lifecycle types and the controls that differ.
- Deploy a workload into a DEV namespace.
- See how a **PROD** namespace enforces stricter policy (Kyverno) and rejects a non-compliant change.
- Explain **promotion** — why you move work DEV → PROD rather than editing PROD in place.

## Prerequisites

- **lab-a02-kubernetes-essentials** — you should be comfortable applying a Deployment and inspecting it with `oc`.

## Your Environment

A **split terminal**, an editor, the web console, and — unique to this lab — your own
**virtual cluster**, which gives you cluster-admin so you can create real namespaces and
policies without touching anyone else's work. The sample image is served from the
{{< param product_short >}} Harbor registry.

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
