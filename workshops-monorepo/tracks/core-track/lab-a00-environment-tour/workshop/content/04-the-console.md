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
**A01** onwards you'll deploy apps and come back here to watch them appear. For now, just
note that the tab exists and shows *your* namespace.

{{< note >}}
**This is not the OpenShift web console — and here's why.** The full OpenShift console
refuses to be embedded in another page (it sends a `frame-ancestors: 'none'` header, so a
browser won't render it inside this dashboard's tab), and it wouldn't share your session
login anyway. So the in-session Console tab is the generic **Kubernetes Dashboard**, which
*does* embed and runs as your session account — enough for a quick visual check.
{{< param product_short >}}'s richer **OpenShift web console** is a separate tool you open
in its own browser tab; you get a guided tour of it in **A08: The OpenShift Console**.
{{< /note >}}

When you've had a look, switch back to the terminal:

```dashboard:open-dashboard
name: Terminal
```
