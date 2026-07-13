# Networking & Exposing Apps

**Take an app only you can reach and make it reachable — the DCS way.**

You already know how to deploy a workload and reach it in-cluster. This lab is about
exposure: how traffic gets from a browser to your Pod, the path it travels on DCS, and why
some traffic simply doesn't go anywhere. You'll expose an app first through the session
proxy, then via an OpenShift Route, trace the full DCS traffic chain, and see the limits an
air-gapped platform puts on network traffic.

- **Track / module:** Core — DCS Foundations (Module A) · Lab 6 of 9
- **Audience:** Beginner — comfortable applying a Deployment and Service with `oc`
- **Duration:** ~55 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a02-kubernetes-essentials

## By the end of this lab you'll be able to

- Reach a Service in-cluster by DNS.
- Expose an app to the browser via the session proxy.
- Create an OpenShift Route and explain the DCS chain: Service → Route → External Load Balancer with DCS-managed DNS.
- Explain why a Route on DCS requires a PROD-type namespace.
- Read a Network Policy and explain how it isolates workloads, and why egress is restricted on an air-gapped platform.

## What you'll do

You'll reach the sample app in-cluster by DNS, expose it to your browser through the session
proxy (an App tab appears), then create a Route and follow the traffic chain out to the load
balancer. You'll finish by reading a Network Policy and reasoning about egress — both
observe-only, since network policy isn't self-service on DCS yet.
