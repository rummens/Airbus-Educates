---
title: The Console
---

The **Console** tab is a visual, point-and-click view of your **namespace** — the
[Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).

When a lab has you create something from the terminal, you can switch here to *see* it:
**Deployments**, **Pods**, **Services** and more, laid out visually instead of as command
output.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/console
```

## Open the Console on your namespace

Click below to switch to the Console tab and point it at your own project:

```dashboard:reload-dashboard
name: Console
url: {{< param ingress_protocol >}}://console-{{< param session_hostname >}}/#/workloads?namespace={{< param session_namespace >}}
```

It is **empty** right now — you have not deployed anything yet.

From **Deploy Your First App** onwards you deploy apps and come back here to watch them
appear.

It may also show a warning or two about resources it is not allowed to list. That is the
dashboard reaching the edge of your **namespace-scoped** permissions, not a problem with
your session.

{{< note >}}
**📌 Not the OpenShift web console.** The real OpenShift console can't be embedded in a tab
like this, so labs use the Kubernetes Dashboard for a quick visual check. The OpenShift
console is a separate tool you open in its own browser tab — the **Console track** tours it.
{{< /note >}}

When you've had a look, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```
