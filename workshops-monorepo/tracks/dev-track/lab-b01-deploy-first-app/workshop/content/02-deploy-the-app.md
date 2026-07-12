---
title: Deploy the App
---

Time to run the app. You'll deploy it declaratively — from the manifest file — which is how
you run things for real: the file is your source of truth, kept in git, reviewed, and
re-applied anywhere.

## What's in the Manifest

The [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
describes the app you want running — which image, how many replicas, and the resources it
may use. The file is already open; note three things:

- `spec.replicas: 1` — how many Pods to run (one, to start).
- `spec.selector` / `spec.template.metadata.labels` — the label `app: hello-dcs` ties the Deployment to the Pods it manages.
- The image comes from the {{< param product_short >}} registry via `${DCS_REGISTRY}`, with explicit CPU/memory requests and limits so the app fits your namespace quota.

## Apply It

Apply the manifest. `envsubst` fills in the registry value from the `DCS_REGISTRY`
environment variable first, then pipes the result to `oc apply`:

{{< note >}}
Creating the Deployment starts a **rollout** — {{< param product_short >}} pulls the image
from Harbor and starts the Pod, which takes a few moments. The check below waits for it
automatically.
{{< /note >}}

```terminal:execute
command: |-
  envsubst < deployment.yaml | oc apply -f -
```

Expected output:

```
deployment.apps/hello-dcs created
```

## Watch the Rollout

A Deployment doesn't become ready instantly. `oc rollout status` blocks until it is:

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

You should see:

```
deployment "hello-dcs" successfully rolled out
```

```examiner:execute-test
name: verify-replicas
title: Verify the deployment is ready
args:
- hello-dcs
- "1"
timeout: 5
retries: .INF
delay: 2
```

Your app is running, described entirely by a file you can commit, review, and re-apply
anywhere. Confirm the Pod for yourself:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Expected (status `Running`, `1/1` ready):

```
NAME                         READY   STATUS    RESTARTS   AGE
hello-dcs-6b8999855c-6jjhj   1/1     Running   0          20s
```

```examiner:execute-test
name: verify-pods-running
title: Verify the pod is running
args:
- hello-dcs
- "1"
timeout: 10
```
