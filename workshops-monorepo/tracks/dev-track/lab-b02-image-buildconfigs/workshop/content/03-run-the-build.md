---
title: Run the Build
---

A BuildConfig is just a recipe until you trigger it. In real projects a build is
usually triggered automatically — by a webhook or an image update — but you can always
trigger one by hand with [`oc start-build`](https://docs.openshift.com/container-platform/latest/cicd/builds/basic-build-operations.html).
That's what you'll do now, and watch the whole thing happen live in the **lower**
terminal while you check its status from the **upper** one.

{{< note >}}
A real build takes real time — pulling the builder image, checking out git, assembling
the app, then pushing the result to Harbor. Expect roughly a minute. The checks below
poll, so there's nothing to do but watch.
{{< /note >}}

## Start the build (lower terminal)

Run this in the **lower** pane. The `--follow` flag streams the Build Pod's log straight
to your terminal instead of returning immediately, so you see every stage as it happens:

```terminal:execute
command: oc start-build hello-dcs-s2i --follow
session: 2
```

Watch the log scroll: it fetches your git source, runs the S2I assemble process, builds
the image layer, and — near the end — pushes it to Harbor. That push is the step you've
been building up to on this page.

## Check its status (upper terminal)

While the lower pane is still streaming, switch to the **upper** terminal and list the
[Build](https://docs.openshift.com/container-platform/latest/cicd/builds/basic-build-operations.html)
objects this BuildConfig has created:

```terminal:execute
command: oc get builds
session: 1
```

Each build gets its own name (`hello-dcs-s2i-1`, then `-2`, …) and a `STATUS` column —
`New` → `Pending` → `Running` → `Complete` (or `Failed`). Run it again in a few seconds if
you're still mid-build; the status moves through those phases on its own.

```examiner:execute-test
name: verify-build-complete
title: Verify the build reaches phase Complete
timeout: 10
retries: .INF
delay: 3
```

## Confirm the push landed in Harbor

The build finishing is only half the story — check that the image it produced actually
arrived where `output.to` pointed:

```terminal:execute
command: oc get istag hello-dcs-built:latest-built
session: 1
```

You'll see a row with an `IMAGE REFERENCE` — that's the pushed image's location in
Harbor, proof the ImageStreamTag now points at real, pulled content rather than an empty
placeholder.

```examiner:execute-test
name: verify-istag-populated
title: Verify the ImageStreamTag now has an image
timeout: 10
retries: .INF
delay: 2
```

You built an image on {{< param product_short >}} without touching a Dockerfile locally
or running a single `docker` command. Next, deploy it.
