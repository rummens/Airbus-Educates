---
title: Request and Mount
---

You saw the container's own filesystem forget everything on restart. Now give the app a
volume that *doesn't*.

## Claim a volume

Open the PVC — it asks for 1Gi of **File** (ReadWriteMany) storage:

```editor:open-file
file: ~/exercises/pvc-file.yaml
```

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
**Why mount it there and not at `/data`?** This image runs as a **non-root** user, and a
non-root process can only write where it owns the path. A volume mounted at a root-level
path like `/data` stays root-owned, and the app hits **`Permission denied`** trying to
write. Mounting inside the image's own writable home (`/opt/app-root/src`) avoids that.
{{< /note >}}

```terminal:execute
command: envsubst < hello-dcs-with-volume.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=120s
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

```examiner:execute-test
name: verify-marker-written
title: Verify the marker file exists in the volume
timeout: 10
retries: .INF
delay: 2
```

The marker is on the volume now. The real test is what happens when the Pod goes away.
