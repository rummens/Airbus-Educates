# Configure & Troubleshoot Your App

**Grow up from ad-hoc env vars to real configuration — then break the app on purpose and learn to fix it.**

In A02 you set one value with `oc set env`. Real apps have many settings and secrets, and
they go wrong. This lab moves configuration into a **ConfigMap** and a **Secret**, wires
them into the app as environment variables and a mounted file, and rolls out a change.
Then it hands you a **broken** version and walks the debugging loop every operator lives
by: observe → hypothesise → fix → verify, using logs, events and `describe`.

- **Track:** Core / Fundamentals · Lab 3
- **Audience:** Intermediate — you've done A02
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** A02 (Deploy Your First App).

## By the end of this lab you'll be able to

- Externalise config into a ConfigMap and consume it as env vars and a mounted file.
- Store a credential in a Secret and inject it without printing its value.
- Trigger and watch a rollout when configuration changes.
- Diagnose a failing workload from logs, events and `describe`, fix it, and verify recovery.

## What you'll do

Apply a ConfigMap and Secret, wire them into a declarative Deployment, roll out a config
change, then apply a version with one seeded fault, diagnose the root cause from the
cluster's own signals, fix the single offending line, and confirm the app recovers.
