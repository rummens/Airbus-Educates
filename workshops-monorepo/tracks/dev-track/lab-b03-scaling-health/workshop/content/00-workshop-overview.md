---
title: Overview
---

Welcome to **Scaling, Health & Resources** on **{{< param product_name >}}**.

{{< note >}}
**First time in a workshop?** The panel on the left is the instructions; the panel on the
right is your live environment (a terminal, an editor, and the OpenShift web console).
Clickable code blocks run commands or open files for you — you don't have to type. Work
top to bottom.
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
