---
title: Application Logging
---

When something misbehaves, logs are usually where you look first. A containerised app
should write its logs to standard output/error rather than to files inside the
container — Kubernetes collects that stream, and `oc logs` reads it back.

View the logs for your application:

```terminal:execute
command: oc logs deployment/hello-dcs --tail=20
```

You should see the application's startup output. Referring to the Deployment
(`deployment/hello-dcs`) rather than a specific Pod name is convenient — `oc` picks a Pod
for you, and you don't have to copy the random Pod suffix.

```examiner:execute-test
name: verify-logs
title: Verify the application is logging
args:
- hello-dcs
timeout: 10
```

## Useful Options

- `--tail=N` — show only the last N lines (as above).
- `-f` — **follow** the log live, like `tail -f`; great while reproducing a problem. (Interrupt it when done.)
- `--previous` — show logs from the *previous* container instance, essential when a Pod has crashed and restarted.
- A specific Pod (`oc logs pod/hello-dcs-…`) when you need one instance; add `-c <container>` if a Pod has more than one container.

{{< note >}}
Because Pods are replaced over time, logs viewed through a Deployment come from whichever
Pods currently exist. For durable, searchable, cross-Pod logs, {{< param product_short >}}
provides centralised logging — covered in the Observability track.
{{< /note >}}
