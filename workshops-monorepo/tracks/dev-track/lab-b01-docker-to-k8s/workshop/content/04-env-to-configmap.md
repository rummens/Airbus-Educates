---
title: Env to ConfigMap
---

Third row of the mapping: the compose block

```yaml
environment:
  GREETING: "Hello from docker-compose"
```

sets an environment variable straight in the compose file — fine for one file on one
machine, but it means the value is baked into that file rather than living as its own,
reusable piece of configuration. On Kubernetes the same variable moves into a
[**ConfigMap**](https://kubernetes.io/docs/concepts/configuration/configmap/), which you
already used in A03 to hold this app's config — here you're recreating that same idea by
migrating it out of a compose file instead of writing it from scratch.

## Before: no GREETING set

The Deployment you applied on page 02 never set `GREETING`, so check what the container
actually sees right now:

```terminal:execute
command: |-
  oc exec deploy/hello-dcs -- sh -c 'if [ -n "$GREETING" ]; then echo "GREETING is set: $GREETING"; else echo "GREETING NOT set — app is using its built-in default"; fi'
```

```examiner:execute-test
name: verify-deployment-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

You should see **`GREETING NOT set`** — the migrated app is currently running on its
image default, not the compose value.

## Apply the ConfigMap

```editor:open-file
file: ~/exercises/configmap.yaml
```

This carries the exact value the compose file set under `environment:`. Apply it:

```terminal:execute
command: oc apply -f configmap.yaml
```

```examiner:execute-test
name: verify-configmap
title: Verify the ConfigMap exists
timeout: 10
```

## Wire it into the Deployment

The ConfigMap alone doesn't change anything yet — the Deployment has to reference it. `oc
set env --from=` copies every key in a ConfigMap (or Secret) into the container's
environment, without you having to name each key individually:

```terminal:execute
command: oc set env deploy/hello-dcs --from=configmap/hello-dcs-config
```

Because this changes the Deployment's desired state, {{< param product_short >}} rolls out
a replacement Pod carrying the new environment — the same rollout mechanic from A03, now
triggered by a migrated setting.

```examiner:execute-test
name: verify-greeting-configured
title: Verify GREETING is sourced from the ConfigMap and served
timeout: 15
retries: .INF
delay: 2
```

## After: the migrated value, live

```terminal:execute
command: |-
  curl -s "http://hello-dcs.$(oc project -q).svc:8080"
```

```examiner:execute-test
name: verify-greeting-configured
title: Verify the app serves the migrated greeting
timeout: 10
```

Before, no `GREETING`; after, **`Migrated from docker-compose`** — the exact value the
compose file set, now served from a Kubernetes object instead of a line in a compose
file. All three rows of the mapping are done. Next: the compose lines that had no clean
translation at all.
