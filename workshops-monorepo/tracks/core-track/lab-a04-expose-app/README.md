# Expose Your App

**From a local-only tunnel to a real, external URL on DCS-managed DNS — and a live tab for it inside your session.**

In A02 you could only reach your app through a `port-forward` tunnel, just for you, just
while the command ran. This lab gives it a proper front door: a **Service** for a stable
in-cluster address, then a **Route** that exposes it externally on DCS DNS via the
platform load balancer — reachable from a normal browser outside the session. You'll also
pin the running app as a new dashboard tab, and see why a Route needs a PROD-type
namespace.

- **Track:** Core / Fundamentals · Lab 4
- **Audience:** Intermediate — you've done A02 (A03 helpful)
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, runs in your own (PROD-type) OpenShift session namespace
- **Prerequisites:** A02 (Deploy Your First App).

## By the end of this lab you'll be able to

- Explain the DCS traffic chain: Service → Route → external load balancer with managed DNS.
- Give the app a stable in-cluster address with a Service and reach it by DNS.
- Expose the app externally with a real Route and reach it outside the session.
- Surface the running app as a new in-session dashboard tab.
- State that a Route requires a PROD-type namespace.

## What you'll do

Deploy the app in UI mode, front it with a Service, curl it by cluster DNS, then create a
Route and open its external URL, pin the app as a dashboard tab, and inspect the
platform's network posture — a pre-provisioned NetworkPolicy and blocked internet egress.
