---
title: Inspect and Pull an Image
---

Now use the registry. You'll inspect an image's metadata, pull it onto the cluster by
running it, and understand why {{< param product_short >}} uses `skopeo` rather than a
container engine inside a workshop.

## Why skopeo, not docker/podman

A workshop session already runs inside a container. Running `docker` or `podman`
*inside* it means a container engine inside a container — **double-virtualization** — which
{{< param product_short >}} does not allow (it needs privileges and a daemon you shouldn't
have in a tenant workload).

[`skopeo`](https://github.com/containers/skopeo) sidesteps all of that: it's **daemonless**
and talks to registries directly over HTTP. It can inspect and copy images without ever
building or running one — exactly what you need to work with Harbor.

## Inspect an image

Ask Harbor about the sample image without pulling its layers:

```terminal:execute
command: skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0
```

You should see JSON describing the image — its **digest**, layers, architecture, and
labels. The `docker://` prefix is skopeo's *transport* (where the image lives); the digest
is the image's immutable identity — a tag can move, a digest never does.

```examiner:execute-test
name: verify-image-inspectable
title: skopeo can inspect the catalog image
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

{{< note >}}
This reads through your session's **read-only robot account**, so no `skopeo login` is
needed. Inspecting talks to Harbor over the network — it needs the real registry to be
reachable.
{{< /note >}}

## Pull it by running it

The most useful "pull" is the cluster pulling the image to run it. Apply a Pod that
references the catalog image:

```editor:open-file
file: ~/exercises/pod-from-catalog.yaml
```

```terminal:execute
command: oc apply -f pod-from-catalog.yaml
```

{{< note >}}
The node pulls the image from Harbor and starts the container — give it a few seconds.
"Done" is the Pod reaching **Running**.
{{< /note >}}

```terminal:execute
command: oc get pod hello-catalog -w --request-timeout=60s
```

```examiner:execute-test
name: verify-pod-running
title: The catalog image pulled and is Running
args:
- hello-catalog
timeout: 120
retries: .INF
delay: 3
```

The image came straight from a {{< param product_short >}} catalog — no internet involved.
