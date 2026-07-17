---
title: Ports to Service
---

Second row of the mapping: the compose line `ports: "8080:8080"` **publishes** the
container's port 8080 onto the Docker host's own port 8080 — anything that can reach the
host can reach the app. Kubernetes has no host to publish onto; instead it gives the app a
stable address through a [**Service**](https://kubernetes.io/docs/concepts/services-networking/service/),
independent of the host or the Pod's own IP.

{{< note >}}
Pods are replaced on every rollout and get a new IP each time, so nothing can rely on a
Pod IP directly. A Service's name and address stay constant even as the Pods behind it
come and go — the same problem `-p`/`ports:` solves for a single host, a Service solves
across the whole cluster.
{{< /note >}}

## Open the Service manifest

```editor:open-file
file: ~/exercises/service.yaml
```

Note the `selector: app: hello-dcs` — the same label the Deployment stamps onto its Pods.
That's how the Service finds the right Pods to send traffic to; no image reference here,
so no `envsubst` needed this time.

## Apply it

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

The Service is reachable in-cluster at `hello-dcs.<namespace>.svc` — call it from your
terminal:

```terminal:execute
command: |-
  curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

```examiner:execute-test
name: verify-service-dns
title: Verify the Service responds over cluster DNS
timeout: 10
retries: .INF
delay: 2
```

`HTTP 200` — a name that survives Pod restarts, reachable from anywhere in the cluster.
No public exposure yet (that's a later Developer lab); for now this is the equivalent of
compose's `ports:` line, translated. Next: the environment variable.
