---
title: Right-Sizing
---

The oversized app is stuck because it asked for more than it needs. Let's set realistic
[requests and limits](https://docs.openshift.com/container-platform/latest/nodes/clusters/nodes-cluster-resource-configure.html)
so it fits — and understand the difference between the two.

## Requests vs limits

- **`requests`** — what the scheduler *reserves* for the container. It counts against your
  quota and decides whether the Pod fits. Set it to what the app normally uses.
- **`limits`** — the *ceiling* the container may burst to. Exceed a memory limit and the
  container is OOM-killed; exceed a CPU limit and it's throttled.

`hello-dcs` is a tiny web server — it needs very little. `deployment-probes.yaml` requests
`50m` CPU / `64Mi` memory per replica, with modest limits.

## Apply the right-sized app

```editor:open-file
file: ~/exercises/deployment-probes.yaml
```

```terminal:execute
command: oc apply -f ~/exercises/deployment-probes.yaml
```

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

Expected: the rollout completes and the Pending Pods are gone — two right-sized replicas now
schedule comfortably inside the budget. Check:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

```examiner:execute-test
name: verify-pods-running
title: All replicas Running within the namespace budget
timeout: 8
retries: 5
delay: 3
```

{{< note >}}
Same app, same budget — the only thing that changed is that you asked for what you actually
use. Right-sizing is the single most common fix for "my Pod won't schedule" on a quota'd
platform like {{< param product_short >}}.
{{< /note >}}
