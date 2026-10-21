---
title: ClusterIP and Cluster DNS
---

Start with the default. A **ClusterIP** Service is one virtual IP in front of every ready Pod
that matches its selector.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/clusterip
```

## Deploy two replicas

Two, so every Service in this lab has more than one endpoint and the differences are visible.

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=120s
```

```section:begin
name: breakdown-deploy-app
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment.yaml`** — reads the file and replaces each `${VAR}` placeholder (here the Harbor registry, `${DCS_REGISTRY}`) with the value from your session, so the registry host is never hard-coded.
- **`| oc apply -f -`** — the pipe passes that output to `oc apply`; `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc rollout status deploy/hello-dcs --timeout=120s`** — waits until every replica is ready, or gives up after 120 seconds.

```section:end
name: breakdown-deploy-app
```

```examiner:execute-test
name: verify-app-ready
title: Verify hello-dcs is running with two ready replicas
timeout: 20
retries: .INF
delay: 2
```

## Add the Service

```editor:open-file
file: ~/exercises/service-clusterip.yaml
```

`type: ClusterIP` is written out here, but it is also what you get when you write no `type` at
all.

```terminal:execute
command: oc apply -f service-clusterip.yaml
```

```examiner:execute-test
name: verify-clusterip-endpoints
title: Verify the ClusterIP Service has both Pods as endpoints
timeout: 20
retries: .INF
delay: 2
```

Two things exist now, and they are worth telling apart:

- the **Service** is one name and one virtual IP, and it does not change;
- its **endpoints** are the list of ready Pod IPs behind it, which changes as Pods come and
  go.

```terminal:execute
command: oc get svc hello-dcs -o wide && oc get endpoints hello-dcs
```

```section:begin
name: breakdown-service-and-endpoints
prefix: Breakdown
title: What each part of the command does
```

- **`oc get svc hello-dcs -o wide`** — shows the Service, including its `CLUSTER-IP` and, with `-o wide`, its selector.
- **`&&`** — run the next command only if the first one succeeded.
- **`oc get endpoints hello-dcs`** — shows the ready Pod IPs and ports the Service forwards to.

```section:end
name: breakdown-service-and-endpoints
```

## Ask DNS what the name means

Cluster DNS gives every Service a name of the form
`<service>.<namespace>.svc.cluster.local`. Resolve yours by hand:

```terminal:execute
command: getent hosts hello-dcs.$(oc project -q).svc.cluster.local
```

```section:begin
name: breakdown-resolve-clusterip
prefix: Breakdown
title: What each part of the command does
```

- **`getent hosts`** — asks the terminal's resolver, which is cluster DNS, for the addresses of a name, the same lookup an app does before it connects.
- **`hello-dcs.`** — the Service name, followed by your namespace.
- **`$(oc project -q)`** — runs first and puts your namespace name into the hostname (`-q` prints only the name).
- **`.svc.cluster.local`** — the cluster DNS suffix every Service name ends in.

```section:end
name: breakdown-resolve-clusterip
```

You get **exactly one** address, and it is the Service's `CLUSTER-IP`, not a Pod IP:

```
10.217.5.253    hello-dcs.<your-namespace>.svc.cluster.local
```

```examiner:execute-test
name: verify-clusterip-single-ip
title: Verify DNS returns one address, the Service's own cluster IP
timeout: 20
retries: .INF
delay: 2
```

Clients resolve **one** address that never changes, and the
platform forwards each connection to one of the ready Pods.

## Use it

```terminal:execute
command: curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

```section:begin
name: breakdown-curl-service
prefix: Breakdown
title: What each part of the command does
```

- **`curl -s`** — sends an HTTP request; `-s` hides the progress bar.
- **`-o /dev/null`** — throws the response body away, because only the status matters here.
- **`-w 'HTTP %{http_code}\n'`** — prints the HTTP status code of the response after the request finishes.
- **`"http://hello-dcs.$(oc project -q).svc:8080"`** — the Service name and your namespace (inserted by `$(oc project -q)`), followed by `.svc` and the Service port `8080`. The resolver adds the rest of the `cluster.local` suffix.

```section:end
name: breakdown-curl-service
```

```examiner:execute-test
name: verify-clusterip-http
title: Verify the app answers HTTP 200 through the Service
timeout: 20
retries: .INF
delay: 2
```

{{< note >}}
**📌 Note:** the short form `hello-dcs:8080` also works from inside the same namespace,
because the resolver appends the rest. The long name is used here so it is obvious what is
being asked.
{{< /note >}}

Next, what happens when you take the virtual IP away.
