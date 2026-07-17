---
title: Deploy the Built Image
---

The image you just built is a normal Harbor image now — nothing about deploying it is
different from any other image on {{< param product_short >}}. `deployment.yaml` uses the
same shape you already know from earlier labs; the only thing that's new is *whose* image
it points at.

```editor:open-file
file: ~/exercises/deployment.yaml
```

The `image:` field resolves to `{{< param dcs_registry >}}/<your session namespace>/hello-dcs-built:latest-built`
— the exact tag the build pushed on the last page, in your own session-scoped Harbor
project.

## Apply and confirm it's ready

```terminal:execute
command: envsubst < deployment.yaml | oc apply -f -
session: 1
```

```examiner:execute-test
name: verify-deployed-ready
title: Verify hello-dcs-built has 1 ready replica
timeout: 10
retries: .INF
delay: 2
```

## Reach it and confirm it's *your* build

Open a tunnel in the **lower** terminal:

```terminal:execute
command: |-
  oc rollout status deploy/hello-dcs-built --timeout=60s
  kill "$(cat /tmp/pf.pid 2>/dev/null)" 2>/dev/null || true
  oc port-forward deploy/hello-dcs-built 8080:8080 >/tmp/pf.log 2>&1 &
  echo $! > /tmp/pf.pid
  sleep 2 && echo "port-forward ready on localhost:8080"
session: 2
```

```examiner:execute-test
name: verify-app-responds
title: Verify the tunnel reaches the built app (HTTP 200)
timeout: 10
retries: .INF
delay: 2
```

Now `curl` it from the **upper** terminal:

```terminal:execute
command: curl -s localhost:8080
session: 1
```

You'll see the same `hello-dcs` greeting as in earlier labs — but this time the container
serving it came from an image *you* built, on-cluster, moments ago. Next, trigger a
rebuild and watch a second image replace this one.
