---
title: Expose It for Real
---

Now the payoff: a real external URL. One thing to know first —

{{< note >}}
**A Route requires a PROD-type namespace.** DCS only admits Routes in namespaces marked
PROD; a DEV namespace can't expose anything. Your session namespace is PROD-type for this
lab, so you're good. *Why* PROD enforces this — and how — is a Developer-track topic
(**B06**).
{{< /note >}}

## Create the Route

Open it — there's no explicit `host`, so OpenShift assigns one that includes your
namespace, on the DCS `*.apps` domain:

```editor:open-file
file: ~/exercises/route.yaml
```

```terminal:execute
command: oc apply -f route.yaml
```

```examiner:execute-test
name: verify-route-admitted
title: Verify the Route was admitted with a host
timeout: 10
retries: .INF
delay: 2
```

See the host DCS assigned:

```terminal:execute
command: oc get route hello-dcs -o jsonpath='{.spec.host}{"\n"}'
```

```examiner:execute-test
name: verify-route-admitted
title: Confirm the Route host is set
timeout: 10
```

## Reach it from outside the session

That host is on public DCS DNS — reachable from a normal browser, not just this session.
Call it:

```terminal:execute
command: |-
  HOST=$(oc get route hello-dcs -o jsonpath='{.spec.host}')
  curl -sk -o /dev/null -w 'HTTP %{http_code} from '"$HOST"'\n' "http://$HOST"
```

```examiner:execute-test
name: verify-route-reachable
title: Verify the Route URL responds (HTTP 200)
timeout: 15
retries: .INF
delay: 2
```

`HTTP 200`. Because the app runs in **UI mode**, that page also prints its *own* Route
URL — the live DCS DNS name — so you can see the real address it's serving on.
