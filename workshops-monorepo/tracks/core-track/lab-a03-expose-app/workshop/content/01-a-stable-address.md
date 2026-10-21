---
title: A Stable Address
---

Pods are **replaced** on every rollout, and each new Pod gets a new IP address. You cannot
hand out a Pod IP as a fixed address.

A [**Service**](https://kubernetes.io/docs/concepts/services-networking/service/) solves
this. It is a stable name and IP that always load-balances to whichever Pods currently match
its **selector**.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/service
```

## Get the app running

First, deploy the app in UI mode, so it serves a full web page later. Applying it takes two
steps; run them one after another and read what each does.

**Step 1 — fill in the registry, then apply.** The manifest names its image as
`${DCS_REGISTRY}/...` instead of a hard-coded registry, so the same file works on any DCS
environment:

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f -
```

```section:begin
name: breakdown-apply-deployment
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with the
  registry address from your session, then prints the finished manifest.
- **`| oc apply -f -`** — the pipe hands that output to `oc apply`; `-f -` means "read
  the manifest from the pipe" instead of from a file.

```section:end
name: breakdown-apply-deployment
```

**Step 2 — wait for the rollout.** `oc rollout status` waits until the new Pod is Ready, so
you know the app is running before moving on:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=90s
```

```section:begin
name: breakdown-wait-for-rollout
prefix: Breakdown
title: What each part of the command does
```

- **`oc rollout status deploy/hello-dcs`** — waits until the new Pod is Ready and the
  rollout is complete.
- **`--timeout=90s`** — stops waiting after 90 seconds and reports an error,
  instead of waiting forever.

```section:end
name: breakdown-wait-for-rollout
```

```examiner:execute-test
name: verify-app-ready
title: Verify the app is running
timeout: 15
retries: .INF
delay: 2
```

## Front it with a Service

Open the Service. Note the `selector: app: hello-dcs` — the same labels the Deployment
puts on its Pods (from the **Deploy Your First App** lab). That is how the Service finds them:

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

The Service is reachable inside the cluster at `hello-dcs.<namespace>.svc`. Call it from
your terminal:

```terminal:execute
command: curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

```section:begin
name: breakdown-call-service
prefix: Breakdown
title: What each part of the command does
```

- **`curl -s`** — calls the URL quietly, without a progress bar.
- **`-o /dev/null`** — throws away the page body.
- **`-w 'HTTP %{http_code}\n'`** — prints `HTTP` and the response's status code, then a line
  break.
- **`"http://hello-dcs.$(oc project -q).svc:8080"`** — the Service's in-cluster DNS name and
  port. `$(oc project -q)` runs first and inserts your namespace name.

```section:end
name: breakdown-call-service
```

```examiner:execute-test
name: verify-service-dns
title: Verify the Service responds over cluster DNS
timeout: 10
retries: .INF
delay: 2
```

`HTTP 200` confirms a stable address that survives Pod restarts. But that name only works
inside the cluster. The next page explains why, and how to fix it.
