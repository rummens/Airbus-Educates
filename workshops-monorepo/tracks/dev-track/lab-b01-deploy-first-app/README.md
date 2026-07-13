# Deploy Your First App on DCS

**The developer's first move on DCS: take an app from a registry image to a running, reachable workload in your own namespace.**

Every developer's day one on a container platform is the same — get an application off the shelf and actually running where people can reach it. This lab does exactly that on the Digital Container Service (DCS). You meet the `hello-dcs` sample app, deploy it from the DCS Harbor registry, give it a stable in-cluster address, expose it to your browser, and iterate. The manifests you build here carry through the rest of the Developer track.

- **Track / module:** Developer — Build on DCS (Module B) · Lab 1 of 6
- **Audience:** Beginner — comfortable with `oc` and the Foundations basics
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** Module A (Foundations), especially lab-a02-kubernetes-essentials · external: a DCS login, basic Linux CLI

## By the end of this lab you'll be able to

- Deploy the sample app to your DEV namespace with a Deployment and a Service
- Give a workload a stable in-cluster address and explain why it needs one
- Expose the app through the workshop session ingress and reach it in a browser
- Verify a workload is healthy from both the CLI and the web console
- Explain why self-service exposure in a DEV namespace uses the session proxy, while a real external Route requires a PROD namespace

## What you'll do

Work with the `hello-dcs` sample app end to end: deploy it from a Harbor image with a Deployment, front it with a Service for a stable address, expose it through the session ingress so you can open it in a browser, then iterate on it the way you would day to day. You leave with a running app and the core deploy workflow you'll reuse across the track.

## Before you start

This lab builds directly on Module A (Foundations). You should be comfortable running `oc`, and know what a Deployment and Service are (A02), the DEV/PROD namespace model (A03), and in-cluster networking (A06).
