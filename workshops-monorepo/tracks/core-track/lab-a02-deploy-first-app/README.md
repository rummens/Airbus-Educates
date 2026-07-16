# Deploy Your First App

**Your own app running on DCS in a few minutes — then a look under the hood at the YAML that made it happen.**

This is the quick win. You take a ready-made image from the DCS registry, turn it into a
running Deployment with a single command, customise it, reach it, change it and watch DCS
roll out the new version — then reveal the YAML `oc` generated and read the
Deployment → ReplicaSet → Pod chain behind it. Imperative first for speed, declarative
last so the YAML makes sense once you've earned it.

- **Track:** Core / Fundamentals · Lab 2
- **Audience:** Beginner — you've done A01
- **Duration:** ~30 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** A01 (What is DCS?).

## By the end of this lab you'll be able to

- Deploy a Harbor image to your namespace with `oc create deployment`.
- Customise the running app with an environment variable (`oc set env`).
- Reach the app locally with `oc port-forward` and `curl`.
- Change config and watch the Deployment roll out a new version.
- Read the generated YAML and explain the Deployment → ReplicaSet → Pod ownership chain.

## What you'll do

Deploy the `hello-dcs` sample, set a greeting, tunnel to it and curl it, change the
greeting and watch the rollout replace the pod, then save and read the Deployment YAML —
the bridge from "do this" commands to the desired-state manifests every later lab writes.
