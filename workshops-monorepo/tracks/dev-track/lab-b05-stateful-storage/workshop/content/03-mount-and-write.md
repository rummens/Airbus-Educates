---
title: Mount and Write
---

A bound PVC is just a disk waiting to be used. Now attach it to the app. Open the updated
Deployment:

```editor:open-file
file: ~/exercises/deployment-stateful.yaml
```

It's the same `hello-dcs` Deployment, with two additions:

- a **volume** named `data`, backed by the `hello-dcs-data` PVC;
- a **volumeMount** placing that volume at `/data` inside the container.

## Apply it

`envsubst` fills in the registry value first, then `oc apply` updates the running Deployment —
starting a rollout that replaces the pod with one that has the volume attached:

```terminal:execute
command: envsubst < deployment-stateful.yaml | oc apply -f -
```

Expected output:

```
deployment.apps/hello-dcs configured
```

Wait for the new pod to be Running:

```terminal:execute
command: oc rollout status deployment/hello-dcs
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

This time, write into the **mounted volume** at `/data` — not the container's own filesystem:

```terminal:execute
command: oc exec deployment/hello-dcs -- sh -c 'echo "persisted-by-dcs" > /data/marker'
```

Read it back to confirm it's there:

```terminal:execute
command: oc exec deployment/hello-dcs -- cat /data/marker
```

You should see:

```
persisted-by-dcs
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

`/data` is the PVC-backed volume — a different place entirely from the `/tmp/note` you lost
on page 1. On the next page you'll destroy the pod again and prove this file is still there.
