---
title: The Console
---

The **Console** tab is a visual, point-and-click view of your namespace — the
[Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).
When a lab has you create something from the terminal, you can flip here to *see* it:
Deployments, Pods, Services, and more, laid out visually instead of as command output.

## Open the Console on your namespace

Click below to switch to the Console tab and point it at your own project:

```dashboard:reload-dashboard
name: Console
url: {{< param ingress_protocol >}}://console-{{< param session_hostname >}}/#/workloads?namespace={{< param session_namespace >}}
```

It's **empty** right now — you haven't deployed anything yet. That's expected: from
**A02** onwards you'll deploy apps and come back here to watch them appear. For now, just
note that the tab exists and shows *your* namespace.

{{< note >}}
**This is not the OpenShift web console.** The Console tab is the generic Kubernetes
Dashboard, embedded read-mostly for a quick visual check. {{< param product_short >}} also
has the full **OpenShift web console**, which is a richer, separate tool — you get a
guided tour of it later in **A08: The OpenShift Console**.
{{< /note >}}

When you've had a look, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```
