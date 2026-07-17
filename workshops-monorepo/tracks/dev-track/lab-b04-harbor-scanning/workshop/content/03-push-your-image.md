---
title: Push and Verify Your Image
---

The image B02 built didn't just appear in Harbor — someone (B02's BuildConfig) **pushed**
it there. Pushing needs a different kind of robot account from the one you've used so far,
and it's worth understanding the contrast even on the pages where you don't push yourself.

## Pull-only vs. push-capable

Your session's robot account can only `pull`. B02's build pipeline uses a **second**,
push-capable robot account — scoped to the same `samples` project, but with `push`
permission added. Harbor's project permission model is what makes this safe: a robot
account's rights are a project-scoped allow-list, not an all-or-nothing login. A pipeline
that can push a new `hello-dcs` tag still can't touch an unrelated project, and a
compromised pull-only credential (like the one in this workshop's session) can never push
anything at all.

Pushing the image B02 built looks like this — shown here for shape, not run in this
session (this session's robot account genuinely cannot push, matching the read-only
posture you've used since page 2):

```workshop:copy
text: |-
  skopeo copy oci-archive:hello-dcs.tar docker://{{< param dcs_registry >}}/samples/hello-dcs:1.0 --dest-creds "$PUSH_ROBOT_USER:$PUSH_ROBOT_SECRET"
```

`skopeo copy` moves an image between two locations without ever needing a local daemon —
here, from a local build output (`oci-archive:`) to Harbor (`docker://`), authenticating
with the push-capable robot's credentials rather than a personal login.

## Confirm the image is there

What you *can* do with a read-only robot account is confirm a push landed — which is
exactly what you'd check after B02's build finishes. List every tag Harbor holds for
`samples/hello-dcs`:

```terminal:execute
command: skopeo list-tags docker://{{< param dcs_registry >}}/samples/hello-dcs
```

`list-tags` is a read-only Harbor project browse — it doesn't touch any single image, just
asks "what tags exist here?" You should see a JSON list including `1.0`:

```
{
    "Repository": "harbor.example.dcs/dcs-academy/samples/hello-dcs",
    "Tags": [
        "1.0",
        "flagged"
    ]
}
```

`1.0` is the tag B02's push-capable robot account landed. Its presence here — visible
through your pull-only credential — is the confirmation a push succeeded, without ever
needing push rights yourself.

```examiner:execute-test
name: verify-samples-tags
title: Verify the pushed tag is present in the project
args:
- "{{< param dcs_registry >}}/samples/hello-dcs"
- "1.0"
timeout: 15
```

Two robot accounts, two scopes, one project: push lands an image, pull consumes it. Next,
what Harbor does to every image the moment it lands.
