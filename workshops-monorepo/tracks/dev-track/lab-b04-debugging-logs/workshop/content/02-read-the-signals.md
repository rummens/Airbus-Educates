---
title: Read the Signals
---

`ImagePullBackOff` tells you *what kind* of problem you have, but not *why*. To get to the
root cause you have three lenses, each showing a different angle. Use them in order.

## Lens 1: `oc describe` — the Pod's story

[`oc describe`](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pods/)
prints everything Kubernetes knows about the Pod, and — crucially — its recent **Events**
at the bottom. That Events section is where a Pod explains itself.

```terminal:execute
command: |-
  oc describe pod -l app=hello-dcs
```

Scroll to the **Events** at the bottom. You'll see lines like:

```
  Type     Reason          Age                 From     Message
  ----     ------          ----                ----     -------
  Normal   Scheduled       2m                  ...      Successfully assigned ...
  Normal   Pulling         2m (x4 over 3m)     kubelet  Pulling image "harbor.example.dcs/dcs-academy/samples/hello-dcs:2.0"
  Warning  Failed          2m (x4 over 3m)     kubelet  Failed to pull image ".../hello-dcs:2.0": ... not found
  Warning  Failed          2m (x4 over 3m)     kubelet  Error: ErrImagePull
  Normal   BackOff         1m (x6 over 3m)     kubelet  Back-off pulling image ".../hello-dcs:2.0"
```

There's your root cause, in the `Failed` line: the image
`.../hello-dcs:**2.0**` could **not be found** in the registry. The Pod is healthy
in every other respect — it was scheduled fine; it simply can't get the image it was told
to run.

## Lens 2: `oc get events` — the namespace timeline

`oc describe` shows one Pod. `oc get events` shows *everything* happening in the
namespace, newest changes together — useful when you don't yet know which object is at
fault. Sort by time so the story reads top-to-bottom:

```terminal:execute
command: |-
  oc get events --sort-by=.lastTimestamp
```

You'll see the same `Pulling` / `Failed` / `BackOff` sequence, in context with everything
else. For a single known-bad Pod, `describe` is faster; for "something in here is wrong
but I'm not sure what", this wider view wins.

## Lens 3: `oc logs` — what the app itself said

[`oc logs`](https://kubernetes.io/docs/concepts/cluster-administration/logging/) shows the
container's own output. Try it:

```terminal:execute
command: oc logs -l app=hello-dcs --tail=20
```

This time you'll get little or nothing — perhaps:

```
Error from server (BadRequest): container "hello-dcs" in pod "hello-dcs-..." is waiting to start: trying and failing to pull image
```

That **absence of logs is itself a signal**: the container never started, so it never
logged. This confirms the problem is *before* the app runs. Logs are indispensable for a
different signature — an app that starts and then *crashes* — where you'd reach for:

- `oc logs -l app=hello-dcs --tail=20` — the current attempt.
- `oc logs <pod> --previous` — the **previous, crashed** instance's logs, gone after the restart unless you ask for them. This is the single most useful flag when a Pod is in `CrashLoopBackOff`.

{{< note >}}
Why does a missing image tag matter so much on {{< param product_short >}}? Because the
platform is **air-gapped** — nodes can only pull from the internal Harbor registry, never
the public internet. If a tag wasn't **mirrored** into Harbor, the pull fails exactly like
this. See
[working with the {{< param product_short >}} registry]({{< param dcs_docs_base_url >}}/registry/mirroring-images).
{{< /note >}}

You now have a root cause from the evidence — not a guess. Next, turn it into a hypothesis
and a fix.
