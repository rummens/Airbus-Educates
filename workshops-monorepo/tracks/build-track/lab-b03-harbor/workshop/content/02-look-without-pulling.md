---
title: Look Without Pulling
---

You can learn almost everything about an image without downloading it. `skopeo` asks the
registry directly.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/inspect
```

## Inspect it

```terminal:execute
command: skopeo inspect docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 | head -25
```

```section:begin
name: breakdown-inspect-image
prefix: Breakdown
title: What each part of the command does
```

- **`skopeo inspect`** — reads the image's metadata from the registry API without downloading its layers.
- **`docker://`** — the transport: it tells `skopeo` the image is in a registry, not in a local file or directory.
- **`${DCS_REGISTRY}/samples/hello-dcs:1.0`** — the registry, the repository and the tag.
- **`| head -25`** — shows only the first 25 lines of the JSON output.

```section:end
name: breakdown-inspect-image
```

```examiner:execute-test
name: verify-inspect-works
title: Verify you can read an image's metadata without pulling it
timeout: 90
retries: .INF
delay: 5
```

Four fields are worth knowing by name:

- **`Digest`** is `sha256:…`, the image's real identity. It is content-addressed, so the same
  digest is always the same bytes.
- **`RepoTags`** lists every tag this repository has. Tags **move**; digests do not.
- **`Layers`** lists the filesystem layers in order. A shared base means shared layers, which
  is why a rebuild is faster than a first build.
- **`Labels`** is metadata baked in at build time. `org.opencontainers.image.source` tells you
  where it came from, when the builder set it.

## Tags move, digests do not

```terminal:execute
command: skopeo inspect docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 --format '{{ "{{" }} .Digest {{ "}}" }}'
```

```section:begin
name: breakdown-read-digest
prefix: Breakdown
title: What each part of the command does
```

- **`skopeo inspect docker://…/hello-dcs:1.0`** — reads the image's metadata from the registry, as before.
- **`--format '…'`** — a Go template. `.Digest` selects one field, so only the digest is printed instead of the full JSON.

```section:end
name: breakdown-read-digest
```

```examiner:execute-test
name: verify-digest-readable
title: Verify the image digest can be read on its own
timeout: 60
retries: .INF
delay: 5
```

That digest is what a scan result is attached to, what an admission policy can pin, and what
`:1.0` pointed at **at this moment**. Tomorrow the tag may point somewhere else; the digest
will not have changed.

{{< warning >}}
**⚠️ Watch out:** this is why a floating tag like `latest` is refused on
{{< param product_short >}}. A tag that moves means the thing you scanned and the thing you
run are not provably the same bytes.
{{< /warning >}}

## What is inside, without running it

```terminal:execute
command: skopeo inspect --config docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 | head -20
```

```section:begin
name: breakdown-inspect-config
prefix: Breakdown
title: What each part of the command does
```

- **`skopeo inspect`** — reads image metadata from the registry without pulling the image.
- **`--config`** — returns the image's runtime configuration (user, environment, command, ports) instead of its manifest summary.
- **`docker://${DCS_REGISTRY}/samples/hello-dcs:1.0`** — the image, in the registry.
- **`| head -20`** — shows only the first 20 lines.

```section:end
name: breakdown-inspect-config
```

```examiner:execute-test
name: verify-config-readable
title: Verify the image's runtime configuration is readable
timeout: 60
retries: .INF
delay: 5
```

`--config` returns what the container will do when it starts: its `User`, `Env`, `Cmd` and
`ExposedPorts`.

Two of those are worth checking before you deploy anything here:

- **`User`** must be non-root, or the restricted SCC refuses the Pod.
- **`Env`** tells you what is baked in, and therefore what you are expected to supply.
