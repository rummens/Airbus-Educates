---
title: Config in a ConfigMap
---

A [**ConfigMap**](https://kubernetes.io/docs/concepts/configuration/configmap/) holds
non-secret configuration as key/value pairs, *outside* your image. The same image can
then run in DEV, QA and PROD with different ConfigMaps — no rebuild to change a setting.
On an air-gapped platform that matters: promoting an app moves its **config**, not a new
image.

{{< note >}}
If you've run VMs: a ConfigMap is like the answer file or config drive you attach to one
golden template — same image, environment-specific settings supplied from outside.
{{< /note >}}

## Apply the ConfigMap

You saw `configmap.yaml` on the last page — two keys the app reads, `GREETING` and
`MODE`. Apply it:

```terminal:execute
command: oc apply -f configmap.yaml
```

```examiner:execute-test
name: verify-configmap
title: Verify the ConfigMap exists
timeout: 10
```

## Wire it into the app

Now the declarative Deployment — this is the shape you revealed at the end of A01, now
written out. It consumes the ConfigMap **two ways**: `envFrom` turns every key into an
environment variable, and a volume mounts the same keys as files under `/etc/hello-dcs`.

```editor:open-file
file: ~/exercises/deployment-configured.yaml
```

Apply it (the `envsubst` fills in the registry from `DCS_REGISTRY` first — the house
pattern for any manifest with a `${VAR}`):

```terminal:execute
command: envsubst < deployment-configured.yaml | oc apply -f - && oc rollout status deploy/hello-dcs --timeout=90s
```

```examiner:execute-test
name: verify-configured
title: Verify the app runs and serves the configured greeting
timeout: 15
retries: .INF
delay: 2
```

The app now answers with **`Configured by a ConfigMap`**, and the same values are also
readable as files in `/etc/hello-dcs` — env and file, from one ConfigMap.
