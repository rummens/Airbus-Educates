---
title: Deploy It
---

One command gets your app running. A [**Deployment**](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
is how you tell {{< param product_short >}} "keep one copy of this image running for me" —
it pulls the image, starts a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/),
and keeps it alive.

## Create the Deployment

```terminal:execute
command: oc create deployment hello-dcs --image=${DCS_REGISTRY}/samples/hello-dcs:1.0
```

You'll see `deployment.apps/hello-dcs created`. Behind that one line, DCS pulled the
image from Harbor and scheduled a Pod to run it.

{{< note >}}
The image pull can take a few seconds the first time. The check below waits for the app
to become available, so give it a moment — it turns green once one copy is running.
{{< /note >}}

```examiner:execute-test
name: verify-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

## See it running

Don't take the green check's word for it — look at what's actually running:

```terminal:execute
command: oc get deployment,pods -l app=hello-dcs
```

You'll see the Deployment reporting `1/1` READY and one Pod in `Running` — your app, live
on {{< param product_short >}}.

```examiner:execute-test
name: verify-ready
title: Verify hello-dcs is running (1 ready replica)
timeout: 10
retries: .INF
delay: 2
```

That's your app running on {{< param product_short >}} — from an image, to a scheduled,
self-healing workload, with a single command. Next, make it yours.
