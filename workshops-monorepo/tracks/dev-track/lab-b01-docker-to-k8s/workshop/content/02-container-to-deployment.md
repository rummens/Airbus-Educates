---
title: Container to Deployment
---

First row of the mapping: the compose `hello-dcs` service becomes a
[**Deployment**](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
You already built one of these by hand in A01 — this time you're translating an existing
definition instead of starting from nothing.

## Open the starter manifest

```editor:open-file
file: ~/exercises/deployment.yaml
```

The shape should look familiar from A01/A02: `replicas: 1`, a `selector` and Pod
`template` with matching labels. One thing is missing — the `image:` field still reads
`REPLACE_WITH_HARBOR_IMAGE`. On DCS, an air-gapped platform, every image is pulled from
the [Harbor]({{< param dcs_docs_base_url >}}/registry/overview) registry
(`{{< param dcs_registry >}}`) rather than a public registry like the compose file's
`docker.io` — more on exactly why on page 05.

## Fill in the image

Select the placeholder:

```editor:select-matching-text
file: ~/exercises/deployment.yaml
text: REPLACE_WITH_HARBOR_IMAGE
```

And replace it with the Harbor-mirrored reference:

```editor:replace-matching-text
file: ~/exercises/deployment.yaml
match: REPLACE_WITH_HARBOR_IMAGE
replacement: "${DCS_REGISTRY}/samples/hello-dcs:1.0"
```

## Apply it

The manifest now contains a literal `${DCS_REGISTRY}` placeholder — a shell variable
reference, not a Kubernetes feature. `oc apply` doesn't expand it, so it has to be
substituted first. `envsubst` does exactly that: it replaces every `${VAR}` in its input
with the matching environment variable's value, here reading `$DCS_REGISTRY` from your
session:

```terminal:execute
command: |-
  envsubst < deployment.yaml | oc apply -f -
```

{{< note >}}
Any manifest with a `${DCS_REGISTRY}` placeholder is applied this way — piped through
`envsubst` first — never with a plain `oc apply -f`. You'll repeat this pattern for the
rest of the workshop.
{{< /note >}}

```examiner:execute-test
name: verify-deployment-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

## See it running

```terminal:execute
command: oc get deployment,pods -l app=hello-dcs
```

The `-l` flag filters by **label** — `app=hello-dcs` selects only objects carrying that
label, so this one command shows the Deployment and its Pod together, ignoring anything
else in your namespace.

You'll see the Deployment reporting `1/1` READY and one Pod `Running` — the same
Deployment → Pod result you'd get from `docker compose up`, but declared in a YAML
document instead of run from a command line.

```examiner:execute-test
name: verify-deployment-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

The container is migrated. Next: the port mapping.
