---
title: Container to Deployment
---

First row of the mapping: the compose `hello-dcs` service becomes a
[**Deployment**](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

You built one of these by hand in the **Deploy Your First App** lab. This time you are
translating an existing definition instead of starting from nothing.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/deployment
```

## Open the starter manifest

```editor:open-file
file: ~/exercises/deployment.yaml
```

The shape is familiar: `replicas: 1`, a `selector`, and a Pod `template` whose labels match it.

One field is deliberately unfinished — `image:` still reads `REPLACE_WITH_HARBOR_IMAGE`.

{{< note >}}
**📌 Note:** {{< param product_short >}} is air-gapped, so every image comes from the
platform's own [Harbor]({{< param dcs_docs_base_url >}}/services/container-registry)
registry (`{{< param dcs_registry >}}`) — never from `docker.io` like the compose file.
Page 05 covers exactly why.
{{< /note >}}

## Fill in the image

Select the placeholder:

```editor:select-matching-text
file: ~/exercises/deployment.yaml
text: REPLACE_WITH_HARBOR_IMAGE
```

Replace it with the registry reference:

```editor:replace-matching-text
file: ~/exercises/deployment.yaml
match: REPLACE_WITH_HARBOR_IMAGE
replacement: "${DCS_REGISTRY}/samples/hello-dcs:1.0"
```

## Apply it

The manifest now holds a literal `${DCS_REGISTRY}` — a **shell variable**, not a Kubernetes
feature. `oc apply` does not expand it, so it has to be substituted first.

`envsubst` does that: it replaces every `${VAR}` in its input with the value from your
environment, then the `|` pipe hands the finished manifest to `oc apply -f -` (the `-` means
"read from the pipe, not from a file"):

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f -
```

```examiner:execute-test
name: verify-deployment-image
title: Verify the Deployment uses the Harbor image, not the placeholder
timeout: 10
retries: 3
delay: 2
```

{{< warning >}}
**⚠️ Watch out:** any manifest carrying `${DCS_REGISTRY}` is applied this way — through
`envsubst` first, never with a plain `oc apply -f`. You will repeat this pattern for the
rest of the track.
{{< /warning >}}

## See it running

```terminal:execute
command: oc get deployment,pods -l app=hello-dcs
```

The `-l` flag filters by **label**: `app=hello-dcs` selects only objects carrying it, so one
command shows the Deployment and its Pod together.

Two things to read in the output:

- **READY 1/1** on the Deployment — the desired replica exists and passed its checks.
- **Running** on the Pod — the container started.

```examiner:execute-test
name: verify-deployment-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

{{< note >}}
**⏳ This takes a moment:** the first apply pulls the image, so the Pod can sit in
`ContainerCreating` for a few seconds. The check keeps retrying.
{{< /note >}}

Same result as `docker compose up`, declared in a document instead of run from a command
line. Next: the port mapping.
