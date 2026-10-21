---
title: Change It and Watch the Rollout
---

This page shows how {{< param product_short >}} reacts when you change the desired state.

When you change the **desired state** — here, the greeting — the platform reconciles to it:

1. it **rolls out** a new Pod with the new configuration;
2. it **retires** the old one.

There is no downtime, and you restart nothing by hand. The next page defines "desired
state" properly.

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
title: Verify the new greeting rolled out
timeout: 10
retries: .INF
delay: 2
```

{{< note >}}
**⚠️ The rollout replaced the Pod.** The tunnel from the last page pointed at the *old*
Pod, so it is now closed.

This is expected. Reopen it with the command below.
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
title: Verify the tunnel reaches the new Pod (HTTP 200)
timeout: 10
retries: .INF
delay: 2
```

## Confirm the new value (upper terminal)

```terminal:execute
command: curl -s localhost:8080
```

The response now reads `Updated without a rebuild`.

A new **Pod** serves it, from the **same image**, without a rebuild. You changed the
desired state, and {{< param product_short >}} replaced the Pod to match it.

```examiner:execute-test
name: verify-new-greeting
title: Verify the app serves the updated greeting
timeout: 10
retries: 3
delay: 2
```
