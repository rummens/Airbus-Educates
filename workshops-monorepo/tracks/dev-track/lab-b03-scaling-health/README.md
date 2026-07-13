# Scaling, Health & Resources

**Turn a demo workload into a resilient, quota-friendly one — scale it, right-size it, and teach the platform when it's healthy.**

Your `hello-dcs` app runs as a single replica with no health checks and modest resources — fine for a demo, not for something people rely on. In this lab you make it resilient and quota-friendly on the Digital Container Service (DCS): scale it, discover that your namespace has a real resource budget, deliberately hit that quota with an oversized request, right-size to fit, and add probes so the platform knows when the app is actually healthy.

- **Track:** Developer — Build on DCS · Lab 3 of 6
- **Audience:** Intermediate — comfortable with `oc apply`, `oc scale`, and reading Pods
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b01-deploy-first-app; assumes the Core track (lab-a02-kubernetes-essentials).

## By the end of this lab you'll be able to

- Scale a Deployment and explain how replica count meets your namespace quota
- Read a quota rejection from the events when a request is too large
- Right-size requests and limits so a workload fits its DEV namespace budget
- Add readiness and liveness probes and explain how each changes Pod behaviour

## What you'll do

Starting from the running `hello-dcs` app, you scale the Deployment and watch it meet the namespace quota, ask for too much on purpose and read the rejection in the events, right-size requests and limits to fit the `medium` budget, then add readiness and liveness probes and see the difference each makes. You finish with a workload that is production-shaped rather than demo-shaped.

## Before you start

Finish lab-b01-deploy-first-app first — this lab starts with `hello-dcs` already running (one replica, no probes). You should be comfortable with `oc apply`, `oc scale`, and reading Pods with `oc get`.
