---
title: Ports to Service
---

Second row of the mapping: `ports: "8080:8080"` **publishes** the container's port onto the
Docker host's own port 8080. Anything that can reach the host can reach the app.

A cluster has no single host to publish onto. Instead, a
[**Service**](https://kubernetes.io/docs/concepts/services-networking/service/) gives the
app a stable address of its own, independent of any host and of the Pod's IP.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/service
```

{{< note >}}
**📌 Why not just use the Pod's IP?** Pods are **replaced** on every rollout and get a new
IP each time. A Service's name and address stay constant while the Pods behind it come and
go.
{{< /note >}}

## Open the Service manifest

```editor:open-file
file: ~/exercises/service.yaml
```

Note `selector: app: hello-dcs` — the same label the Deployment stamps onto its Pods. That
is how the Service finds them.

There is no image reference in this file, so no `envsubst` this time.

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

An **endpoint** is a Pod IP the Service currently sends traffic to. No endpoints means the
selector matches nothing.

## Reach it by cluster DNS

The Service answers in-cluster at `hello-dcs.<namespace>.svc`. Call it from your terminal:

```terminal:execute
command: curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

Each part of that command does one thing:

- **`-s`** — no progress bar.
- **`-o /dev/null`** — throw the page body away.
- **`-w 'HTTP %{http_code}\n'`** — print just the status code.
- **`$(oc project -q)`** — substitute your own namespace name.

```examiner:execute-test
name: verify-service-dns
title: Verify the Service responds HTTP 200 over cluster DNS
timeout: 10
retries: .INF
delay: 2
```

`HTTP 200` from a name that survives Pod restarts — the compose `ports:` line, translated.

Nothing is exposed outside the cluster yet. That is a Route, which the Core **Expose Your
App** lab covers, and which the **Services & Cluster Networking** lab later in this track
takes apart properly.

Next: the environment variable.
