---
title: A Secret
---

A [**Secret**](https://kubernetes.io/docs/concepts/configuration/secret/) looks like a
ConfigMap but is for sensitive values — tokens, passwords, keys. Two differences matter:

- Secret values are **base64-encoded, not encrypted**. Base64 is just an encoding anyone
  can reverse — so a Secret is *not* safe because of base64. It's safer because access to
  Secrets is restricted by RBAC and the values are kept out of manifests and logs.
- You **never** print a Secret's value to the terminal or bake it into an image.

## Apply the Secret

Open it — note the value is written in `stringData` for readability, with a clear warning
that real secrets are created out-of-band, never committed:

```editor:open-file
file: ~/exercises/secret.yaml
```

```terminal:execute
command: oc apply -f secret.yaml
```

```examiner:execute-test
name: verify-secret
title: Verify the Secret exists
timeout: 10
```

## Wire it into the app

The Secret exists, but the app isn't using it yet. Inject its keys as environment
variables with `oc set env --from` — this adds an `API_TOKEN` env var backed by the
Secret, and rolls out a new Pod:

```terminal:execute
command: oc set env deploy/hello-dcs --from=secret/hello-dcs-secret && oc rollout status deploy/hello-dcs --timeout=120s
```

{{< note >}}
Order matters: you create the Secret **first**, then reference it. A workload that
references a Secret (or ConfigMap) that doesn't exist yet won't start.
{{< /note >}}

## Confirm injection — without leaking the value

Confirm the `API_TOKEN` variable **exists and is non-empty** in the container without
printing what it holds. This checks the value is set and reports only its **length**:

```terminal:execute
command: oc exec deploy/hello-dcs -- sh -c 'if [ -n "$API_TOKEN" ]; then echo "API_TOKEN is set — ${#API_TOKEN} characters, value hidden"; else echo "API_TOKEN is NOT set"; fi'
```

You see something like `API_TOKEN is set — 40 characters, value hidden` — the key is
present and carries a real value, but the value itself never reaches your screen. That's
the habit: prove wiring without exposing secrets.

```examiner:execute-test
name: verify-secret-injected
title: Verify API_TOKEN is injected into the container
timeout: 10
retries: .INF
delay: 2
```
