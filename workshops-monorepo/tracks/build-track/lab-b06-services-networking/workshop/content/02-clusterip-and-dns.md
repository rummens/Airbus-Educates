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

- the **Service** — one name, one virtual IP, unchanging;
- its **endpoints** — the list of ready Pod IPs behind it, which changes as Pods come and go.

```terminal:execute
command: oc get svc hello-dcs -o wide && oc get endpoints hello-dcs
```

## Ask DNS what the name means

Cluster DNS gives every Service a name of the form
`<service>.<namespace>.svc.cluster.local`. Resolve yours by hand:

```terminal:execute
command: getent hosts hello-dcs.$(oc project -q).svc.cluster.local
```

You get **exactly one** address, and it is the Service's `CLUSTER-IP` — not a Pod IP:

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

That is the whole point of the type: clients resolve **one** address that never changes, and
the platform forwards each connection to one of the ready Pods.

## Use it

```terminal:execute
command: curl -s -o /dev/null -w 'HTTP %{http_code}\n' "http://hello-dcs.$(oc project -q).svc:8080"
```

```examiner:execute-test
name: verify-clusterip-http
title: Verify the app answers HTTP 200 through the Service
timeout: 20
retries: .INF
delay: 2
```

{{< note >}}
**📌 Note:** the short form `hello-dcs:8080` works too from inside the same namespace — the
resolver appends the rest. The long name is used here so it is obvious what is being asked.
{{< /note >}}

Next: what happens when you take the virtual IP away.
