# Deploy Your First App

**Your own app running on DCS in a few minutes — then a look at the YAML behind it.**

This is the quick win.

You take a ready-made **image** from the DCS registry and turn it into a running
**Deployment** with a single command. Then you customise it, reach it, change it, and watch
DCS **roll out** the new version.

Last, you reveal the YAML `oc` generated and read the **Deployment → ReplicaSet → Pod**
chain behind it.

> **💡 Tip:** imperative first for speed, declarative last — so the YAML makes sense by the
> time you read it.

- **Track:** Core / Fundamentals
- **Audience:** Beginner — no prior lab required
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** None. The **What is DCS?** lab gives the background, but this lab doesn't assume it.

## By the end of this lab you'll be able to

- Deploy a Harbor image to your namespace with `oc create deployment`.
- Customise the running app with an environment variable (`oc set env`).
- Reach the app locally with `oc port-forward` and `curl`.
- Change config and watch the Deployment roll out a new version.
- Read the generated YAML and explain the Deployment → ReplicaSet → Pod ownership chain.

## What you'll do

1. **Deploy** the `hello-dcs` sample.
2. **Set** a greeting.
3. **Tunnel** to it and `curl` it.
4. **Change** the greeting and watch the rollout replace the Pod.
5. **Save and read** the Deployment YAML.

That last step is the bridge from "do this" commands to the desired-state manifests every
later lab writes.
