---
title: Overview
---

Welcome to **Scaling, Health & Resources** on **{{< param product_name >}}**.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

Your `hello-dcs` app is already deployed and running — one replica, no health checks, modest
resources. That's fine for a demo, but not for something people rely on. In this workshop you
make it **resilient** and **quota-friendly**: you scale it, discover that your namespace has a
real resource **budget**, right-size the app to fit, and add **probes** so the platform knows
when it's healthy.

## What You'll Do

- Scale the Deployment and see how replica count meets your namespace **quota**.
- Ask for too much on purpose, watch the quota **reject** it, and read the events.
- **Right-size** requests and limits to fit the budget.
- Add **readiness** and **liveness** probes and see how each changes behaviour.

## Before You Start

- **Prerequisites:** B01 (Deploy Your First App). You should be comfortable with `oc apply`,
  `oc scale`, and reading Pods with `oc get`.
- **Difficulty:** intermediate · **Time:** ~40 minutes.
- **Your app:** the `hello-dcs` Deployment + Service are already running here.

Open the manifest you'll grow into a production-ready one:

```editor:open-file
file: ~/exercises/deployment-probes.yaml
```

When you're ready, move to the next page.

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
