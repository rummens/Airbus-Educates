---
title: Put It Under Load
---

Now make the app work for its living. You do not need a load-testing tool — a handful of
parallel request loops from your own terminal is enough to move a 100m CPU request past its
50% target.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/load
```

## Watch first

In the **lower** pane, watch the HPA and the Pods together. `timeout 240` stops the watch by
itself, so nothing is left running:

```terminal:execute
command: timeout 240 sh -c 'while true; do date +%T; oc get hpa hello-dcs --no-headers; oc get pods -l app=hello-dcs --no-headers | wc -l | sed "s/^/pods: /"; echo; sleep 10; done'
session: 2
```

## Drive the load

In the **upper** pane, start eight parallel request loops against the Service for two
minutes:

```terminal:execute
command: |-
  end=$(( $(date +%s) + 120 ))
  for i in $(seq 1 8); do
    ( while [ "$(date +%s)" -lt "$end" ]; do curl -s -o /dev/null "http://hello-dcs.$(oc project -q).svc:8080"; done ) &
  done
  wait
  echo "load finished"
```

What that does:

- **`for i in $(seq 1 8)`** — eight independent loops, so requests overlap instead of
  queuing behind one another.
- **`( … ) &`** — each loop runs in the background.
- **`wait`** — hold the terminal until they have all finished, so the command's end really is
  the end of the load.

{{< note >}}
**⏳ This takes a moment:** the HPA samples metrics every 15 seconds and scales out at most
once per interval. Expect the first extra Pod after roughly half a minute of load.
{{< /note >}}

In the lower pane you should see TARGETS climb well past `50%`, then the Pod count rise —
2, then 3, then more.

```examiner:execute-test
name: verify-hpa-scaled-up
title: Verify the HPA scaled the Deployment above its minimum
timeout: 180
retries: .INF
delay: 5
```

## What just happened

Nobody ran `oc scale`. The HPA wrote a new replica count onto the Deployment, and everything
after that was the ordinary Deployment behaviour from the earlier labs: a new ReplicaSet
Pod, a readiness probe, a Service endpoint.

```terminal:execute
command: oc describe hpa hello-dcs
```

Read the **Events** at the bottom: each scale decision is recorded with the metric that
triggered it, like `New size: 3; reason: cpu resource utilization (percentage of request) above target`.

```examiner:execute-test
name: verify-hpa-scale-event
title: Verify the HPA recorded a scaling event with its reason
timeout: 30
retries: .INF
delay: 3
```

That event trail is the first thing to read when an HPA does something surprising.
