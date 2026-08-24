---
title: Change It and Watch the Rollout
---

This is the core {{< param product_short >}} behaviour, made concrete.

When you change the **desired state** — here, the greeting — the platform reconciles to it:

1. it **rolls out** a new Pod with the new configuration;
2. it **retires** the old one.

No downtime, and nothing for you to restart by hand. The next page defines this
"desired state" idea properly.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/rollout
```

## Change the greeting again (upper terminal)

In the **upper** pane, set a new value:

```terminal:execute
command: oc set env deploy/hello-dcs GREETING="Updated without a rebuild"
```

That one change makes {{< param product_short >}} roll out a replacement Pod. The check
waits for the new version to become available:

```examiner:execute-test
name: verify-rollout-new
title: ✅ Verify the new greeting rolled out
timeout: 10
retries: .INF
delay: 2
```

{{< note >}}
**⚠️ The rollout replaced the Pod.** The tunnel from the last page pointed at the *old*
Pod, so it is now closed.

That is expected — you simply reopen it.
{{< /note >}}

## Reopen the tunnel (lower terminal)

Same command as before, in the **lower** pane — it reconnects to the new Pod:

```terminal:execute
command: |-
  oc rollout status deploy/hello-dcs --timeout=60s
  kill "$(cat /tmp/pf.pid 2>/dev/null)" 2>/dev/null || true
  oc port-forward deploy/hello-dcs 8080:8080 >/tmp/pf.log 2>&1 &
  echo $! > /tmp/pf.pid
  sleep 2 && echo "port-forward ready on localhost:8080"
session: 2
```

```examiner:execute-test
name: verify-portforward
title: ✅ Verify the tunnel reaches the new Pod (HTTP 200)
timeout: 10
retries: .INF
delay: 2
```

## Confirm the new value (upper terminal)

```terminal:execute
command: curl -s localhost:8080
```

The response now reads `Updated without a rebuild`.

It is served by a brand-new **Pod**, from the **same image**, with no rebuild — declarative
desired state at work.

```examiner:execute-test
name: verify-new-greeting
title: ✅ Verify the app serves the updated greeting
timeout: 10
retries: 3
delay: 2
```
