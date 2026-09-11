---
title: Create the HPA
---

First the workload the autoscaler will own, then the autoscaler itself.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/create
```

## Deploy the app

```editor:open-file
file: ~/exercises/deployment.yaml
```

Note two things: `replicas: 1` is only a starting point, and `requests.cpu: 100m` is the
number the HPA measures against.

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f - && oc apply -f service.yaml && oc rollout status deploy/hello-dcs --timeout=120s
```

```examiner:execute-test
name: verify-app-with-requests
title: Verify hello-dcs is running with a CPU request set
timeout: 20
retries: .INF
delay: 2
```

## Apply the autoscaler

```editor:open-file
file: ~/exercises/hpa.yaml
```

Three fields carry the whole behaviour:

- **`scaleTargetRef`** — which Deployment this HPA owns.
- **`minReplicas` / `maxReplicas`** — the range it may move within (1 to 6 here).
- **`metrics`** — what it watches. One entry: CPU at **50%** average utilisation.

```terminal:execute
command: oc apply -f hpa.yaml
```

```examiner:execute-test
name: verify-hpa-created
title: Verify the HPA exists and targets the hello-dcs Deployment
timeout: 15
retries: .INF
delay: 2
```

{{< note >}}
**💡 Tip:** `oc autoscale deploy/hello-dcs --min=1 --max=6 --cpu-percent=50` creates the same
object in one line. The manifest is here so you can read what that line produces.
{{< /note >}}

## Read its status

```terminal:execute
command: oc get hpa hello-dcs
```

The **TARGETS** column reads `<current>/<target>` — for example `3%/50%`.

```examiner:execute-test
name: verify-hpa-has-metrics
title: Verify the HPA is reading live CPU metrics
timeout: 90
retries: .INF
delay: 5
```

{{< note >}}
**⏳ This takes a moment:** immediately after creation, TARGETS shows `<unknown>` until the
first metrics arrive. Give it up to a minute.
{{< /note >}}

For the reasoning behind the number, ask the HPA directly:

```terminal:execute
command: oc describe hpa hello-dcs
```

The **Conditions** and **Events** at the bottom are where an HPA explains itself:
`AbleToScale`, `ScalingActive`, and a `ScalingLimited` condition when it wants more replicas
than `maxReplicas` allows.

An idle app sits at `minReplicas`. Next, give it something to do.
