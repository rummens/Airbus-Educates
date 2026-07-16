---
title: Roll Out a Change
---

Configuration in a ConfigMap earns its keep when you *change* it. Let's edit the greeting,
apply it, and roll the app onto the new value — no image involved.

## Edit the ConfigMap

```editor:replace-matching-text
file: ~/exercises/configmap.yaml
match: |
  data:
    GREETING: "Configured by a ConfigMap"
replacement: |
  data:
    GREETING: "Reconfigured without a redeploy"
```

Apply the updated ConfigMap:

```terminal:execute
command: oc apply -f configmap.yaml
```

```examiner:execute-test
name: verify-configmap-updated
title: Verify the ConfigMap holds the new greeting
timeout: 10
```

## Roll the app onto it

Updating a ConfigMap does **not** restart running Pods on its own — they read their env at
start. Trigger a rollout so new Pods pick up the change:

```terminal:execute
command: oc rollout restart deploy/hello-dcs && oc rollout status deploy/hello-dcs --timeout=90s
```

{{< note >}}
Want to watch it happen? In the **lower** terminal you can run `oc get pods -w` to see the
old Pod terminate as the new one starts. Press `Ctrl-C` there when done.
{{< /note >}}

```examiner:execute-test
name: verify-updated-value
title: Verify the app now serves the updated greeting
timeout: 15
retries: .INF
delay: 2
```

The app now answers **`Reconfigured without a redeploy`** — same image, new config, live.
