---
title: Spot the Bad Pattern
---

Let's make the leak concrete. You'll deploy a workload that carries its token the wrong way —
as a plaintext `env` literal — and then prove, from the outside, that the token is exposed.

## Look at the leaky manifest

Open the Deployment and find the problem:

```editor:open-file
file: ~/exercises/deploy-leaky.yaml
```

Look at the `env` block on the container. The credential is right there in the manifest:

```yaml
        env:
        - name: API_TOKEN
          value: "s3cr3t-plaintext-token"
```

That literal is the whole problem. It's in the file, it's in the object once applied, and it
would be in git the moment this manifest is committed. Anyone with read access to the
Deployment can see it.

## Deploy it

Apply the Deployment. The manifest's image uses `$DCS_REGISTRY`, so `envsubst` expands it
before `oc` reads it:

```terminal:execute
command: envsubst < deploy-leaky.yaml | oc apply -f -
```

Wait for the rollout to complete (the node pulls `hello-dcs` from Harbor and starts the pod):

```terminal:execute
command: oc rollout status deploy/leaky-app --timeout=60s
```

```examiner:execute-test
name: verify-leaky-running
title: The leaky deployment rolled out
args:
- leaky-app
timeout: 120
retries: .INF
delay: 3
```

## Prove the token is exposed

Now read the deployment's environment back — exactly what any teammate with `get deploy`
could do:

```terminal:execute
command: oc set env deploy/leaky-app --list | grep API_TOKEN
```

You'll see the token in clear text:

```
API_TOKEN=s3cr3t-plaintext-token
```

There it is — the literal value, readable by anyone who can view the Deployment, with no
extra permission needed. That's the leak, confirmed from outside the container.

```examiner:execute-test
name: verify-leak-visible
title: The plaintext token is visible in the env dump
args:
- leaky-app
- s3cr3t-plaintext-token
timeout: 15
```

{{< note >}}
This is the "inline in a manifest / env dump" path from page 1. The same value would also be
visible if the app printed its config to **logs**, and it would ship inside the **image** if
it were baked into a `Dockerfile ENV`. One habit — never write the literal — closes all three.
{{< /note >}}

Next, you'll move this token into a Secret and reference it instead.
