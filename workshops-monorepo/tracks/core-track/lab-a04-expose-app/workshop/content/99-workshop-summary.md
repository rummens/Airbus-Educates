---
title: Summary
---

Your app went from a private tunnel to a real, external address on
**{{< param product_name >}}** — with a live tab inside the session too.

## What You Did

- Fronted the app with a **Service** for a stable in-cluster address, reached by DNS.
- Learned the traffic chain: **Service → Route → external load balancer** on managed DNS.
- Created a **Route** in a PROD-type namespace and reached it **from outside** the session.
- Pinned the app as an in-session **dashboard tab** (session proxy vs Route).
- Inspected a pre-provisioned **NetworkPolicy** and confirmed **egress is blocked** (air-gapped).

## Check Your Understanding

1. How do you reach a **Service** from inside the cluster?

{{< note >}}
**Answer:** By its DNS name `‹service›.‹namespace›.svc` (optionally with the port), e.g.
`hello-dcs.<namespace>.svc:8080`. The Service load-balances to the matching Pods.
{{< /note >}}

2. What does a **Route** add that a Service alone doesn't?

{{< note >}}
**Answer:** External reachability — it publishes the Service on a public hostname on
DCS-managed DNS via the external load balancer, so clients *outside* the cluster can reach
it. A Service alone is in-cluster only.
{{< /note >}}

3. Why does a Route need a **PROD-type namespace**?

{{< note >}}
**Answer:** DCS policy only admits Routes in PROD-type namespaces — exposing a service is
a production-grade action. DEV namespaces can't create Routes. (The enforcement mechanism
is a Developer-track topic, B06.)
{{< /note >}}

4. Why did the `example.com` call **fail**?

{{< note >}}
**Answer:** DCS is air-gapped — workloads have no egress to the public internet.
Everything comes from inside the platform (Harbor images, internal mirrors).
{{< /note >}}

## Next Steps

Your app is reachable, but it still forgets everything when a Pod restarts — no storage.
**A05 — Storage** gives it a persistent volume so its data survives restarts.
