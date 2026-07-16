---
title: Customise It
---

The sample app reads its greeting from an [**environment variable**](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
called `GREETING`. Setting an env var is the simplest way to change how an app behaves
**without rebuilding the image** — same image, different configuration.

## Set the greeting

```terminal:execute
command: oc set env deploy/hello-dcs GREETING="Hello from the DCS Academy"
```

`oc set env` updates the Deployment's Pod template. Because that changes the desired
state, {{< param product_short >}} automatically rolls out a new Pod with the new value —
you'll watch that happen properly on a later page.

```examiner:execute-test
name: verify-env-set
title: Verify GREETING is set on the Deployment
timeout: 10
retries: .INF
delay: 2
```

The variable is now part of your Deployment's desired state. Next, let's actually reach
the app and see the greeting.
