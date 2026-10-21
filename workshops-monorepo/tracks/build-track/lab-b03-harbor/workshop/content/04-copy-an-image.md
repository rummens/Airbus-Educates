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
