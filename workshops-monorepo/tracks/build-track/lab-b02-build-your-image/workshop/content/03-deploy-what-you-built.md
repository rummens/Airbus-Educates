---
title: Deploy What You Built
---

The image exists. Now run it, and reference it the way the platform prefers.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/deploy
```

## Find it in the ImageStream

```terminal:execute
command: oc get imagestream hello-built -o jsonpath='{range .status.tags[*]}{.tag}{"  →  "}{.items[0].dockerImageReference}{"\n"}{end}'
```

```section:begin
name: breakdown-read-istag
prefix: Breakdown
title: What each part of the command does
```

- **`oc get imagestream hello-built`** — reads the ImageStream object.
- **`-o jsonpath='…'`** — prints only the fields named in the expression, instead of the table.
- **`{range .status.tags[*]}` … `{end}`** — repeats the part in between once for every tag the ImageStream tracks.
- **`{.tag}`** — the tag name, for example `latest`.
- **`{"  →  "}`** — a literal arrow between the two columns.
- **`{.items[0].dockerImageReference}`** — the newest image the tag points at, written with its `@sha256:` digest.
- **`{"\n"}`** — ends each tag's output with a newline.

```section:end
name: breakdown-read-istag
```

```examiner:execute-test
name: verify-imagestream-tag
title: Verify the ImageStream has a tag pointing at your built image
timeout: 120
retries: .INF
delay: 5
```

The tag `latest` now resolves to an image **with a digest** in the cluster's registry. The
digest identifies the exact image. The tag can be moved to a different image later.

## Deploy it

```editor:open-file
file: ~/exercises/deployment.yaml
```

It references the registry path for your namespace's `hello-built:latest`.

```terminal:execute
command: envsubst < ~/exercises/deployment.yaml | oc apply -f - && oc rollout status deploy/hello-built --timeout=180s
```

```section:begin
name: breakdown-apply-and-wait
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < ~/exercises/deployment.yaml`** — reads the manifest and replaces `${DCS_REGISTRY}` with the registry address from your session.
- **`| oc apply -f -`** — the pipe hands the result to `oc apply`. The `-f -` means "read the manifest from the pipe" instead of from a file.
- **`&&`** — runs the next command only if the apply succeeded.
- **`oc rollout status deploy/hello-built --timeout=180s`** — waits until the new Pods are ready, or gives up after three minutes.

```section:end
name: breakdown-apply-and-wait
```

```examiner:execute-test
name: verify-built-app-running
title: Verify the app is running from the image you built
timeout: 180
retries: .INF
delay: 5
```

## Prove it is yours

```terminal:execute
command: oc exec deploy/hello-built -- printenv GREETING VERSION
```

```examiner:execute-test
name: verify-baked-in-values
title: Verify the values baked into your image are what the container runs with
timeout: 60
retries: .INF
delay: 3
```

The output is `Built on DCS, by me`. Nothing set it at deploy time: it is the `ENV` line
from your Containerfile, baked into the image by your build.

**Configuration** (such as `oc set env`) is added at deploy time. **Image contents** (such as
`ENV` in the Containerfile) are fixed at build time.
