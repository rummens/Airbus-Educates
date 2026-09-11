---
title: Liveness and Readiness
---

A right-sized Pod that never tells the platform whether it is working is still a gamble.

Without probes, {{< param product_short >}} will happily send traffic to a hung container, or
leave a slow-starting one out of rotation forever.

**Probes** are how a Pod answers two different questions the platform keeps asking.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/probes
```

## Two different questions

![A readinessProbe on GET / gates whether Service endpoints send traffic to the Pod; a livenessProbe on GET /healthz tells the kubelet whether to kill and restart the container](probe-flow.svg)

- **Readiness — "can you take traffic right now?"** Fail it and the Pod is pulled out of the
  Service's **endpoints**. No traffic reaches it, and the container is left alone. Pass again
  and traffic resumes. Nothing restarts.
- **Liveness — "are you still alive in there?"** Fail it repeatedly and the **kubelet** kills
  the container and starts a fresh one in the same Pod. This is for a container that is
  running but permanently stuck, which readiness alone can never fix.

{{< note >}}
**📌 Note:** there is a third kind, a [startup probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-startup-probes),
for apps that need a long time to boot. It holds liveness off until the app has started once,
so a slow start is not mistaken for a hang.
{{< /note >}}

## Read the probes you already applied

`deployment-probes.yaml` — the file from the last page — carries both: readiness on `/`, and
liveness on the app's dedicated `/healthz`.

```terminal:execute
command: oc describe deployment hello-dcs
```

Near the bottom of the output, the `Readiness:` and `Liveness:` lines name each probe's HTTP
path, port and timing (`initialDelaySeconds`, `periodSeconds`, `failureThreshold`).

```examiner:execute-test
name: verify-probes-configured
title: Verify hello-dcs has both a readiness and a liveness probe
timeout: 10
retries: 3
delay: 2
```

## Ready means "in the endpoints"

A Pod that passes readiness is added to its Service's endpoint list — the addresses traffic
is actually sent to:

```terminal:execute
command: oc get endpoints hello-dcs
```

```examiner:execute-test
name: verify-endpoints-ready
title: Verify the Service has ready Pods in its endpoints
timeout: 15
retries: .INF
delay: 2
```

Four `IP:8080` pairs, one per ready Pod. That list is exactly what readiness controls.

## Break readiness on purpose

Watch the Pods in the **lower** pane while you do this. `-o wide` adds the NODE and IP
columns, and `timeout 60` stops the watch by itself:

```terminal:execute
command: timeout 60 oc get pods -o wide -l app=hello-dcs --watch
session: 2
```

In the **upper** pane, point readiness at a path that does not exist. `oc set probe` edits a
running Deployment's probes directly, with no manifest edit:

```terminal:execute
command: oc set probe deployment/hello-dcs --readiness --get-url=http://:8080/this-path-does-not-exist
```

That is a template change, so one replacement Pod rolls out at a time. The new Pod starts,
fails its readiness check every few seconds, and never becomes Ready — so it never joins the
endpoints.

In the lower pane, one Pod's READY column sits at `0/1` while the others stay `1/1`.

```examiner:execute-test
name: verify-readiness-broken
title: Verify one Pod is held out of rotation by the broken readiness probe
timeout: 20
retries: .INF
delay: 3
```

Check the endpoints again:

```terminal:execute
command: oc get endpoints hello-dcs
```

```examiner:execute-test
name: verify-endpoints-reduced
title: Verify the broken Pod was removed from the Service endpoints
timeout: 20
retries: .INF
delay: 3
```

One address short. The broken Pod is **quarantined** while the others keep serving without
interruption.

That is the whole point of readiness: an unhealthy replica is taken out of rotation, not
paraded in front of users.

## Restore it

```terminal:execute
command: envsubst < deployment-probes.yaml | oc apply -f -
```

```examiner:execute-test
name: verify-readiness-restored
title: Verify readiness is restored and all replicas are ready again
timeout: 30
retries: .INF
delay: 2
```

All four addresses are back.

The liveness probe never came into play here: the container was always running and
answering, just not on the path readiness was pointed at. Liveness only acts when the
container itself stops answering **anything** — and it recovers by restarting, not by routing
around.
