---
title: DEV Moves Fast
---

Start in the DEV namespace, with the manifest people actually write first.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/dev
```

## Deploy something unfinished

```editor:open-file
file: ~/exercises/hello-dcs-unsized.yaml
```

No `resources` block at all. No requests, no limits — the app will take the namespace
LimitRange defaults.

```terminal:execute
command: envsubst < hello-dcs-unsized.yaml | oc apply -f - -n $DEV_NS && oc rollout status deploy/hello-dcs -n $DEV_NS --timeout=120s
```

```examiner:execute-test
name: verify-dev-accepts-unsized
title: Verify DEV accepted the unsized workload
timeout: 60
retries: .INF
delay: 3
```

Accepted without comment. That is DEV doing its job: you are iterating, and the platform is
staying out of your way.

## Put a Service in front of it

```terminal:execute
command: oc apply -f service.yaml -n $DEV_NS
```

```examiner:execute-test
name: verify-dev-service
title: Verify the Service in DEV has an endpoint
timeout: 30
retries: .INF
delay: 3
```

## Now try to publish it

```editor:open-file
file: ~/exercises/route.yaml
```

An ordinary Route. Apply it to DEV:

```terminal:execute
command: oc apply -f route.yaml -n $DEV_NS || true
```

It is **refused**, and the message says exactly why:

```
A Route needs a PROD-type namespace. This namespace is DEV-type.
```

```examiner:execute-test
name: verify-dev-route-blocked
title: Verify DEV refused the Route
timeout: 30
retries: .INF
delay: 3
```

{{< note >}}
**📌 Note:** the `|| true` on that command is only so the page continues past an expected
failure. The rejection is the point.
{{< /note >}}

## Why DEV cannot publish

A Route puts your app on the platform's **external** edge — a real hostname, reachable by real
people, fronted by the controlled load balancer the **Services & Cluster Networking** lab
described.

That is a production act. Giving it to a namespace whose whole purpose is unfinished work
would mean half-built things quietly becoming reachable.

So: iterate in DEV, publish from PROD. Next page.
