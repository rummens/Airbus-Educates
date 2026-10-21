---
title: Change It, Build It Again
---

An image does not change after it is built. When the source changes you need a new build,
and something has to start it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/rebuild
```

## Change the source

```terminal:execute
command: |-
  cd ~/exercises/app
  sed -i 's/Built on DCS, by me/Rebuilt, and it shows/' Containerfile
  grep GREETING Containerfile
```

```section:begin
name: breakdown-edit-greeting
prefix: Breakdown
title: What each part of the command does
```

- **`cd ~/exercises/app`** — moves to the directory that holds the Containerfile.
- **`sed -i`** — edits the file in place instead of printing the result.
- **`'s/Built on DCS, by me/Rebuilt, and it shows/'`** — replaces the old greeting text with the new text.
- **`grep GREETING Containerfile`** — prints the changed line, so you can see the edit worked.

```section:end
name: breakdown-edit-greeting
```

## Build again

```terminal:execute
command: |-
  cd ~/exercises/app
  oc start-build hello-built --from-dir=. --follow
```

```examiner:execute-test
name: verify-second-build
title: Verify a second build ran and succeeded
timeout: 300
retries: .INF
delay: 5
```

Faster this time: the base image is already on the node, and unchanged layers are reused.

```terminal:execute
command: oc get builds
```

Two builds now, `hello-built-1` and `hello-built-2`. Each is a permanent record of one run,
and `latest` in the ImageStream has moved to the newer image.

## The running app has not changed

```terminal:execute
command: oc exec deploy/hello-built -- printenv GREETING
```

```examiner:execute-test
name: verify-app-still-old
title: Verify the running app is still on the previous image
timeout: 60
retries: .INF
delay: 3
```

Still the old greeting. **A new image does not restart anything.** The Deployment is
running the image it pulled when its Pod started, and nothing has told it to look again.

## Make the new image roll out

```terminal:execute
command: oc rollout restart deploy/hello-built && oc rollout status deploy/hello-built --timeout=180s
```

```section:begin
name: breakdown-restart-and-wait
prefix: Breakdown
title: What each part of the command does
```

- **`oc rollout restart deploy/hello-built`** — replaces every Pod of the Deployment. The new Pods pull `hello-built:latest` again and get the rebuilt image.
- **`&&`** — runs the next command only if the restart was accepted.
- **`oc rollout status deploy/hello-built --timeout=180s`** — waits until the new Pods are ready, or gives up after three minutes.

```section:end
name: breakdown-restart-and-wait
```

```examiner:execute-test
name: verify-new-image-rolled-out
title: Verify the rebuilt image is now the one running
timeout: 180
retries: .INF
delay: 5
```

```terminal:execute
command: oc exec deploy/hello-built -- printenv GREETING
```

Now it says `Rebuilt, and it shows`.

## What does this automatically

Doing it by hand is fine once. On a real project, two mechanisms connect the pieces:

- **Build triggers:** a push to the source repository starts a Build. On
  {{< param product_short >}} that is a webhook from your tenant's GitLab, not from the public
  internet.
- **Image triggers:** a Deployment can watch an ImageStream tag and roll out when it moves.
  That is what turns "a build finished" into "the new version is live" without anybody typing
  `rollout restart`.

{{< warning >}}
**⚠️ Watch out:** an automatic image trigger rolls out whatever the build produced, tested or not. A
pipeline that builds and immediately promotes puts an untested image into a running app. That
is why PROD does not accept pushes, which the **DEV vs PROD Namespaces** lab covers.
{{< /warning >}}
