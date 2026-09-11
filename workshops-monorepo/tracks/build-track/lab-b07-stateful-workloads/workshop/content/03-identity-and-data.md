---
title: Identity and Data
---

Two Pods with tidy names prove nothing yet. Now address one **specific** replica, and give
each one data of its own.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/dns
```

## A DNS name per Pod

The headless Service gives every Pod a name of the form
`<pod>.<service>.<namespace>.svc.cluster.local`. Resolve replica 0's:

```terminal:execute
command: getent hosts hello-dcs-0.hello-dcs.$(oc project -q).svc.cluster.local
```

One address comes back, and it is **that Pod's** IP — not a Service IP, and not replica 1's.

```examiner:execute-test
name: verify-pod-dns-identity
title: Verify each replica resolves to its own Pod address
timeout: 30
retries: .INF
delay: 3
```

This is the point of the whole exercise: a client can say *"connect to replica 0"* and mean it.

{{< note >}}
**💡 Tip:** the Service name on its own (`hello-dcs.<namespace>.svc`) still resolves to **both**
Pod addresses, as any headless Service does. The per-Pod name is the addition.
{{< /note >}}

## Write something different into each volume

Each replica has its own disk, so each can hold its own data. Write the Pod's **own name**
into its volume:

```terminal:execute
command: |-
  for i in 0 1; do
    oc exec hello-dcs-$i -- sh -c 'echo "written by $HOSTNAME" > /opt/app-root/src/data/owner.txt'
  done
  echo "wrote a marker into each replica's volume"
```

The mount path sits inside the image's writable home, and `fsGroup: 1001` in the manifest is
what lets a non-root process write a freshly provisioned volume.

Read them back:

```terminal:execute
command: |-
  for i in 0 1; do
    printf 'hello-dcs-%s: ' "$i"
    oc exec hello-dcs-$i -- cat /opt/app-root/src/data/owner.txt
  done
```

Two different answers, from two different disks:

```
hello-dcs-0: written by hello-dcs-0
hello-dcs-1: written by hello-dcs-1
```

```examiner:execute-test
name: verify-marker-per-replica
title: Verify each replica wrote its own name into its own volume
timeout: 30
retries: .INF
delay: 3
```

If those two Pods shared one volume, the second write would have overwritten the first and
both would read the same. They do not share.

Next: delete one and see what comes back.
