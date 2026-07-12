---
title: Liveness & Readiness
---

Your app is scheduled and running — but "the process is up" isn't the same as "the app is
healthy and ready to serve." That's what
[probes](https://docs.openshift.com/container-platform/latest/applications/application-health.html)
are for. The manifest you just applied already has both; let's see what each one does.

## Two probes, two jobs

- **Readiness probe** — *should this Pod receive traffic yet?* While it fails, the Service
  takes the Pod **out of its endpoints**. Use it for startup and temporary "busy" states.
- **Liveness probe** — *is this Pod wedged?* If it fails repeatedly, the kubelet **restarts**
  the container. Use it to recover from hangs.

Both here are a simple HTTP GET on `/` at port 8080.

Confirm the Deployment carries both:

```examiner:execute-test
name: verify-probes
title: Deployment has readiness and liveness probes
args:
- hello-dcs
timeout: 5
```

## Watch readiness gate traffic

The Service only routes to **Ready** Pods. See the endpoints track readiness:

```terminal:execute
command: oc get endpoints hello-dcs
```

Expected: one endpoint address per Ready Pod. Now watch a rollout in a split terminal — new
Pods appear but only join the endpoints once their readiness probe passes:

```terminal:execute
command: oc get pods -l app=hello-dcs -w
session: 2
```

```terminal:execute
command: oc rollout restart deployment/hello-dcs
```

Expected: a new Pod goes `Running` but `0/1` **not ready** for a few seconds, then flips to
`1/1` **Ready** — and only then does traffic reach it. Old Pods leave only after new ones are
Ready, so there's no gap. Stop the watch with `Ctrl-C`.

Confirm the app is healthy at the intended replica count:

```examiner:execute-test
name: verify-replicas
title: Two healthy replicas ready
args:
- hello-dcs
- "2"
timeout: 5
retries: 6
delay: 3
```

{{< note >}}
Readiness protects your **users** (no traffic to a Pod that isn't ready); liveness protects
your **app** (restart a wedged one). Together they're what makes a Deployment self-managing —
the platform keeps it healthy without you watching it.
{{< /note >}}
