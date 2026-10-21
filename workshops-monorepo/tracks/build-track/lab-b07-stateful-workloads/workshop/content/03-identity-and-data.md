---
title: Identity and Data
---

Ordinal names alone do not show that each replica is separate. On this page you address one
**specific** replica and give each one its own data.

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

```section:begin
name: breakdown-resolve-replica
prefix: Breakdown
title: What each part of the command does
```

- **`getent hosts`** — asks the terminal's resolver, which is cluster DNS, for the addresses of a name.
- **`hello-dcs-0.hello-dcs.`** — the Pod name, then the headless Service name.
- **`$(oc project -q)`** — runs first and puts your namespace name into the hostname (`-q` prints only the name).
- **`.svc.cluster.local`** — the cluster DNS suffix.

```section:end
name: breakdown-resolve-replica
```

One address comes back, and it is **that Pod's** IP, not a Service IP and not replica
1's.

```examiner:execute-test
name: verify-pod-dns-identity
title: Verify each replica resolves to its own Pod address
timeout: 30
retries: .INF
delay: 3
```

The per-Pod name lets a client connect to replica 0 specifically.

{{< note >}}
**💡 Tip:** the Service name on its own (`hello-dcs.<namespace>.svc`) still resolves to
**both** Pod addresses, as any headless Service does. The per-Pod name is what a StatefulSet
adds.
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

```section:begin
name: breakdown-write-markers
prefix: Breakdown
title: What each part of the command does
```

- **`for i in 0 1; do … done`** — runs the lines in between twice, once with `i=0` and once with `i=1`.
- **`oc exec hello-dcs-$i --`** — runs the command after `--` inside Pod `hello-dcs-0`, then `hello-dcs-1`.
- **`sh -c '…'`** — starts a shell inside the Pod, so the `>` redirect writes to the Pod's file system instead of your terminal's.
- **`echo "written by $HOSTNAME"`** — prints a line with the Pod's own name. The single quotes around the `sh -c` script stop your terminal from expanding `$HOSTNAME`, so each Pod fills in its own name.
- **`> /opt/app-root/src/data/owner.txt`** — writes that line into a file on the mounted volume.
- **`echo "wrote a marker…"`** — prints a confirmation once the loop has finished.

```section:end
name: breakdown-write-markers
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

```section:begin
name: breakdown-read-markers
prefix: Breakdown
title: What each part of the command does
```

- **`for i in 0 1; do … done`** — runs the lines in between once for each replica.
- **`printf 'hello-dcs-%s: ' "$i"`** — prints the Pod name as a label, without a line break, so the file's content follows on the same line.
- **`oc exec hello-dcs-$i -- cat /opt/app-root/src/data/owner.txt`** — prints the marker file from that Pod's own volume.

```section:end
name: breakdown-read-markers
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
both would read the same thing. Each replica has its own volume.

Next, delete one and see what comes back.
