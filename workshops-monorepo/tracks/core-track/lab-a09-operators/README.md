# Operators on DCS

**The pattern behind DCS platform services — and the one thing about it that trips people up: who owns what.**

Operators extend Kubernetes with *new* resource types that represent whole applications — a
database, a Git server — plus a controller that runs them for you. On DCS these are offered
as operators, not managed services, which changes who is responsible for the running
instance. In this lab you learn the Operator pattern, tell a CRD from a CR, meet OLM and
OperatorHub, then create a CloudNativePG Custom Resource and watch the operator reconcile it.
The core takeaway is the DCS ownership model.

- **Track / module:** Core — DCS Foundations (Module A) · Lab 9 of 9
- **Audience:** Beginner — comfortable applying manifests and inspecting resources with `oc`
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a02-kubernetes-essentials

## By the end of this lab you'll be able to

- Explain the Operator pattern: a controller reconciling a Custom Resource toward its desired state.
- Distinguish a CRD (a new resource *type*) from a CR (an *instance*).
- Explain OLM and OperatorHub at a high level.
- Create a Custom Resource and watch the operator reconcile it.
- State the DCS ownership model: the platform owns the operator; you own the instance it manages.

## What you'll do

With a lightweight CloudNativePG operator pre-installed by the platform, you'll create a
Custom Resource instance and watch the operator reconcile it into a running application —
then reason about the ownership split: the platform owns the operator, you own the instance.
This lab is also the gateway to the Operators track (Module F).
