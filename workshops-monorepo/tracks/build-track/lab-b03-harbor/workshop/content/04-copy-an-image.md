---
title: Copy It Somewhere Else
---

Moving an image between registries is the operation behind mirroring, promotion and every
air-gapped import. It is one command, with no daemon involved.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/copy
```

## Copy into your own namespace

On {{< param product_short >}} the destination would be the project you asked for on the last
page. There is no Harbor behind this cluster, so the cluster's own registry stands in for it,
and your session token is the credential:

```terminal:execute
command: |-
  skopeo copy --dest-tls-verify=false \
    --dest-creds "unused:$(oc whoami -t)" \
    docker://${DCS_REGISTRY}/samples/hello-dcs:1.0 \
    docker://image-registry.openshift-image-registry.svc:5000/${SESSION_NAMESPACE}/mirrored:1.0
```

```section:begin
name: breakdown-copy-image
prefix: Breakdown
title: What each part of the command does
```

- **`skopeo copy`** — copies an image's manifest and layers from one registry to another. The two image references at the end are the source and the destination.
- **`--dest-tls-verify=false`** — skips certificate checks on the destination. The training cluster's internal registry uses a certificate this terminal does not trust.
- **`--dest-creds "unused:$(oc whoami -t)"`** — the destination's username and password. `$(oc whoami -t)` is replaced by your session token. The note below explains the username.
- **`\`** at the end of a line — continues the command on the next line.
- **`docker://${DCS_REGISTRY}/samples/hello-dcs:1.0`** — the source image.
- **`docker://image-registry.openshift-image-registry.svc:5000/${SESSION_NAMESPACE}/mirrored:1.0`** — the destination: the cluster's internal registry, a repository in your session namespace, and the new name and tag.

```section:end
name: breakdown-copy-image
```

```examiner:execute-test
name: verify-image-copied
title: Verify the image was copied into your namespace's registry
timeout: 180
retries: .INF
delay: 5
```

What that command did:

1. **Read** the manifest and layers from the source registry.
2. **Wrote** them to the destination registry, under a new name.
3. Preserved the **digest** of each layer. Nothing was rebuilt and nothing was unpacked.

{{< note >}}
**📌 `--dest-creds "unused:$(oc whoami -t)"`.** A registry wants a username and a password.
The cluster's registry only checks the **token** and ignores the username, so `unused` works
as well as anything.

Do not be tempted by `$(oc whoami)` there: for a ServiceAccount that expands to
`system:serviceaccount:<ns>:<name>`, and those colons break `user:password` parsing with an
unhelpful "authentication required".

On {{< param product_short >}} a Harbor **robot account** goes here instead: a credential
issued to a system rather than a person, and scoped to one project.
{{< /note >}}

## See it arrive

```terminal:execute
command: oc get imagestream mirrored -o jsonpath='{range .status.tags[*]}{.tag}{"  →  "}{.items[0].dockerImageReference}{"\n"}{end}'
```

```section:begin
name: breakdown-read-mirrored-tag
prefix: Breakdown
title: What each part of the command does
```

- **`oc get imagestream mirrored`** — reads the ImageStream object.
- **`-o jsonpath='…'`** — prints only the fields named in the expression, instead of the table.
- **`{range .status.tags[*]}` … `{end}`** — repeats the part in between once for every tag the ImageStream tracks.
- **`{.tag}`** — the tag name, for example `latest`.
- **`{"  →  "}`** — a literal arrow between the two columns.
- **`{.items[0].dockerImageReference}`** — the newest image the tag points at, written with its `@sha256:` digest.
- **`{"\n"}`** — ends each tag's output with a newline.

```section:end
name: breakdown-read-mirrored-tag
```

```examiner:execute-test
name: verify-mirrored-tag
title: Verify the copied image is tracked in your namespace
timeout: 120
retries: .INF
delay: 5
```

## This is what a promotion is

A **mirror from a DEV project into a PROD project** is the same operation you just ran: it
copies the image without changing its digest.

A promotion adds three conditions around that copy:

- it is **requested through ITSM** rather than run by you;
- the destination **refuses direct pushes**, so this is the only route in;
- the image must be **below the CVE threshold** before the destination will serve it.

Next: the scan report that decides whether an image is below the threshold.
