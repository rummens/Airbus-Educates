---
title: Expose It for Real
---

Now you give the app a real external URL with a Route. One thing to know first.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/route
```

{{< note >}}
**A Route requires a PROD-type namespace.** DCS only admits Routes in namespaces marked
PROD; a DEV namespace cannot expose anything. Your session namespace is PROD-type for this
lab, so this works. *Why* PROD enforces this, and how, is a Developer-track topic (**DEV vs PROD Namespaces & Policies**).
{{< /note >}}

## Create the Route

Open it. There is no explicit `host`, so OpenShift assigns one that includes your
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

See the host DCS assigned. The `-o jsonpath='...'` flag extracts one field from the object
instead of printing all of it; `{.spec.host}` selects the host name, and `{"\n"}` adds a
line break after it:

```terminal:execute
command: oc get route hello-dcs -o jsonpath='{.spec.host}{"\n"}'
```

```examiner:execute-test
name: verify-route-admitted
title: Confirm the Route host is set
timeout: 10
retries: 3
delay: 2
```

## Reach it from outside the session

That host is on public DCS DNS, reachable from a normal browser, not just this session.
Call it. The first line stores the Route host in a shell variable named `HOST`; the second
line calls it with `curl`. The `-k` flag tells `curl` to accept the DCS TLS certificate
without complaint, and `%{http_code} from "$HOST"` prints the status code and the host it
reached:

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

`HTTP 200`. Because the app runs in **UI mode**, that page also prints its own Route URL,
the live DCS DNS name, so you can see the real address it is serving on.
