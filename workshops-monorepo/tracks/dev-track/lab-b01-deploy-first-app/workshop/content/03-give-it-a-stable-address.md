---
title: Give It a Stable Address
---

Your app is running, but nothing can reliably reach it yet. Pods are **ephemeral**: when
one is replaced — a crash, a scale change, a rollout — the new Pod gets a **new name and a
new IP**. You can never hard-code a Pod IP to talk to your app.

The fix is a [Service](https://kubernetes.io/docs/concepts/services-networking/service/): a
stable name and IP that automatically tracks whatever Pods exist and **load-balances**
across them. As Pods come and go, the Service's set of backends (its *endpoints*) updates on
its own — the label selector is the glue.

## Create the Service

Open the Service manifest:

```editor:open-file
file: ~/exercises/service.yaml
```

Its `spec.selector` is `app: hello-dcs` — the same label on your Pods — and it exposes port
8080. Create it:

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

The address listed is your Pod. Scale the Deployment later and these update on their own —
that's the Service tracking the label selector.

## Reach It by DNS

Inside the cluster, address the app by its **DNS name**, which {{< param product_short >}}
registers automatically — never by a Pod IP. Within your own namespace the Service name
alone works; fully qualified it is `<service>.<namespace>.svc`. Call your app from the
terminal:

```terminal:execute
command: curl -s http://hello-dcs.$SESSION_NAMESPACE.svc:8080
```

You should see the `hello-dcs` page's HTML come back — proof the Service is routing to a
healthy Pod.

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
This `curl` works only *inside* the cluster — your terminal runs as a Pod in the same
cluster. Reaching the app from a **browser** needs the session ingress, which you'll set up
next.
{{< /note >}}
