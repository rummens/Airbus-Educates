# Cloud Development with OpenShift Dev Spaces

**Stop deploying *to* DCS and start developing *on* it — a browser IDE that runs inside the cluster, fully air-gapped.**

So far you've deployed applications to the Digital Container Service (DCS). This lab is about developing on it. OpenShift Dev Spaces gives every developer a consistent, browser-based IDE that runs inside the cluster — no laptop toolchain, no reaching out to the internet, fully policy-compliant on an air-gapped platform. You'll launch (or tour) a workspace from a devfile, change and run the sample app inside the cluster, and place Dev Spaces alongside the Educates editor and a plain `oc apply`.

- **Track:** Developer — Build on DCS · Lab 6 of 6
- **Audience:** Intermediate — comfortable deploying an app with `oc`
- **Duration:** ~45 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b01-deploy-first-app; assumes the Core track (lab-a02-kubernetes-essentials); lab-a09-operators recommended for the "platform installs it, you use it" idea.

## By the end of this lab you'll be able to

- Explain what Dev Spaces is and why it fits an air-gapped platform
- Read a devfile — the reproducible spec for a workspace — that points at the sample app
- Launch (or tour) a workspace and run the app inside the cluster
- Place Dev Spaces next to the Educates editor and a plain `oc apply` deploy, and pick the right tool for a task

## What you'll do

You start from a devfile that describes a reproducible workspace built on a Harbor-mirrored universal developer image, launch an in-cluster IDE, change the `hello-dcs` sample app and run it inside the cluster, then compare Dev Spaces with the other ways you've edited and deployed code in this track. If the cluster has a live Dev Spaces instance you'll drive a real workspace; if not, the identical steps run as a guided, screenshot-driven tour — the devfile and concepts are the same either way.

## Before you start

Finish lab-b01-deploy-first-app first. lab-a09-operators is recommended for the framing that the platform installs Dev Spaces cluster-wide and your session simply consumes it.
