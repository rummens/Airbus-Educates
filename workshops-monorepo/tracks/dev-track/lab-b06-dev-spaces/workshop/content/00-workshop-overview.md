---
title: Overview
---

Welcome to **Cloud Development with OpenShift Dev Spaces** on **{{< param product_name >}}**.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

So far you've **deployed to** {{< param product_short >}}. This workshop is about developing
**on** it. **OpenShift Dev Spaces** gives every developer a consistent, browser-based IDE that
runs *inside* the cluster — no laptop toolchain, no reaching out to the internet, fully
policy-compliant on an air-gapped platform.

## What You'll Do

- Explain what Dev Spaces is and why it fits an air-gapped platform.
- Read a **devfile** — the reproducible spec for a workspace — that points at the sample app.
- Launch (or tour) a workspace and run the app **inside the cluster**.
- Place Dev Spaces next to the Educates editor and a plain `oc apply` deploy.

## Before You Start

- **Prerequisites:** B01 (Deploy Your First App); A09 (Operators) for the "platform installs
  it, you use it" idea.
- **Difficulty:** intermediate · **Time:** ~45 minutes.

{{< note >}}
**Live vs concept:** if this cluster has a Dev Spaces instance and a Harbor-mirrored image,
you'll launch a real workspace. If not, the same steps are a guided, screenshot-driven tour —
the devfile and the concepts are identical either way.
{{< /note >}}

Open the workspace definition you'll use:

```editor:open-file
file: ~/exercises/devfile.yaml
```

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
