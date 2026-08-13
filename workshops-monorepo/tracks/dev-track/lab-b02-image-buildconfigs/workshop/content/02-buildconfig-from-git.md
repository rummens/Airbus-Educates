---
title: A BuildConfig from Git
---

Time to read the real thing. Open the S2I BuildConfig you'll run in this lab:

```editor:open-file
file: ~/exercises/buildconfig-s2i.yaml
```

## The git source

```editor:select-matching-text
file: ~/exercises/buildconfig-s2i.yaml
text: |2
    source:
      type: Git
      git:
        uri: ${BUILD_SOURCE_REPO}
        ref: main
```

`source.git.uri` is the repository the Build Pod checks out before doing anything else —
the same idea as `git clone`, just run by the platform instead of by you.
`${BUILD_SOURCE_REPO}` resolves (via `envsubst`, in a moment) to a small repository already
reachable from your session — no external git host, no public internet, consistent with
{{< param product_short >}} being air-gapped. `ref: main` pins which branch to build; in a
real project you'd point this at whatever branch or tag your pipeline builds from.

## The strategy

```editor:select-matching-text
file: ~/exercises/buildconfig-s2i.yaml
text: |2
    strategy:
      type: Source
      sourceStrategy:
        # The S2I builder image itself is Harbor-mirrored, like every image on
        # DCS — never pulled from an external registry.
        from:
          kind: DockerImage
          name: ${DCS_REGISTRY}/s2i-builders/python-311:1
```

`type: Source` selects the S2I strategy from the last page. `sourceStrategy.from` names the
**builder image** that knows how to assemble this particular repo's source — here, a
Harbor-mirrored Python S2I builder, referenced through `${DCS_REGISTRY}` exactly like any
other image reference on this platform.

## The output

```editor:select-matching-text
file: ~/exercises/buildconfig-s2i.yaml
text: |2
    output:
      to:
        kind: ImageStreamTag
        name: hello-dcs-built:latest-built
```

`output.to` is where the finished image goes: a tag (`latest-built`) on the
`hello-dcs-built` ImageStream you'll apply next. That ImageStream is what actually holds
the pointer to the pushed image in Harbor.

Note the two tags play different roles. The **builder** input is pinned (`python-311:1`) —
you never want a build's toolchain shifting under you, the same "no floating `:latest`"
rule you met in B01. The **output** tag `latest-built` is a moving pointer *you* own: each
successful build overwrites it so "the latest thing I built" always resolves, while the
immutable, promotable identity of a specific build is its digest.

## Apply the BuildConfig and its ImageStream

Both manifests reference `${DCS_REGISTRY}` or `${BUILD_SOURCE_REPO}`, so — carrying the
rule forward from B01 — apply them with [`envsubst`](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html),
never a plain `oc apply`:

```terminal:execute
command: envsubst < buildconfig-s2i.yaml | oc apply -f -
```

```terminal:execute
command: oc apply -f imagestream.yaml
```

`imagestream.yaml` has no `${...}` placeholders, so it's applied directly.

```examiner:execute-test
name: verify-buildconfig-imagestream
title: Verify the BuildConfig and ImageStream exist
timeout: 10
```

Both objects now exist, but no image has been built yet — a BuildConfig describes *how* to
build, it doesn't build anything by itself. Next, you'll trigger the actual build.
