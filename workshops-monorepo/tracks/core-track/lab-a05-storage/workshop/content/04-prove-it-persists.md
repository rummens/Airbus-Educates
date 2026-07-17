---
title: Prove It Persists
---

Here's the whole point. Destroy the Pod, let {{< param product_short >}} create a fresh
one, and check the marker is still there — because it lives on the PV, not the container.

## Restart the Pod

```terminal:execute
command: oc rollout restart deploy/hello-dcs && oc rollout status deploy/hello-dcs --timeout=90s
```

{{< note >}}
Want to watch it? In the **lower** terminal run `oc get pods,pvc -w` — you'll see the old
Pod terminate, a new one start, and the PVC stay `Bound` throughout. `Ctrl-C` when done.
{{< /note >}}

```examiner:execute-test
name: verify-restarted
title: Verify a fresh Pod is running
timeout: 15
retries: .INF
delay: 2
```

## Read the marker back

This is a **brand-new** Pod. If the marker is still readable, the data survived:

```terminal:execute
command: oc exec deploy/hello-dcs -- cat /opt/app-root/src/data/marker
```

```examiner:execute-test
name: verify-persisted
title: Verify the marker survived the restart
timeout: 10
retries: .INF
delay: 2
```

`persisted-marker-42` — same value, new Pod. The container was replaced; the volume, and
everything on it, persisted. **That's persistent storage.**
