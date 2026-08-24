# Expose Your App

**From a local-only tunnel to a real, external URL on DCS-managed DNS — and a live tab for it inside your session.**

In the **Deploy Your First App** lab you could only reach your app through a `port-forward`
tunnel — only for you, only while the command ran.

This lab gives it a proper address:

- a **Service** for a stable in-cluster address;
- a **Route** that exposes it externally on DCS DNS via the platform load balancer,
  reachable from a normal browser outside the session.

You also pin the running app as a new **dashboard tab**, and see why a Route needs a
**PROD-type** namespace.

- **Track:** Core / Fundamentals
- **Audience:** Beginner — you've done the **Deploy Your First App** lab (**Configure & Troubleshoot Your App** helps)
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal, runs in your own (PROD-type) OpenShift session namespace
- **Prerequisites:** the **Deploy Your First App** lab.

## By the end of this lab you'll be able to

- Explain the DCS traffic chain: Service → Route → external load balancer with managed DNS.
- Give the app a stable in-cluster address with a Service and reach it by DNS.
- Expose the app externally with a real Route and reach it outside the session.
- Surface the running app as a new in-session dashboard tab.
- State that a Route requires a PROD-type namespace.

## What you'll do

1. **Deploy** the app in UI mode.
2. **Front** it with a Service and `curl` it by cluster DNS.
3. **Create** a Route and open its external URL.
4. **Pin** the app as a dashboard tab.
5. **Inspect** the platform's network posture — a pre-provisioned NetworkPolicy and blocked
   internet egress.
