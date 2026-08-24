---
title: See It in the Session
---

The Route is the real external address. For convenience while you work, you can also pin
the running app as a **dashboard tab** here in the session, served through the Educates
session proxy.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/app-tab
```

## Open the app as a tab

This creates an **App** tab pointing at the in-session proxied endpoint for your Service:

```dashboard:create-dashboard
name: App
url: {{< param ingress_protocol >}}://app-{{< param session_hostname >}}
```

You should see the hello-dcs page — its greeting and the URL it's serving on. Switch to it
any time:

```dashboard:open-dashboard
name: App
```

{{< note >}}
**📌 Two ways to reach the same app.** The **session proxy** (this tab) is an HTTPS,
auth-gated endpoint for use inside your session. The **Route** from the last page is the
real, external URL anyone can reach from outside. Same app, two separate entry points.
{{< /note >}}

When you're ready to run more commands, switch back to the terminal (the next steps type
there):

```dashboard:open-dashboard
name: Terminal
```
