---
title: Shutting Down Well
---

A Pod being taken away is not an event, it is a **sequence**. Most dropped requests during
maintenance come from an app that ignored part of it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/shutdown
```

## The sequence

When a Pod is marked for deletion, two things start **at the same time**:

1. the Pod is removed from its Service's **endpoints**, so new traffic stops being routed to
   it;
2. the container's shutdown begins — `preStop` first, then `SIGTERM`.

Those are not instant and they are not coordinated. Traffic already in flight, and routing
that has not caught up yet, can still arrive after shutdown has started.

Then the clock: after `terminationGracePeriodSeconds`, anything still running gets `SIGKILL`.

## Read the settings you deployed

```terminal:execute
command: oc get deploy hello-dcs -o jsonpath='{.spec.template.spec.terminationGracePeriodSeconds}{"  preStop: "}{.spec.template.spec.containers[0].lifecycle.preStop.exec.command}{"\n"}'
```

```examiner:execute-test
name: verify-grace-settings
title: Verify the grace period and preStop hook are configured
timeout: 30
retries: .INF
delay: 3
```

- **`preStop: sleep 10`** — runs **before** `SIGTERM`. Its job is to cover the race above:
  keep serving for a few seconds while the endpoint removal propagates.
- **`terminationGracePeriodSeconds: 30`** — the total budget for all of it. `preStop` comes
  out of this, not on top of it.

## Time a real deletion

```terminal:execute
command: |-
  pod=$(oc get pods -l app=hello-dcs -o name | head -1)
  start=$(date +%s)
  oc delete "$pod"
  end=$(date +%s)
  echo $(( end - start )) > /tmp/shutdown-seconds.txt
  echo "deleting $pod took $(cat /tmp/shutdown-seconds.txt) seconds"
```

```examiner:execute-test
name: verify-shutdown-took-time
title: Verify the deletion waited for the shutdown sequence
timeout: 60
retries: .INF
delay: 3
```

That was not instant, and the number is probably close to the **full 30 seconds** rather than
the 10 you might expect from `preStop`.

## Why the full grace period

`hello-dcs` is a small Python web server that does **not** handle `SIGTERM`. So:

1. `preStop` sleeps its 10 seconds;
2. `SIGTERM` arrives — and the process ignores it;
3. the kubelet waits out the rest of the grace period;
4. `SIGKILL` ends it.

A well-behaved app shortens step 3 to nothing: it catches `SIGTERM`, stops accepting new
connections, finishes the requests it already has, and exits. The Pod disappears **early**,
and nobody notices the maintenance.

{{< note >}}
**💡 Tip:** this is a property of your **image**, not of your manifest. `preStop` and the grace
period give an app room to shut down well; they cannot make an app that ignores `SIGTERM`
behave.
{{< /note >}}

## The replacement

```terminal:execute
command: oc get pods -l app=hello-dcs
```

```examiner:execute-test
name: verify-replacement-ready
title: Verify the Deployment replaced the deleted Pod
timeout: 90
retries: .INF
delay: 3
```

Back to three, exactly as in **Health & Resources** — but now you know what the 30 seconds in
the middle were spent on.

{{< warning >}}
**⚠️ Watch out:** a grace period that is too **short** is worse than one that is too long.
`SIGKILL` in the middle of a request drops it, and in the middle of a write can leave state
half-finished. Size it from what your app actually needs to finish.
{{< /warning >}}

Next: making sure the platform's maintenance cannot reach all your replicas at once.
