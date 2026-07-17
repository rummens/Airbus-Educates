# Scaling, Health & Resources

**Take your app from "it runs" to "it survives" — within the budget you're actually given.**

Your app has been running as a single, unmonitored replica since Core. This lab scales it
up, walks it straight into the namespace's resource quota so you feel the constraint bite,
right-sizes it to fit, adds liveness and readiness probes so DCS can tell a healthy replica
from a hung one, and finishes by deleting a Pod outright and watching the platform bring it
back — proof that desired state, not the Pod you happen to be looking at, is what DCS
actually guarantees.

- **Track:** Developer — Build on DCS · Lab 7
- **Audience:** Intermediate — comfortable with `oc scale` and Deployments from the Core track
- **Duration:** ~28 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** lab-a02-deploy-first-app; lab-a03-configure-troubleshoot — comfortable with Deployments, rollouts, and basic `oc` usage

## By the end of this lab you'll be able to

- Scale a Deployment and reason about replica count against a namespace quota.
- Read a namespace's `ResourceQuota` to tell whether a rollout has room to land.
- Diagnose a quota rejection from cluster events and fix it by right-sizing requests/limits.
- Add liveness and readiness probes, and explain what each one actually protects.
- Delete a Pod and confirm the platform reconciles it back to the desired replica count.

## What you'll do

Starting from a plain, single-replica `hello-dcs`, you'll scale it up until it exactly
fills the namespace budget, apply a deliberately oversized version to see the quota reject
it, fix it by setting sane `requests`/`limits`, add liveness and readiness probes and watch
one flip live, then delete a running Pod in one terminal while `watch`-ing its replacement
appear in the other.
