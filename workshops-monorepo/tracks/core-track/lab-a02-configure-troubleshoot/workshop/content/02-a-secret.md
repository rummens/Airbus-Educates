---
title: A Secret
---

A [**Secret**](https://kubernetes.io/docs/concepts/configuration/secret/) looks like a
ConfigMap but is for sensitive values — tokens, passwords, keys. Two differences matter:

- Secret values are **base64-encoded, not encrypted**. Base64 is just an encoding anyone
  can reverse — so a Secret is *not* safe because of base64. It's safer because access to
  Secrets is restricted by RBAC and the values are kept out of manifests and logs.
- You **never** print a Secret's value to the terminal or bake it into an image.

*[📊 See this on a slide](/slides/#/secret) — opens the **Slides** tab on this topic.*

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

You want to prove the `API_TOKEN` variable is present in the container **without** printing
what it holds. The trick is to count its characters instead of showing it.

`printenv API_TOKEN` reads the variable inside the container and would normally print its
value. Instead of showing that value, the `|` pipe sends it to `wc -c`, which prints only
**how many characters** it received. So the value travels through the pipe but never
reaches your screen:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv API_TOKEN | wc -c
```

You see a number (around `41` — the token's length plus the line ending). A number greater
than `1` proves the variable is set and non-empty, while the value itself stays hidden.
That is the habit: prove the wiring without exposing the secret.

```examiner:execute-test
name: verify-secret-injected
title: Verify API_TOKEN is injected into the container
timeout: 10
retries: .INF
delay: 2
```
