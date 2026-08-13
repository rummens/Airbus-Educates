---
title: Inspect and Pull an Image
---

Time to talk to Harbor for real. You'll use [`skopeo`](https://github.com/containers/skopeo),
a command-line tool for inspecting, copying, and signing container images **without** a
running container engine. That "without" matters here: the workshop container already runs
inside a container, and running a full Docker/Podman daemon *inside* it to manage more
containers is double-virtualization for no benefit — `skopeo` talks to registries directly
over their API, so there's no daemon to run at all.

## Inspect the image

Ask Harbor about `samples/hello-dcs:1.0` — the same image A01 deployed and B02 (re)builds —
using the read-only robot account already configured in your session:

```terminal:execute
command: skopeo inspect docker://{{< param dcs_registry >}}/samples/hello-dcs:1.0
```

The `docker://` prefix is a **transport** — it tells `skopeo` *where* to resolve the
reference from. `skopeo` can talk to several kinds of source (a registry, a local tar
archive, an OCI directory on disk); `docker://` means "resolve this as an image in a
container registry," which is what you want here.

You should see a JSON document describing the image, including its digest:

```
{
    "Name": "harbor.example.dcs/dcs-academy/samples/hello-dcs",
    "Digest": "sha256:2c26b0f5b6f0e...e4b0d3255bfef95601890afd80709",
    "RepoTags": ["1.0"],
    "Created": "2026-06-18T10:04:00Z",
    "DockerVersion": "",
    "Labels": {
        "org.opencontainers.image.description": "DCS Academy sample app (hello-dcs)"
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Layers": ["sha256:...", "sha256:..."]
}
```

The **`Digest`** is the field that matters most: a `sha256` hash of the image's content. A
tag like `1.0` can be moved to point at a different image later; a digest can't — it *is*
the image. You'll come back to this distinction in a moment.

```examiner:execute-test
name: verify-catalog-inspect
title: Verify skopeo can inspect the catalog image
args:
- "$DCS_REGISTRY/samples/hello-dcs:1.0"
timeout: 15
```

## Pull it onto the cluster

Inspecting proves the image is *there*; deploying proves it *runs*. `pod-from-catalog.yaml`
is a plain Pod referencing the same image:

```editor:open-file
file: ~/exercises/pod-from-catalog.yaml
```

Notice it references the image by **tag** (`:1.0`), with a comment noting that a
production manifest should pin the **digest** you just saw instead — a tag can be
overwritten to point at different content later, but a digest is that exact content,
forever. Tags are convenient for a workshop; digests are what you'd actually ship.

The manifest has a `${DCS_REGISTRY}` placeholder, so before applying it you substitute the
real registry host with [`envsubst`](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html) —
piping the file through it fills in the variable from your terminal's environment before
`oc` ever sees the YAML. You'll use this exact pattern for every manifest with a
`${DCS_REGISTRY}` placeholder in this workshop:

```terminal:execute
command: envsubst < pod-from-catalog.yaml | oc apply -f -
```

{{< note >}}
The image pull can take a few seconds the first time. The check below polls until the Pod
is actually `Running`, so give it a moment.
{{< /note >}}

```examiner:execute-test
name: verify-catalog-pod-running
title: Verify the Pod is running from the catalog pull
timeout: 10
retries: .INF
delay: 2
```

Confirm it yourself rather than taking the check's word for it:

```terminal:execute
command: oc get pod catalog-pull
```

You should see `catalog-pull` in phase `Running` — the same image `skopeo inspect` just
described, now scheduled and running on {{< param product_short >}}, pulled straight from
its Harbor project using nothing but a read-only robot account.
