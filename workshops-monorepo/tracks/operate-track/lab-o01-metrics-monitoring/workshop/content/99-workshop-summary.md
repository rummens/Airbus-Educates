---
title: Summary
---

Your app now says what it is doing, the platform collects it, and you can ask for it back —
but only about your own namespace.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Separated** the metrics the platform gives you from the ones only your app can produce.
2. **Read** the exposition format your app serves on `/metrics`, and made its counter move.
3. **Created** a ServiceMonitor — and checked its selector actually matches, because nothing
   would have told you otherwise.
4. **Queried** your own series through the platform's tenant endpoint, then asked a real
   question with `rate()` and `sum by`.
5. **Were refused** when asking about another namespace.

## Check Your Understanding

1. Your ServiceMonitor exists, the app is healthy, and no data ever appears. What do you check
   first?

{{< note >}}
**❓ Answer:** the **selector**, and the **port name**. A ServiceMonitor that matches no Service
— or names a port the Service does not — reports no error at all. Compare
`spec.selector.matchLabels` against `oc get svc --show-labels`, and check the port is named.
{{< /note >}}

2. Why is `hello_dcs_requests_total` almost never useful on its own?

{{< note >}}
**❓ Answer:** it is a **counter** — it only ever goes up, and its absolute value depends on how
long the Pod has been alive. What you want is `rate(...)` over a window, which turns it into
"per second right now".
{{< /note >}}

3. You query another team's namespace with your own token and get Forbidden. Which permission
   decided that?

{{< note >}}
**❓ Answer:** the same one that decides whether you may **read Pods** in that namespace. The
tenant query endpoint authorizes every query against the namespace named in it — so the
metrics boundary is the RBAC boundary, not a separate system.
{{< /note >}}

4. Who configures Prometheus in this story?

{{< note >}}
**❓ Answer:** **nobody you know**. The platform runs user-workload monitoring; you put a
ServiceMonitor in your own namespace and it gets picked up. That split is why you cannot break
anyone else's collection, and why you cannot fix it either.
{{< /note >}}

## Next Steps

Metrics tell you *that* something changed. **Logs** tell you what happened — the next lab in
this track, where the same tenancy boundary applies to a very different kind of data.
