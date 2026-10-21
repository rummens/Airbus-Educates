---
title: A Secret
---

A [**Secret**](https://kubernetes.io/docs/concepts/configuration/secret/) looks like a
ConfigMap but is for sensitive values — tokens, passwords, keys. Two differences matter:

- Secret values are **base64-encoded, not encrypted**. Base64 is an encoding anyone can
  reverse. What protects a Secret is RBAC, which restricts who can read it, and keeping its
  values out of manifests and logs.
- You **never** print a Secret's value to the terminal or bake it into an image.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/secret
```

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

```section:begin
name: breakdown-inject-secret
prefix: Breakdown
title: What each part of the command does
```

- **`oc set env deploy/hello-dcs`** — changes the environment variables in the
  Deployment's Pod template.
- **`--from=secret/hello-dcs-secret`** — adds one variable for each key in the Secret (here
  `API_TOKEN`), with the value taken from the Secret.
- **`&&`** — runs the next command only if `oc set env` succeeded.
- **`oc rollout status deploy/hello-dcs`** — waits until the new Pod with the variable is Ready and the
  rollout is complete.
- **`--timeout=120s`** — stops waiting after 120 seconds and reports an error,
  instead of waiting forever.

```section:end
name: breakdown-inject-secret
```

{{< note >}}
**⚠️ Order matters.** You create the Secret **first**, then reference it. A workload that
references a Secret (or ConfigMap) that doesn't exist yet won't start.
{{< /note >}}

## Confirm injection — without leaking the value

You want to prove the `API_TOKEN` variable is present in the container **without** printing
what it holds. To do that, count its characters instead of printing it.

`printenv API_TOKEN` reads the variable inside the container and would normally print its
value. Instead of showing that value, the `|` pipe sends it to `wc -c`, which prints only
**how many characters** it received. So the value travels through the pipe but never
reaches your screen:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv API_TOKEN | wc -c
```

```section:begin
name: breakdown-count-token
prefix: Breakdown
title: What each part of the command does
```

- **`oc exec deploy/hello-dcs`** — runs a command inside a running Pod of the Deployment.
- **`--`** — ends the `oc` options; everything after it is the command to run in the
  container.
- **`printenv API_TOKEN`** — prints the value of the `API_TOKEN` variable inside the
  container.
- **`| wc -c`** — counts the characters it receives and prints only that number, so the
  value never reaches your screen.

```section:end
name: breakdown-count-token
```

You see a number (around `41` — the token's length plus the line ending). A number greater
than `1` proves the variable is set and non-empty, while the value itself stays hidden.
Use this check whenever you need to confirm a secret is set: it proves the wiring without
showing the value.

```examiner:execute-test
name: verify-secret-injected
title: Verify API_TOKEN is injected into the container
timeout: 10
retries: .INF
delay: 2
```
