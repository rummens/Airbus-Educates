---
title: "Deploy Your First App"
---

The quick win, and the entry point to the course: you'll get your own app running on
**{{< param product_name >}}** in a few minutes — then look under the hood to see how it
works. No theory first; if you want the background on *what DCS is* and *why Kubernetes*,
that's the **What is DCS?** lab, any time.

You'll deploy a small sample called **hello-dcs**: a tiny web server that listens on port
8080 and prints a greeting. Its image already lives in the {{< param product_short >}}
[Harbor](https://goharbor.io/) registry (`{{< param dcs_registry >}}`), pulled from
inside the platform — nothing comes from the public internet. More on the registry in the
[{{< param product_short >}} registry docs]({{< param dcs_docs_base_url >}}/services/container-registry).

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Deploy a Harbor image with [`oc create deployment`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/developer_cli_commands.html).
- Customise the running app with an environment variable (`oc set env`).
- Reach the app locally with [`oc port-forward`](https://docs.openshift.com/container-platform/latest/nodes/containers/nodes-containers-port-forwarding.html) and `curl`.
- Change config and watch the [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) roll out a new version.
- Read the generated YAML and explain the Deployment → ReplicaSet → Pod chain.

## Prerequisites

- **None** — this is the hands-on entry point. Comfort with a terminal helps. New to
  containers or `oc`? The **What is DCS?** lab gives the background, but isn't required first.

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

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Beginner
