---
title: Ephemeral by Default
---

Before you claim any storage, see the problem it solves. A container's own filesystem is
**ephemeral** — it exists only while the Pod exists. Nothing you write inside a running
container survives that container being replaced.

You will prove that below, then fix it on the next pages.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/ephemeral
```

## Deploy the app with no storage

Deploy hello-dcs on its own, with no volume attached. `oc create deployment` builds a
minimal Deployment from an image. The `--image` flag names the image to run; `$DCS_REGISTRY`
is the Harbor registry, filled in for you:

```terminal:execute
command: oc create deployment hello-dcs --image="$DCS_REGISTRY/samples/hello-dcs:v1.0.0"
```

Now wait for the Pod to be ready. `oc rollout status` blocks until the Deployment has a
running Pod; `--timeout=120s` makes it give up after 120 seconds rather than wait forever:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=120s
```

```examiner:execute-test
name: verify-ephemeral-ready
title: ✅ Verify the app is running
timeout: 15
retries: .INF
delay: 2
```

## Write a file inside the container

The app runs as a **non-root** user, so it *can* write inside its own home directory
(`/opt/app-root/src`). Write a file there.

Three parts to the command:

- **`oc exec`** — runs a command inside the Pod.
- **`--`** — separates the `oc` flags from the command to run.
- **`sh -c '...'`** — runs that shell command. Here it writes the file, then prints it back
  with `cat`.

```terminal:execute
command: oc exec deploy/hello-dcs -- sh -c 'echo written-inside-the-container > /opt/app-root/src/note && cat /opt/app-root/src/note'
```

You see `written-inside-the-container` — the file is there, on the container's own
filesystem.

## Now destroy the Pod

Delete the Pod. The `-l app=hello-dcs` flag selects the Pod by its label (`-l` means "match
this label") rather than by name, so you do not need to know the generated Pod name:

```terminal:execute
command: oc delete pod -l app=hello-dcs
```

The Deployment immediately starts a **fresh** Pod from the image. Wait for it:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=120s
```

## The file is gone

Look for the note on the new Pod. The `||` operator runs the second command only if the
first one fails, so if the file is missing you get a clear message instead of an error:

```terminal:execute
command: oc exec deploy/hello-dcs -- cat /opt/app-root/src/note || echo "(gone — the file did not survive)"
```

```examiner:execute-test
name: verify-ephemeral-lost
title: ✅ Verify the file did NOT survive the new Pod
timeout: 15
retries: .INF
delay: 2
```

The note is **gone**. The new Pod started from the clean image — everything the old
container wrote to its filesystem went with it. That's the default: **no Pod, no data.**

For anything that must outlive a Pod — a database, uploads, state — you need storage that
is *not* part of the container. That's what you'll request next.
