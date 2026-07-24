---
title: Fix It and Verify
---

You've named the root cause: the broken manifest's `envFrom` points at a ConfigMap called
`hello-dcs-conf`, which doesn't exist — the real one is `hello-dcs-config`. Time to fix
and confirm.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/fix
```

## See the bad line

```editor:open-file
file: ~/exercises/broken-deployment.yaml
```

Under `containers → envFrom → configMapRef`, the `name:` reads `hello-dcs-conf`. That one
wrong name is the whole fault.

## Restore the correct desired state

Rather than hand-patch the running object, apply the manifest you know is correct —
`deployment-configured.yaml`, which references the right ConfigMap. Applying the known-good
desired state is the declarative way to recover.

Apply the good manifest (same two steps as before — fill in the registry and apply):

```terminal:execute
command: envsubst < deployment-configured.yaml | oc apply -f -
```

Then wait for the new Pod to become Ready:

```terminal:execute
command: oc rollout status deploy/hello-dcs --timeout=90s
```

```examiner:execute-test
name: verify-recovered
title: Verify the app has recovered and serves its config
timeout: 15
retries: .INF
delay: 2
```

The Pod is Ready again and serving **`Reconfigured without a redeploy`** — recovered,
*and* still reading its configuration. That's the full loop: **observe → hypothesise →
fix → verify.**
