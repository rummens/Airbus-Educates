---
title: Copy It Somewhere Else
---

Moving an image between registries is the operation behind mirroring, promotion and every
air-gapped import. It is one command, and no daemon.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/copy
```

## Copy into your own namespace

The cluster's registry stands in for your DEV Harbor project here. Your session token is the
credential:

```terminal:execute
command: |-
  skopeo copy --dest-tls-verify=false \
    --dest-creds "$(oc whoami):$(oc whoami -t)" \
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

What that command actually did:

1. **Read** the manifest and layers from the source registry.
2. **Wrote** them to the destination registry, under a new name.
3. Preserved the **digest** of each layer — nothing was rebuilt, and nothing was unpacked.

{{< note >}}
**📌 `--dest-creds "$(oc whoami):$(oc whoami -t)"`.** A registry wants a username and password;
your OpenShift token works as the password. On {{< param product_short >}} this is where a
Harbor **robot account** goes instead — a credential issued to a system, not a person, scoped
to one project.
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

Nothing about that operation is special. A **mirror from a DEV project into a PROD project** is
exactly this: read here, write there, same digest.

What makes it a promotion is everything around it:

- it is **requested through ITSM** rather than run by you;
- the destination **refuses direct pushes**, so this is the only route in;
- the image must be **below the CVE threshold** before the destination will serve it.

Which brings us to the report that decides that.
