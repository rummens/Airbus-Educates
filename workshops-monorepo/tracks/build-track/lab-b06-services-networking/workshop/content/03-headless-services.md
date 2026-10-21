---
title: Headless Services
---

Some clients need to address a specific Pod: a database client that must talk to **replica
2**, or a peer-to-peer cluster whose members find each other.

Setting `clusterIP: None` makes a **headless** Service. There is no virtual IP and no load
balancing, and DNS answers with the Pods themselves.

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

Those are **Pod** IPs. Nothing is proxying, so the client resolved the name and talks
straight to the Pod it chose.

```examiner:execute-test
name: verify-headless-per-pod
title: Verify DNS returns one address per ready Pod, and none of them is a cluster IP
timeout: 20
retries: .INF
delay: 2
```

## Headless Services and StatefulSets

A headless Service is also how a **StatefulSet** gives each replica a **stable name**:
`<pod>.<service>.<namespace>.svc.cluster.local`, so `db-0` stays `db-0` across restarts.

The next lab covers StatefulSets. Pod IPs change when a Pod is replaced, but the names a
StatefulSet builds on top of this Service stay the same.

{{< warning >}}
**⚠️ Watch out:** a headless Service gives you no load balancing and no failover. The
client chose that Pod, so the client owns the retry when it disappears.
{{< /warning >}}

Next, a Service that points at nothing in your namespace at all.
