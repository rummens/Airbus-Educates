---
title: Launch a Workspace
---

Time to open the environment the devfile describes.

{{< note >}}
**Live vs concept.** If your session has a **Dev Spaces** tab, follow the live steps. If not,
this cluster has no Dev Spaces instance — read the steps as an annotated tour; the flow is the
same, and you'll answer a knowledge check instead of the live one.
{{< /note >}}

## Live: open the workspace

Open the **Dev Spaces** dashboard tab, then create a workspace from the sample app's devfile
(the dashboard's "Create Workspace" → from devfile / Git URL flow). Dev Spaces reads the
devfile, pulls the Harbor UDI, and starts your IDE Pods.

While it starts, watch it from the Educates terminal:

```terminal:execute
command: oc get pods -l controller.devfile.io/devworkspace_name
```

Expected: a workspace Pod moves through `Pending` → `Running` as the IDE comes up. Confirm:

```examiner:execute-test
name: verify-workspace
title: (Live) A Dev Spaces workspace is Running
timeout: 10
retries: 6
delay: 5
```

## Concept: what you'd see

The Dev Spaces dashboard lists your workspaces; "Create Workspace" from the devfile spins up an
IDE in the browser within a minute — an editor, a file tree of the cloned source, and a
terminal, all running as Pods in your namespace. No local install, no downloads.

## Check Your Understanding

Where does the workspace's tools image come from, and why does that matter on
{{< param product_short >}}?

{{< note >}}
**Answer:** From **Harbor**, via `${DCS_REGISTRY}` in the devfile. On an air-gapped platform
the cluster can't pull from public registries, so the UDI must be mirrored into Harbor first.
{{< /note >}}
