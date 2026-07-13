# Namespaces & the Prod/Dev Model

**Meet DCS's DEV and PROD namespaces — and feel the difference first-hand.**

On DCS the namespace is the unit you consume: this is Namespace as a Service (NaaS). Every
namespace is either a DEV or a PROD type, and they are deliberately not the same — PROD is
guarded so that what runs in production stays controlled and repeatable. In this lab you
create both kinds side by side in your own virtual cluster and see the difference live: PROD
enforces a Kyverno admission policy and rejects a non-compliant change; DEV doesn't.

- **Track:** Core — DCS Foundations · Lab 3 of 9
- **Audience:** Beginner — comfortable applying a Deployment with `oc`
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in a per-session virtual cluster (gives you cluster-admin)
- **Prerequisites:** lab-a02-kubernetes-essentials

## By the end of this lab you'll be able to

- Explain Namespace as a Service (NaaS) — why the namespace is the DCS consumption unit.
- Distinguish the DEV and PROD namespace lifecycle types and the controls that differ.
- Deploy a workload into a DEV namespace.
- See how a PROD namespace enforces stricter policy (Kyverno) and rejects a non-compliant change.
- Explain promotion — why you move work DEV → PROD rather than editing PROD in place.

## What you'll do

You'll create a DEV namespace and deploy into it, then create a PROD namespace and try the
same change — watching the Kyverno policy block it. From there you'll reason about
promotion: why the right move is to carry a known-good workload from DEV to PROD rather than
hand-editing production.

## Before you start

This lab is unique in the Core track: it gives you your own throwaway virtual cluster with
cluster-admin, so you can create real namespaces and apply real policies without touching
anyone else's work. Nothing you do here affects the shared platform.
