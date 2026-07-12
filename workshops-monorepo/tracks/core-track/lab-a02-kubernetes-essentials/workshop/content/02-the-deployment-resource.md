---
title: The Deployment Resource
---

The [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
is the resource you'll work with most. It describes an application you want to run: which
container image to use, how many instances (replicas) to keep running, and how to roll
out updates. You tell the Deployment your desired state, and Kubernetes works
continuously to maintain it.

Rather than the bare-bones object `oc create` generated, we'll use a proper manifest kept
as a file — the declarative approach. Open it:

```editor:open-file
file: ~/exercises/deployment.yaml
```

Note three things:

- `spec.replicas: 1` — how many Pods to run.
- `spec.selector` / `spec.template.metadata.labels` — the label `app: hello-dcs` ties the Deployment to the Pods it manages (more on labels shortly).
- The image comes from the {{< param product_short >}} registry via `${DCS_REGISTRY}`, and we set explicit CPU/memory requests and limits so the app fits your project quota.

## Apply It

Apply the manifest. `envsubst` fills in the registry value first:

{{< note >}}
Creating the Deployment starts a **rollout** — Kubernetes pulls the image and starts the
Pod, which takes a few moments. The check below waits for it automatically.
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

You now have a running application described entirely by a file you can commit, review,
and re-apply anywhere.
