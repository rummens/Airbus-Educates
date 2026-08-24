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
actually uses it (a "wait for first consumer" policy), so let's give it a consumer next.

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
the same file works on any DCS environment.

Applying it therefore takes two steps, joined by a pipe:

1. **`envsubst`** — replaces `${DCS_REGISTRY}` with the real value and prints the finished
   manifest.
2. **`| oc apply -f -`** — hands that output straight to `oc`. The `-` means "read the
   manifest from the pipe, not a file".

```terminal:execute
command: envsubst < hello-dcs-with-volume.yaml | oc apply -f -
```

Now wait for the new Pod to be ready:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=120s
```

Once the Pod is scheduled, DCS provisions a PV and **binds** it to your claim. Confirm both
the claim is Bound and the app is running with the volume mounted:

```examiner:execute-test
name: verify-pvc-bound
title: ✅ Verify the PVC is Bound
timeout: 15
retries: .INF
delay: 2
```

```examiner:execute-test
name: verify-volume-mounted
title: ✅ Verify the app is running with the volume mounted
timeout: 15
retries: .INF
delay: 2
```

## Write something to it

Write a marker into the mounted volume — this goes onto the PV, not the container:

```terminal:execute
command: oc exec deploy/hello-dcs -- sh -c 'echo persisted-marker-42 > /opt/app-root/src/data/marker && cat /opt/app-root/src/data/marker'
```

```examiner:execute-test
name: verify-marker-written
title: ✅ Verify the marker file exists in the volume
timeout: 10
retries: .INF
delay: 2
```

The marker is on the volume now. The real test is what happens when the Pod goes away.
