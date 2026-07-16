---
title: Workshop Overview
---

Time for the payoff. In A01 you learned what **{{< param product_name >}}** is and *why*
Kubernetes runs your apps the way it does. Now you'll get your own app running on it — in
a few minutes — and then look under the hood to see how it works.

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

- **A01 — What is DCS?** You should be able to run `oc` and find your namespace.

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 30 minutes
- **Difficulty:** Beginner
