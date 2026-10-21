---
title: Expose It Outside the Cluster
---

Now you give the app a real external URL with a Route. First, note the namespace rule
below.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/route
```

{{< note >}}
**⚠️ A Route requires a PROD-type namespace.** DCS only admits Routes in namespaces marked
PROD; a DEV namespace cannot expose anything. Your session namespace is PROD-type for this
lab, so this works. *Why* PROD enforces this, and how, is covered in the **DEV vs PROD Namespaces** lab (Operate & Observe track).
{{< /note >}}

## Create the Route

Open it. There is no explicit `host`, so OpenShift assigns one that includes your
namespace, on the DCS `*.apps` domain:

```editor:open-file
file: ~/exercises/route.yaml
```

The **`tls`** block asks for HTTPS. TLS ends at the platform router (`termination: edge`),
using the `*.apps` certificate DCS manages, and a plain `http://` request is redirected to
`https://` (`insecureEdgeTerminationPolicy: Redirect`).

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

```section:begin
name: breakdown-show-route-host
prefix: Breakdown
title: What each part of the command does
```

- **`oc get route hello-dcs`** — reads the Route object.
- **`-o jsonpath='{.spec.host}{"\n"}'`** — prints one field instead of the whole object:
  `{.spec.host}` is the host name, and `{"\n"}` adds a line break after it.

```section:end
name: breakdown-show-route-host
```

```examiner:execute-test
name: verify-route-admitted
title: Confirm the Route host is set
timeout: 10
retries: 3
delay: 2
```

## Reach it from outside the session

That host is on public DCS DNS, reachable from a normal browser — not just from this
session. Call it:

```terminal:execute
command: |-
  HOST=$(oc get route hello-dcs -o jsonpath='{.spec.host}')
  curl -sk -o /dev/null -w 'HTTP %{http_code} from '"$HOST"'\n' "https://$HOST"
```

```section:begin
name: breakdown-call-route
prefix: Breakdown
title: What each part of the command does
```

- **`HOST=$( … )`** — runs the command inside `$( )` and stores its output in a shell
  variable named `HOST`.
- **`oc get route hello-dcs -o jsonpath='{.spec.host}'`** — prints only the Route's host
  name.
- **`curl -sk`** — `-s` calls the URL quietly, without a progress bar; `-k` skips the
  certificate check, because this terminal may not trust the authority that signed the
  router's certificate (on a training cluster it is often self-signed).
- **`-o /dev/null`** — throws away the page body.
- **`-w 'HTTP %{http_code} from '"$HOST"'\n'`** — prints the status code and the host. The
  quotes switch from single to double around `$HOST`, so the shell fills in its value.
- **`"https://$HOST"`** — the URL to call, built from the variable.

```section:end
name: breakdown-call-route
```

```examiner:execute-test
name: verify-route-reachable
title: Verify the Route URL responds (HTTP 200)
timeout: 15
retries: .INF
delay: 2
```

You should see `HTTP 200`. Because the app runs in **UI mode**, that page also prints its own Route URL,
the live DCS DNS name, so you can see the real address it is serving on.
