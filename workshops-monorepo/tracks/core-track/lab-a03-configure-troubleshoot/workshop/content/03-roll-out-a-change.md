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

## Nothing changed yet — see for yourself

The ConfigMap now holds the new value, but ask the **running** container what greeting it
has, and it still shows the *old* one:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv GREETING
```

Output: `Configured by a ConfigMap` — the **old** value. Updating a ConfigMap does **not**
restart running Pods, and a Pod reads its environment only once, at start. So the change
is staged, but nothing serving it has picked it up.

## Roll the app onto it

Trigger a rollout so new Pods start and read the updated ConfigMap:

```terminal:execute
command: oc rollout restart deploy/hello-dcs && oc rollout status deploy/hello-dcs --timeout=90s
```

Now ask the **new** container the same question:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv GREETING
```

Output: `Reconfigured without a redeploy` — the **new** value. Same image, same Pod
template except for the config it reads: the rollout is what turned the staged change into
a live one.

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
