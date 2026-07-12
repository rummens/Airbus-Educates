---
title: Overview
---

Welcome to **Configuration & Secrets** on **{{< param product_name >}}**.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

In B01 you deployed `hello-dcs` — but its settings were baked into the image and manifest. To
change a value you'd have to rebuild. That doesn't scale: the same image should run in dev and
prod with **different config**, and credentials must never live in an image. In this workshop
you pull configuration out into a **ConfigMap**, inject a credential with a **Secret**, and roll
out a config change without touching the image.

## What You'll Do

- Move settings into a **ConfigMap** and deliver them as env vars **and** a mounted file.
- Store a credential in a **Secret** and inject it — without leaking the value.
- Change a config value and **roll it out**, watching old Pods give way to new.

## Before You Start

- **Prerequisites:** B01 (Deploy Your First App).
- **Difficulty:** intermediate · **Time:** ~35 minutes.
- **Your app:** the `hello-dcs` Deployment + Service are already running here.

Open the ConfigMap you'll apply first:

```editor:open-file
file: ~/exercises/configmap.yaml
```
