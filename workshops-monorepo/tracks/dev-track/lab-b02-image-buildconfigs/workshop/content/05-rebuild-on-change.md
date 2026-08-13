---
title: Rebuild on Change
---

A BuildConfig you have to remember to run by hand isn't much better than building on a
laptop. In a real pipeline, a build fires **automatically** whenever its source changes —
that's what a [build trigger](https://docs.openshift.com/container-platform/latest/cicd/builds/triggering-builds-build-hooks.html)
does.

## Three ways a build can trigger itself

| Trigger | Fires when | Typical use |
|---|---|---|
| **ConfigChange** | The BuildConfig is first created | Bootstraps an initial image with no manual step |
| **ImageChange** | The *builder* or base image's ImageStream gets a new tag | Rebuild automatically when a patched builder image lands (e.g. a CVE fix) |
| **Webhook** | Your git host `POST`s to a generated webhook URL after a push | The everyday case: commit code, a build starts within seconds |

The BuildConfig you applied earlier declares none of these — you triggered its only build
so far by hand with `oc start-build`, deliberately, so the mechanism was visible. In your
own projects you would normally add a **Webhook** trigger so a `git push` starts a build
without you doing anything.

{{< note >}}
This lab's git source is a small read-only mirror reachable in-session — there's no git
host here to push to or configure a webhook against. The next step simulates what that
webhook would do: fire a build. Everything else about the mechanism is identical to the
real thing.
{{< /note >}}

## Before: note the current image

Every build produces a fresh image, identified by a unique digest in its
`dockerImageReference` — even a rebuild of unchanged source gets a new one, because the
image's layers (and their timestamps) are never bit-for-bit identical between two build
runs. Note the current reference before rebuilding:

```terminal:execute
command: |-
  oc get istag hello-dcs-built:latest-built -o jsonpath='{.image.dockerImageReference}{"\n"}'
session: 1
```

## Trigger a second build (lower terminal)

```terminal:execute
command: oc start-build hello-dcs-s2i --follow
session: 2
```

```examiner:execute-test
name: verify-second-build
title: Verify a second build of hello-dcs-s2i completed
timeout: 10
retries: .INF
delay: 3
```

## After: a different image, same tag

```terminal:execute
command: |-
  oc get istag hello-dcs-built:latest-built -o jsonpath='{.image.dockerImageReference}{"\n"}'
session: 1
```

Compare the two references — the digest (the part after the `@sha256:`) has changed. The
tag `latest-built` still points at one image at a time, but which image it points to just
moved. Redeploying now (`oc rollout restart deploy/hello-dcs-built`) would roll your
running Pods onto this new build, exactly like the config-triggered rollout you saw in
B01 — except this time a whole new image is behind it, not just a changed environment
variable.

You've now driven the full loop this lab set out to teach: git source → on-cluster build
→ Harbor → deploy → rebuild. Next, the summary and a few questions to check it stuck.
