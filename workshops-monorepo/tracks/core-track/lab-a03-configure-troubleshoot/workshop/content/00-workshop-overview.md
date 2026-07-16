---
title: Workshop Overview
---

In A02 you customised your app with `oc set env` — one value, on the command line. That's
fine for one setting, but a real app on **{{< param product_name >}}** has many settings,
and some of them are secret. This lab moves configuration to where it belongs — into
dedicated objects — and then, because things break in the real world, hands you a broken
app and teaches you to fix it.

{{< note >}}
**First time in one of these labs?** See the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Externalise configuration into a [**ConfigMap**](https://kubernetes.io/docs/concepts/configuration/configmap/) and consume it as env vars and a mounted file.
- Store a credential in a [**Secret**](https://kubernetes.io/docs/concepts/configuration/secret/) and inject it without printing its value.
- Trigger and watch a rollout when configuration changes.
- Diagnose a failing workload with `oc logs`, `oc describe` and `oc get events`, fix it, and verify recovery.

## Prerequisites

- **A02 — Deploy Your First App.** You know Deployments, rollouts, and the
  Deployment → ReplicaSet → Pod chain. This lab reuses the same `hello-dcs` app.

## Your Environment

A browser-based session with a split **terminal** and an **editor**. The exercise files —
a ConfigMap, a Secret, and two Deployment manifests (one working, one broken) — are in
`~/exercises`. Take a first look at the config:

```editor:open-file
file: ~/exercises/configmap.yaml
```

## Time and Difficulty

- **Estimated time:** 20 minutes
- **Difficulty:** Intermediate
