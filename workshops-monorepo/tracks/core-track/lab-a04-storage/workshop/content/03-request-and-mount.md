---
title: Request and Mount
---

You saw the container's own filesystem lose everything on restart. Now give the app a
volume that keeps its data.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/request-mount
```

## Claim a volume

Open the PVC — it asks for 1Gi of **File** (ReadWriteMany) storage:

```editor:open-file
file: ~/exercises/pvc-file.yaml
```

Apply the file to create the claim. `oc apply -f pvc-file.yaml` reads the manifest from the
named file (`-f` means "from this file") and creates the object in your namespace:

```terminal:execute
command: oc apply -f pvc-file.yaml
```

The claim is created. Many storage classes only **bind** the volume once a workload
uses it (a "wait for first consumer" policy), so let's give it a consumer next.

## Mount it into the app

Re-apply hello-dcs — same app, now with the volume mounted at `/opt/app-root/src/data`:

```editor:open-file
file: ~/exercises/hello-dcs-with-volume.yaml
```

{{< note >}}
**📌 Two details make the write work.** This image runs as a **non-root** user, and a non-root
process can only write where it owns the path.

1. **The mount path.** A volume mounted at a root-level path like `/data` stays root-owned
   and the app hits **`Permission denied`**. Mounting inside the image's own writable home
   (`/opt/app-root/src`) avoids that.
2. **`securityContext.fsGroup: 1001`** in the manifest. A freshly provisioned volume arrives
   root-owned whatever you mount it on; `fsGroup` tells the platform to hand the volume to
   that group and make it group-writable, so the non-root app can write it.
{{< /note >}}

The manifest names its image as `${DCS_REGISTRY}/...` instead of a hard-coded registry, so
the same file works on any DCS environment:

```terminal:execute
command: envsubst < hello-dcs-with-volume.yaml | oc apply -f -
```

```section:begin
name: breakdown-apply-deployment
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < hello-dcs-with-volume.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with the
  registry address from your session, then prints the finished manifest.
- **`| oc apply -f -`** — the pipe hands that output to `oc apply`; `-f -` means "read
  the manifest from the pipe" instead of from a file.

```section:end
name: breakdown-apply-deployment
```

Now wait for the new Pod to be ready:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=120s
```

```section:begin
name: breakdown-wait-for-rollout
prefix: Breakdown
title: What each part of the command does
```

- **`oc rollout status deploy/hello-dcs`** — waits until the new Pod is Ready and the
  rollout is complete.
- **`--timeout=120s`** — stops waiting after 120 seconds and reports an error,
  instead of waiting forever.

```section:end
name: breakdown-wait-for-rollout
```

Once the Pod is scheduled, DCS provisions a PV and **binds** it to your claim. Confirm both
the claim is Bound and the app is running with the volume mounted:

```examiner:execute-test
name: verify-pvc-bound
title: Verify the PVC is Bound
timeout: 15
retries: .INF
delay: 2
```

```examiner:execute-test
name: verify-volume-mounted
title: Verify the app is running with the volume mounted
timeout: 15
retries: .INF
delay: 2
```

## Write something to it

Write a marker into the mounted volume — this goes onto the PV, not the container:

```terminal:execute
command: oc exec deploy/hello-dcs -- sh -c 'echo persisted-marker-42 > /opt/app-root/src/data/marker && cat /opt/app-root/src/data/marker'
```

```section:begin
name: breakdown-write-marker
prefix: Breakdown
title: What each part of the command does
```

- **`oc exec deploy/hello-dcs`** — runs a command inside a Pod of the Deployment.
- **`--`** — separates the `oc` options from the command to run in the container.
- **`sh -c '…'`** — starts a shell in the container to run the quoted commands, so the `>`
  and `&&` happen inside the container.
- **`echo persisted-marker-42 > /opt/app-root/src/data/marker`** — writes the marker into a
  file on the mounted volume.
- **`&& cat /opt/app-root/src/data/marker`** — if the write succeeded, prints the file back.

```section:end
name: breakdown-write-marker
```

```examiner:execute-test
name: verify-marker-written
title: Verify the marker file exists in the volume
timeout: 10
retries: .INF
delay: 2
```

The marker is on the volume now. Next, replace the Pod and check the marker is still there.
