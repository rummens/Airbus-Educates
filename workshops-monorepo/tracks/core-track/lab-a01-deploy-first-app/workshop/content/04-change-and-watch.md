---
title: Change It and Watch the Rollout
---

Here's the {{< param product_short >}} promise from A05 made concrete. Change the desired
state, and the platform reconciles to it — it rolls out a **new** Pod with the new config
and retires the old one, with no downtime and nothing for you to restart by hand.

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
The rollout **replaced the Pod** — so the tunnel from the last page, which pointed at the
*old* Pod, is now closed. That's expected; you'll just reopen it.
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

The response now reads **`Updated without a rebuild`** — served by a brand-new Pod, from
the same image, with no rebuild. That's declarative desired-state and self-healing at
work.

```examiner:execute-test
name: verify-new-greeting
title: Verify the app serves the updated greeting
timeout: 10
```
