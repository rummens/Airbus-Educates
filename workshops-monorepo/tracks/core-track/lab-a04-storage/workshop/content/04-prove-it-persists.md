---
title: Prove It Persists
---

Destroy the Pod, let {{< param product_short >}} create a fresh one, and check the marker
is still there. It lives on the PV, not in the container.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/persists
```

## Restart the Pod

`oc rollout restart` retires the current Pod and starts a new one from the same Deployment:

```terminal:execute
command: oc rollout restart deploy/hello-dcs
```

Wait for the new Pod to be ready:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=90s
```

```section:begin
name: breakdown-wait-for-rollout
prefix: Breakdown
title: What each part of the command does
```

- **`oc rollout status deploy/hello-dcs`** — waits until the new Pod is Ready and the
  rollout is complete.
- **`--timeout=90s`** — stops waiting after 90 seconds and reports an error,
  instead of waiting forever.

```section:end
name: breakdown-wait-for-rollout
```

{{< note >}}
**💡 Want to watch it?** In the **lower** terminal run `oc get pods,pvc -w` — you'll see the old
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

You should see `persisted-marker-42`. The Pod is new, but the marker is on the PV, so it
survived the restart.
