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

```examiner:execute-test
name: verify-inspect-works
title: Verify you can read an image's metadata without pulling it
timeout: 90
retries: .INF
delay: 5
```

Four fields are worth knowing by name:

- **`Digest`** — `sha256:…`, the image's real identity. Content-addressed: the same digest is
  always the same bytes.
- **`RepoTags`** — every tag this repository has. Tags **move**; digests do not.
- **`Layers`** — the filesystem layers, in order. A shared base means shared layers, which is
  why a rebuild is faster than a first build.
- **`Labels`** — metadata baked in at build time. `org.opencontainers.image.source` tells you
  where it came from, when the builder set it.

## Tags move, digests do not

```terminal:execute
command: skopeo inspect docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 --format '{{ "{{" }} .Digest {{ "}}" }}'
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
{{< param product_short >}}. Not fussiness — a tag that moves means the thing you scanned and
the thing you run are not provably the same.
{{< /warning >}}

## What is inside, without running it

```terminal:execute
command: skopeo inspect --config docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 | head -20
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

Two of those you now know to check before deploying anything on this platform:

- **`User`** — non-root, or the restricted SCC will refuse it.
- **`Env`** — what is baked in, versus what you are expected to supply.
