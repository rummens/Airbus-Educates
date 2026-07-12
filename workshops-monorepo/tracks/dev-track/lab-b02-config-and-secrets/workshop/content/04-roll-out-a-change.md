---
title: Roll Out a Change
---

The payoff: change a setting and ship it **without rebuilding the image**. Update the ConfigMap,
trigger a rollout, and confirm the new value reaches the container.

## Change the value

Edit the greeting in the ConfigMap:

```editor:open-file
file: ~/exercises/configmap.yaml
```

```editor:replace-matching-text
file: ~/exercises/configmap.yaml
match: "Hello from DCS"
replace: "Hello from DCS PROD"
```

Apply the updated ConfigMap:

```terminal:execute
command: oc apply -f ~/exercises/configmap.yaml
```

{{< note >}}
Updating a ConfigMap does **not** automatically restart Pods that read it via `envFrom` — env
vars are set at container start. So you trigger a rollout to pick up the change. (Mounted-file
keys *do* update in place eventually, but a rollout is the explicit, predictable way.)
{{< /note >}}

## Roll it out

```terminal:execute
command: oc rollout restart deployment/hello-dcs
```

Watch old Pods give way to new in a split terminal:

```terminal:execute
command: oc get pods -l app=hello-dcs -w
session: 2
```

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

Stop the watch with `Ctrl-C` once the rollout completes.

## Verify the new value

```terminal:execute
command: oc exec deployment/hello-dcs -- printenv GREETING
```

Expected: `Hello from DCS PROD`. Confirm:

```examiner:execute-test
name: verify-config-delivered
title: The updated config value reached the container
args:
- "Hello from DCS PROD"
timeout: 8
retries: 4
delay: 3
```

That's the loop: **edit config → apply → roll out → verify**, same image throughout.
