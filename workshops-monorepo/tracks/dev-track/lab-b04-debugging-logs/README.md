# Debugging & Logs

**A colleague's change broke the app and they went home — diagnose it and bring it back using only the tools DCS already gives you.**

Sooner or later every developer has to figure out why an app *isn't* working. In this lab you arrive to a `hello-dcs` app that is already deployed and already broken, and your job is to find out why and recover it on the Digital Container Service (DCS). The real skill isn't memorising commands — it's running a repeatable loop: observe, hypothesise, fix, verify. You practise it on one seeded fault, but the method diagnoses any outage.

- **Track:** Developer — Build on DCS · Lab 4 of 6
- **Audience:** Intermediate — comfortable deploying and exposing an app with `oc`
- **Duration:** ~35 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b01-deploy-first-app; assumes the Core track (lab-a02-kubernetes-essentials).

## By the end of this lab you'll be able to

- Read a workload's state with `oc get`, `oc describe`, `oc get events` and `oc logs`
- Recognise common failure signatures — `ImagePullBackOff`, `CrashLoopBackOff`, `Pending`, readiness-failing — and map each to its likely cause
- Turn a signature plus evidence into a specific, testable hypothesis
- Apply a fix and verify the app has recovered
- Run the observe → hypothesise → fix → verify loop on any broken workload

## What you'll do

You land on a `hello-dcs` app stuck in `ImagePullBackOff`. Working the four-step loop, you read the signals with `oc get`, `oc describe` and `oc logs`, trace the root cause to an image tag that was never mirrored into Harbor, form a hypothesis, apply the one-line fix, and confirm the Pod goes Ready and serves again.

## Before you start

Finish lab-b01-deploy-first-app first — you should already be comfortable deploying and exposing an app with `oc`. This lab reuses those commands together, as a diagnostic method.
