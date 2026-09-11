---
title: Headless Services
---

Sometimes a single address is exactly wrong. A database client that must talk to **replica 2**,
or a peer-to-peer cluster where members find each other — those need to address Pods
individually.

Setting `clusterIP: None` makes a **headless** Service: no virtual IP, no load balancing. DNS
answers with the Pods themselves.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/headless
```

## Apply it

```editor:open-file
file: ~/exercises/service-headless.yaml
```

Same selector as before. The only difference is the one line, `clusterIP: None`.

```terminal:execute
command: oc apply -f service-headless.yaml
```

```examiner:execute-test
name: verify-headless-created
title: Verify the headless Service exists with no cluster IP
timeout: 15
retries: .INF
delay: 2
```

Note the `CLUSTER-IP` column:

```terminal:execute
command: oc get svc -o wide
```

`hello-dcs` has an IP. `hello-dcs-peers` reads **None**.

## Ask DNS again

```terminal:execute
command: getent hosts hello-dcs-peers.$(oc project -q).svc.cluster.local
```

This time you get **one line per ready Pod**:

```
10.217.0.101    hello-dcs-peers.<your-namespace>.svc.cluster.local
10.217.0.102    hello-dcs-peers.<your-namespace>.svc.cluster.local
```

Those are **Pod** IPs. Nothing is proxying: the client resolved the name and now talks
straight to a Pod it chose.

```examiner:execute-test
name: verify-headless-per-pod
title: Verify DNS returns one address per ready Pod, and none of them is a cluster IP
timeout: 20
retries: .INF
delay: 2
```

## Why this matters later

A headless Service is also how a **StatefulSet** gives each replica a **stable name**:
`<pod>.<service>.<namespace>.svc.cluster.local`, so `db-0` stays `db-0` across restarts.

That is the next lab. Here, notice only that Pod IPs are not stable — the *names* a
StatefulSet builds on top of this are.

{{< warning >}}
**⚠️ Watch out:** a headless Service gives you no load balancing and no failover. The client
chose that Pod, so the client owns the retry when it disappears.
{{< /warning >}}

Next: a Service that points at nothing in your namespace at all.
