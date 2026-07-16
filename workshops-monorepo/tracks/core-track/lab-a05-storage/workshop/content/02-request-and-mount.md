---
title: Request and Mount
---

Time to claim a volume and give it to your app.

## Claim a volume

Open the PVC — it asks for 1Gi of **File** (ReadWriteMany) storage:

```editor:open-file
file: ~/exercises/pvc-file.yaml
```

```terminal:execute
command: oc apply -f pvc-file.yaml
```

DCS provisions a PV and **binds** it to your claim. The check waits for `Bound`:

```examiner:execute-test
name: verify-pvc-bound
title: Verify the PVC is Bound
timeout: 15
retries: .INF
delay: 2
```

## Mount it into the app

Now deploy hello-dcs with that volume mounted at `/data`:

```editor:open-file
file: ~/exercises/hello-dcs-with-volume.yaml
```

```terminal:execute
command: envsubst < hello-dcs-with-volume.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=90s
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
command: oc exec deploy/hello-dcs -- sh -c 'echo persisted-marker-42 > /data/marker && cat /data/marker'
```

```examiner:execute-test
name: verify-marker-written
title: Verify the marker file exists in the volume
timeout: 10
retries: .INF
delay: 2
```

The marker is on the volume now. The real test is what happens when the Pod goes away.
