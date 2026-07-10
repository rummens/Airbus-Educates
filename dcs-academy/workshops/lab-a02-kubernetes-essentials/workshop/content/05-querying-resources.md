---
title: Inspecting Resources
---

Most of your time on {{< param product_short >}} is spent *looking at* resources —
checking state, diagnosing problems. `oc` gives you a few complementary tools; knowing
which to reach for saves a lot of time.

## `oc get` — the quick list

`oc get` lists resources. Add `-o wide` for more columns:

```terminal:execute
command: oc get pods -l app=hello-dcs -o wide
```

The wide output adds the Pod's IP address and the node it runs on:

```
NAME                         READY   STATUS    RESTARTS   AGE   IP            NODE
hello-dcs-6b8999855c-6jjhj   1/1     Running   0          5m    10.128.2.14   worker-1
```

For the full stored object, ask for YAML:

```terminal:execute
command: oc get deployment hello-dcs -o yaml
```

You'll see far more than you wrote — Kubernetes fills in defaults (from the resource type
and from your namespace's limits) and adds a `status` section tracking live state. This
is normal: you specify intent, Kubernetes fills in the rest.

## `oc describe` — the human-readable summary

`oc describe` formats an object for people and, crucially, lists recent **events** at the
bottom — your first stop when something isn't working:

```terminal:execute
command: oc describe deployment/hello-dcs
```

```examiner:execute-test
name: verify-deployment-exists
title: Verify the deployment is inspectable
args:
- hello-dcs
timeout: 10
```

## `oc explain` — the field reference

When you're not sure what a field means or what's allowed, `oc explain` documents the
schema without leaving the terminal:

```terminal:execute
command: oc explain deployment.spec.strategy
```

Between `get` (state), `describe` (summary + events), and `explain` (schema), you can
understand almost any resource without a browser.
