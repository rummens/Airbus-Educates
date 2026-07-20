---
title: "What is DCS?"
---

Welcome to this workshop, part of **{{< param product_name >}}**. In it you will get
oriented on {{< param product_short >}} — what the platform is, how containers and
images fit, and how to work in your environment using the `oc` command line.

This is a **concept/orientation lab** — take it any time; it assumes **no prior container
or Kubernetes knowledge**. If you'd rather start by *doing*, jump into **Deploy Your First
App** and come back here for the background.

{{< note >}}
Prefer it visual? Open the **Slides** tab for a low-text overview of everything on these
pages.
{{< /note >}}

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Explain what {{< param product_short >}} is and where it fits.
- Describe the {{< param product_short >}} **cluster model** — Sandbox and PROD — and the one thing that separates them.
- Describe containers and images at a high level.
- Say why Kubernetes beats plain Docker for running applications.
- Navigate your session environment (terminal and editor).
- Run your first [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) commands and confirm your access.

## Prerequisites

None. Curiosity about [containers](https://kubernetes.io/docs/concepts/containers/) is
enough — we introduce everything you need.

{{< note >}}
**New to the command line or containers?** This track goes best if you're comfortable
with **basic Linux/terminal use** (running a command, reading its output, editing a file)
and know **a little about containers** (what an image is versus a running container). You
don't need to be an expert, and nothing here is blocking — but if it's all new, a short
primer first makes everything click faster:

- [Container Intro — high-level, non-technical](https://drive.google.com/file/d/1HU2t-a4gNn9e_S_rzduL1Y4H59KWP7O-/view?t=2820.945): what containers are and why they matter.
- [Container 101 — technical](https://drive.google.com/file/d/1RINpBVe2g6js4K5vtW0QbijzTB1P_RVI/view?usp=sharing): images, containers, and the basics.
- [OpenShift 101 — technical](https://drive.google.com/file/d/11Th5tteTjsNecWdWextEcmac0wparVhE/view?usp=sharing): how OpenShift runs those containers.

A dedicated **Theory track** covering this ground in depth is planned for the future.
{{< /note >}}

## Your Environment

This session is a browser-based environment with an embedded **terminal** and a **code
editor**. You already have access to your own
{{< param product_short >}} project, scoped just to you. All commands are run with
`oc` in the terminal — no installation or login required.

## Time and Difficulty

- **Estimated time:** 15 minutes
- **Difficulty:** Beginner
