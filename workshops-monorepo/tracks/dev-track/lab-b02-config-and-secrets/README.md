# Configuration & Secrets

**Stop baking settings into images: externalise config and inject credentials so one image runs anywhere on DCS.**

In the previous lab you deployed `hello-dcs`, but its settings were baked into the image and manifest — to change a value you'd have to rebuild. That doesn't scale, and credentials must never live in an image. In this lab you pull configuration out into a ConfigMap, inject a credential with a Secret without leaking its value, and roll out a config change on the very same image on the Digital Container Service (DCS).

- **Track:** Developer — Build on DCS · Lab 2 of 6
- **Audience:** Intermediate — you've deployed an app and are comfortable with `oc`
- **Duration:** ~35 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b01-deploy-first-app; assumes the Core track (lab-a02-kubernetes-essentials).

## By the end of this lab you'll be able to

- Move settings into a ConfigMap and deliver them as environment variables and a mounted file
- Store a credential in a Secret and inject it into a container without leaking the value
- Explain why the same image should carry different config in dev and prod
- Roll out a config change and watch old Pods give way to new ones

## What you'll do

Starting from the already-running `hello-dcs` app, you externalise its configuration into a ConfigMap (delivered both as env vars and as a mounted file), add a Secret for a credential, and trigger a rollout by changing a config value — all without rebuilding the image. Because `hello-dcs` is a static server, you verify delivery at the container boundary with `oc exec` rather than in the HTTP response.

## Before you start

Finish lab-b01-deploy-first-app first — this lab starts where it left off, with `hello-dcs` already deployed (config still baked in, which is the problem you'll solve).
