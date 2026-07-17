---
title: Ephemeral by Default
---

Before you claim any storage, see the problem it solves. A container's own filesystem is
**ephemeral** — it lives and dies with the Pod. Nothing you write inside a running
container survives that container being replaced.

Let's prove it, then fix it on the next pages.

## Deploy the app with no storage

Deploy hello-dcs on its own — no volume, nothing attached. `oc create deployment` builds a
minimal Deployment from the image (`$DCS_REGISTRY` is the Harbor registry, filled in for
you):

```terminal:execute
command: oc create deployment hello-dcs --image="$DCS_REGISTRY/samples/hello-dcs:1.0" && oc rollout status deploy/hello-dcs --timeout=120s
```

```examiner:execute-test
name: verify-ephemeral-ready
title: Verify the app is running
timeout: 15
retries: .INF
delay: 2
```

## Write a file inside the container

The app runs as a non-root user, so it *can* write inside its own home directory
(`/opt/app-root/src`). Drop a note there:

```terminal:execute
command: oc exec deploy/hello-dcs -- sh -c 'echo written-inside-the-container > /opt/app-root/src/note && cat /opt/app-root/src/note'
```

You see `written-inside-the-container` — the file is there, on the container's own
filesystem.

## Now destroy the Pod

Delete the Pod. The Deployment immediately starts a **fresh** one from the image:

```terminal:execute
command: oc delete pod -l app=hello-dcs && oc rollout status deploy/hello-dcs --timeout=120s
```

## The file is gone

Look for the note on the new Pod:

```terminal:execute
command: oc exec deploy/hello-dcs -- cat /opt/app-root/src/note || echo "(gone — the file did not survive)"
```

```examiner:execute-test
name: verify-ephemeral-lost
title: Verify the file did NOT survive the new Pod
timeout: 15
retries: .INF
delay: 2
```

The note is **gone**. The new Pod started from the clean image — everything the old
container wrote to its filesystem went with it. That's the default: **no Pod, no data.**

For anything that must outlive a Pod — a database, uploads, state — you need storage that
is *not* part of the container. That's what you'll request next.
