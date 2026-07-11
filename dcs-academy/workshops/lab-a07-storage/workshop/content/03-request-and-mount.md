---
title: Request and Mount a Volume
---

Time to make it real: request a File volume, mount it into the sample app, and write some
data to it.

## Create the PVC

```editor:open-file
file: ~/exercises/pvc-file.yaml
```

It requests 1Gi, **ReadWriteMany**, from the File storage class (named via the `DCS_SC_FILE`
variable). Apply it — `envsubst` fills in the storage-class name from the environment before
`oc` sees it:

```terminal:execute
command: envsubst < pvc-file.yaml | oc apply -f -
```

{{< note >}}
The StorageClass provisions a real disk and binds it to your claim — this can take a few
seconds. "Done" is the PVC reaching **Bound**.
{{< /note >}}

```terminal:execute
command: oc get pvc hello-dcs-data -w --request-timeout=60s
```

```examiner:execute-test
name: verify-pvc-bound
title: The PVC is Bound
args:
- hello-dcs-data
timeout: 120
retries: .INF
delay: 3
```

## Mount it into the app

```editor:open-file
file: ~/exercises/hello-dcs-with-volume.yaml
```

This is the familiar `hello-dcs` Deployment with two additions: a **volume** backed by the
PVC, and a **volumeMount** putting it at `/data` in the container. Apply it:

```terminal:execute
command: envsubst < hello-dcs-with-volume.yaml | oc apply -f -
```

```examiner:execute-test
name: verify-pods-running
title: The app is running with the volume mounted
args:
- hello-dcs
- "1"
timeout: 120
retries: .INF
delay: 3
```

## Write data to the volume

Write a marker file into the mounted volume at `/data` — not the container's own filesystem:

```terminal:execute
command: oc exec deployment/hello-dcs -- sh -c 'echo "persisted-by-dcs" > /data/marker'
```

Read it back to confirm it's there:

```terminal:execute
command: oc exec deployment/hello-dcs -- cat /data/marker
```

```examiner:execute-test
name: verify-marker
title: The marker file is on the volume
args:
- hello-dcs
- /data/marker
- persisted-by-dcs
timeout: 15
retries: 3
delay: 2
```

`/data` is the PVC-backed volume. On the next page you'll destroy the Pod and prove the file
is still there.
