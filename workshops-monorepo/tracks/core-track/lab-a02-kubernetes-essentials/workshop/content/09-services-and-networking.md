---
title: Services and In-Cluster Networking
---

You have Pods running, but there's a problem hiding in what you've seen: Pods are
**ephemeral**. When one is replaced (a crash, a scale-down, a rollout), the new Pod gets
a **new name and a new IP address**. You saw this during self-healing.

Check the current Pod IP:

```terminal:execute
command: oc get pods -l app=hello-dcs -o wide
```

That IP is only reachable inside the cluster, and it won't survive the next Pod
replacement. So you can never hard-code a Pod IP to talk to your app. You need a stable
address that automatically tracks whatever Pods exist. That's a
[Service](https://kubernetes.io/docs/concepts/services-networking/service/).

## What a Service Does

A Service gives your application a stable name and IP, and **load-balances** across all
Pods that match its label selector. As Pods come and go, the Service's set of backends
(its *endpoints*) updates automatically — the label selector is the glue, exactly as
discussed earlier.

Open the Service manifest:

```editor:open-file
file: ~/exercises/service.yaml
```

Its `spec.selector` is `app: hello-dcs` — the same label on your Pods — and it exposes
port 8080. Create it:

```terminal:execute
command: oc apply -f service.yaml
```

Expected:

```
service/hello-dcs created
```

```examiner:execute-test
name: verify-service
title: Verify the service has endpoints
args:
- hello-dcs
timeout: 15
retries: .INF
delay: 2
```

## Endpoints: the Service's Backends

See which Pod IPs the Service is sending traffic to:

```terminal:execute
command: oc get endpoints hello-dcs
```

The addresses listed are your Pods. Scale the Deployment and these update on their own —
that's the Service tracking the label selector.

## Reaching It by DNS

Never use the Service's IP either — use its **DNS name**, which Kubernetes registers
automatically. Within the same project, the Service name alone works; fully qualified it
is `<service>.<namespace>.svc`. Call your app:

```terminal:execute
command: curl -s http://hello-dcs.$SESSION_NAMESPACE.svc:8080
```

```examiner:execute-test
name: verify-svc-reachable
title: Verify the service responds over HTTP
args:
- hello-dcs
- "8080"
timeout: 10
retries: 3
delay: 2
```

{{< note >}}
This works only *inside* the cluster — your terminal runs as a Pod in the same cluster,
which is why `curl` reaches it. Exposing the app to a **browser** outside the cluster
needs a Route or the session proxy, which you'll do in the Networking workshop.
{{< /note >}}
