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
title: Verify the Secret exists and is referenced by the Deployment
timeout: 10
```

## Confirm injection — without leaking the value

The Deployment you applied already references this Secret via `secretKeyRef`, injecting it
as the `API_TOKEN` env var. Confirm the variable **exists** in the container without
printing what it holds:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv | grep -o '^API_TOKEN='
```

You see `API_TOKEN=` — the key is present, the value stays hidden. That's the habit:
prove wiring without exposing secrets.

```examiner:execute-test
name: verify-secret-injected
title: Verify API_TOKEN is injected into the container
timeout: 10
retries: .INF
delay: 2
```
