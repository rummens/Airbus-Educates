---
title: A Stable Address
---

Pods are ephemeral — they're replaced on every rollout and get a new IP each time. You
can't hand out a Pod IP as an address. A [**Service**](https://kubernetes.io/docs/concepts/services-networking/service/)
solves that: a stable name and IP that always load-balances to whichever Pods currently
match its selector.

## Get the app running

First, deploy the app (in UI mode, so it serves a proper page later):

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=90s
```

```examiner:execute-test
name: verify-app-ready
title: Verify the app is running
timeout: 15
retries: .INF
delay: 2
```

## Front it with a Service

Open the Service — note the `selector: app: hello-dcs`, the same labels the Deployment
stamps on its Pods (from A01). That's how the Service finds them:

```editor:open-file
file: ~/exercises/service.yaml
```

```terminal:execute
command: oc apply -f service.yaml
```

```examiner:execute-test
name: verify-service
title: Verify the Service has endpoints
timeout: 10
retries: .INF
delay: 2
```

## Reach it by cluster DNS

The Service is reachable in-cluster at `hello-dcs.<namespace>.svc`. Call it from your
terminal:

```terminal:execute
command: curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

```examiner:execute-test
name: verify-service-dns
title: Verify the Service responds over cluster DNS
timeout: 10
retries: .INF
delay: 2
```

`HTTP 200` — a stable address that survives Pod restarts. But that name only works
*inside* the cluster. Next, why, and how to fix it.
