---
title: A ConfigMap
---

A ConfigMap holds non-secret key/value data. `configmap.yaml` has two simple keys (`GREETING`,
`FEATURE_FLAG`) and one whole file (`app.conf`).

## Create it

```terminal:execute
command: oc apply -f ~/exercises/configmap.yaml
```

```examiner:execute-test
name: verify-configmap
title: ConfigMap hello-dcs-config exists
args:
- hello-dcs-config
timeout: 5
```

## Wire it into the app

Open the wired Deployment and see how it consumes the ConfigMap — `envFrom` turns every key
into an env var, and a **volume** mounts `app.conf` as a file at `/etc/hello-dcs`:

```editor:open-file
file: ~/exercises/deployment-configured.yaml
```

Apply it and wait for the rollout:

```terminal:execute
command: oc apply -f ~/exercises/deployment-configured.yaml
```

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

## Verify delivery

Confirm the value actually reached the container — read the env var from inside a Pod:

```terminal:execute
command: oc exec deployment/hello-dcs -- printenv GREETING
```

Expected: `Hello from DCS`. And the mounted file:

```terminal:execute
command: oc exec deployment/hello-dcs -- cat /etc/hello-dcs/app.conf
```

Expected: the `greeting=…` / `feature_flag=…` lines. Confirm with the examiner:

```examiner:execute-test
name: verify-config-delivered
title: The ConfigMap value reached the container
timeout: 8
retries: 4
delay: 3
```

{{< note >}}
Same image as B01 — you changed *how it's configured*, not *what it is*. Env vars suit simple
values; a mounted file suits whole config files the app reads at startup.
{{< /note >}}
