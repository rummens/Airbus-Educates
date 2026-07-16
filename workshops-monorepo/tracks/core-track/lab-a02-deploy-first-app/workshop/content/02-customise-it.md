---
title: Customise It
---

The sample app reads its greeting from an [**environment variable**](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
called `GREETING`. Setting an env var is the simplest way to change how an app behaves
**without rebuilding the image** — same image, different configuration.

## Before: no GREETING set

First, look at the Deployment's environment as it is now — straight from the image, with
no `GREETING` of your own:

```terminal:execute
command: oc set env deploy/hello-dcs --list
```

You'll see the container's env with **no `GREETING` line** — the app is using its built-in
default.

```examiner:execute-test
name: verify-ready
title: Verify the Deployment is readable
timeout: 10
```

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

## After: GREETING in the desired state

List it again — now `GREETING` is there:

```terminal:execute
command: oc set env deploy/hello-dcs --list
```

Before, no `GREETING`; after, `GREETING=Hello from the DCS Academy`. That one line is now
part of your Deployment's desired state. Next, let's actually reach the app and see the
greeting.

```examiner:execute-test
name: verify-env-set
title: Verify GREETING is now listed
timeout: 10
retries: .INF
delay: 2
```
