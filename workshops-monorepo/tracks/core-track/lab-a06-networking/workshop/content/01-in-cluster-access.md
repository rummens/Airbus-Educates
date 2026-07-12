---
title: Reaching a Service In-Cluster
---

Every exposure story starts inside the cluster. Before traffic can come from a browser, the
app has to be reachable by other workloads — and that's what a Service gives you.

## Deploy the app

```editor:open-file
file: ~/exercises/hello-dcs.yaml
```

This is the familiar `hello-dcs` Deployment plus a [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
on port 8080. Apply it:

```terminal:execute
command: oc apply -f hello-dcs.yaml
```

{{< note >}}
The Pod needs to pull its image and start — give it a few seconds. "Done" is when the
Deployment reports an available replica.
{{< /note >}}

```examiner:execute-test
name: verify-deploy-ready
title: hello-dcs is running
args:
- hello-dcs
timeout: 90
retries: .INF
delay: 3
```

## Reach it by DNS

Inside the cluster, a Service is reachable at a stable DNS name:
`<service>.<namespace>.svc`. Call it:

```terminal:execute
command: curl -s http://hello-dcs.$SESSION_NAMESPACE.svc:8080
```

You should get the app's greeting back (an HTTP 200 with a short body). That works from
*inside* the cluster — but a colleague with a browser can't use a `.svc` name. The rest of
this workshop is about bridging that gap.

```examiner:execute-test
name: verify-svc-reachable
title: The Service answers in-cluster
args:
- hello-dcs
- "8080"
timeout: 15
retries: 5
delay: 3
```
