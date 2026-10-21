---
title: Fix It and Verify
---

You have named the **root cause**: the broken manifest's `envFrom` points at a **ConfigMap**
called `hello-dcs-conf`, which does not exist.

The real one is `hello-dcs-config`. On this page you **fix** the manifest and **confirm**
the app recovers.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/fix
```

## See the bad line

```editor:open-file
file: ~/exercises/broken-deployment.yaml
```

Under `containers → envFrom → configMapRef`, the `name:` reads `hello-dcs-conf`.

That **name** is the only fault in the file.

## Restore the correct desired state

Rather than hand-patch the running object, **apply** the manifest you know is correct:
`deployment-configured.yaml`, which references the right ConfigMap.

Applying the known-good **desired state** is the declarative way to recover.

Apply the good manifest (same two steps as before — fill in the registry and apply):

```terminal:execute
command: envsubst < deployment-configured.yaml | oc apply -f -
```

```section:begin
name: breakdown-apply-deployment
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < deployment-configured.yaml`** — reads the file and replaces `${DCS_REGISTRY}` with the
  registry address from your session, then prints the finished manifest.
- **`| oc apply -f -`** — the pipe hands that output to `oc apply`; `-f -` means "read
  the manifest from the pipe" instead of from a file.

```section:end
name: breakdown-apply-deployment
```

Then wait for the new Pod to become Ready:

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

```examiner:execute-test
name: verify-recovered
title: Verify the app has recovered and serves its config
timeout: 15
retries: .INF
delay: 2
```

The **Pod** is Ready again and serves `Reconfigured without a redeploy`, so it recovered
and still reads its ConfigMap.

That is the full loop:

1. **observe**
2. **hypothesise**
3. **fix**
4. **verify**
