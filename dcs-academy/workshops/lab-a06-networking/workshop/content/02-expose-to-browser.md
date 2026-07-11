---
title: Expose to the Browser
---

The quickest way to put an app in front of a browser on {{< param product_short >}} is the
**session proxy** — an auth-gated HTTPS endpoint that forwards to your Service. It's the
preferred path for browser access during development because it's encrypted and requires no
DNS or certificate work from you.

## Open the app in a tab

Create an **App** tab pointing at the proxied endpoint for your `hello-dcs` Service:

```dashboard:create-dashboard
name: App
url: "{{< param ingress_protocol >}}://{{< param session_name >}}-app.{{< param ingress_domain >}}"
```

The tab loads the app over HTTPS through the proxy. Behind the scenes the proxy terminates
TLS and forwards to `hello-dcs:8080` in your namespace — so there's no mixed-content
problem and the endpoint is gated by your session login.

{{< note >}}
Why prefer the session proxy over a raw Route for browser access during a lab? It's
HTTPS by default, needs no hostname/cert setup, and is tied to your session's auth. A
Route (next page) is what you use for a *real, externally published* address.
{{< /note >}}

Now switch back to the terminal so the next commands are visible:

```dashboard:open-dashboard
name: Terminal
```

Confirm the same endpoint the proxy forwards to is healthy in-cluster:

```terminal:execute
command: curl -s -o /dev/null -w '%{http_code}\n' http://hello-dcs.$SESSION_NAMESPACE.svc:8080
```

You should see `200`.

```examiner:execute-test
name: verify-svc-reachable
title: The proxied Service is reachable
args:
- hello-dcs
- "8080"
timeout: 15
retries: 5
delay: 3
```
