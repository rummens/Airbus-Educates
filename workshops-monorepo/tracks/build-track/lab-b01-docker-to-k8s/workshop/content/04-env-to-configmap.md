---
title: Env to ConfigMap
---

Third row of the mapping. The compose block

```yaml
environment:
  GREETING: "Hello from docker-compose"
```

sets the variable inline — fine for one file on one machine, but the value is welded into
that file instead of living as configuration of its own.

On Kubernetes it moves into a
[**ConfigMap**](https://kubernetes.io/docs/concepts/configuration/configmap/): a named
object holding key/value config, which any workload in the namespace can reference.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/configmap
```

## Before: whose value is it?

The Deployment you applied set no configuration at all. Check what the container actually
sees right now:

```terminal:execute
command: oc exec deploy/hello-dcs -- printenv GREETING
```

You get a greeting — but it is the one **baked into the image** with a `Dockerfile` `ENV`
line, not the one the compose file set.

That is the problem with configuration living inside an image: changing it means building a
new image.

```examiner:execute-test
name: verify-greeting-default
title: Verify the app is still on its image default greeting
timeout: 10
retries: 3
delay: 2
```

## Apply the ConfigMap

```editor:open-file
file: ~/exercises/configmap.yaml
```

It carries the same value the compose file set under `environment:`.

```terminal:execute
command: oc apply -f configmap.yaml
```

```examiner:execute-test
name: verify-configmap
title: Verify the hello-dcs-config ConfigMap exists
timeout: 10
retries: 3
delay: 2
```

## Wire it into the Deployment

A ConfigMap on its own changes nothing. The workload has to **reference** it:

```terminal:execute
command: oc set env deploy/hello-dcs --from=configmap/hello-dcs-config
```

That writes the reference into the Pod template, which is a change to the desired state — so
the Deployment **rolls out** a new Pod carrying the variable.

Watch the replacement happen in the **lower** pane. `--watch` keeps printing as Pods come
and go, and `timeout 30` stops it by itself so nothing is left running:

```terminal:execute
command: timeout 30 oc get pods -l app=hello-dcs --watch
session: 2
```

You see the old Pod go `Terminating` while a new one starts and reaches `Running`.

```examiner:execute-test
name: verify-greeting-configured
title: Verify the app serves the greeting from the ConfigMap
timeout: 20
retries: .INF
delay: 3
```

{{< warning >}}
**⚠️ Watch out:** editing a ConfigMap later does **not** restart anything by itself. The
running Pod keeps the value it started with until something triggers a new rollout.
{{< /warning >}}

Three compose lines, three Kubernetes objects, one running app. Next: the lines that do not
translate at all.
