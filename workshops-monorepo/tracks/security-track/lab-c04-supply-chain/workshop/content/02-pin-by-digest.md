---
title: Pin an Image by Digest
---

The first control tightens the **run** link: make sure the image your cluster runs is exactly
the one you meant — not "whatever that tag points at today."

## A tag is a movable pointer

When you deploy `samples/hello-dcs:1.0`, the `1.0` is a **tag** — a human-friendly *label* that
points at some image content. Tags are **mutable**: someone can re-push `1.0` tomorrow and it
will point at different content, with the same name. That's convenient for "always get the
latest 1.0," but it means the reference alone doesn't guarantee *what* runs.

A **digest** is the opposite. It's a `sha256:` hash of the image's content — its immutable
identity. Change one byte of the image and the digest changes. Pin to a digest and the
reference can only ever resolve to that exact content.

Ask Harbor for the current digest behind the tag:

```terminal:execute
command: skopeo inspect --format '{{ "{{" }}.Digest{{ "}}" }}' docker://$DCS_REGISTRY/samples/hello-dcs:1.0
```

You should see a single `sha256:...` line — the content hash the tag resolves to right now.

```examiner:execute-test
name: verify-digest
title: skopeo reports a sha256 digest for the tag
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

{{< note >}}
This reads through your session's **read-only robot account**, so no `skopeo login` is needed.
Inspecting talks to Harbor over the network — it needs the real registry reachable.
{{< /note >}}

## Tag vs digest, side by side

Open the "before" manifest — a Pod referencing the mutable tag:

```editor:open-file
file: ~/exercises/pod-by-tag.yaml
```

Its image is `${DCS_REGISTRY}/samples/hello-dcs:1.0`. Correct today, but a moving target.

Now the "after" — the same image pinned by digest:

```editor:open-file
file: ~/exercises/pod-by-digest.yaml
```

Its image is `${DCS_REGISTRY}/samples/hello-dcs@${DIGEST}` — the `@sha256:...` form. `${DIGEST}`
is a placeholder we'll fill with the **real** digest you just inspected, so the manifest pins to
exactly that content.

## Apply the pinned Pod

Capture the live digest into `DIGEST`, substitute both variables, and apply — one click does all
of it:

```terminal:execute
command: export DIGEST=$(skopeo inspect --format '{{ "{{" }}.Digest{{ "}}" }}' docker://$DCS_REGISTRY/samples/hello-dcs:1.0) && echo "Pinning to $DIGEST" && envsubst < pod-by-digest.yaml | oc apply -f -
```

Because `DIGEST` comes straight from `skopeo inspect`, the applied manifest is pinned to the
exact content Harbor reported — no hardcoded, possibly-stale hash. Watch it reach **Running**:

```terminal:execute
command: oc get pod hello-pinned -w --request-timeout=60s
```

```examiner:execute-test
name: verify-pinned-running
title: The digest-pinned Pod pulled and is Running
args:
- hello-pinned
timeout: 120
retries: .INF
delay: 3
```

The node resolved the digest, pulled that exact content from Harbor, and started it. From now on
this Pod can only ever run that content — a retag of `1.0` cannot silently change what it runs.
That is the integrity guarantee digest pinning buys you.
