---
title: Summary
---

You took an app that was only reachable in-cluster and exposed it two ways, learned the DCS
traffic chain, and saw how {{< param product_short >}} controls traffic on an air-gapped
shared platform.

## What You Did

- Reached a **Service** in-cluster by DNS (`<service>.<namespace>.svc`).
- Exposed the app to the browser via the **session proxy** (HTTPS, auth-gated).
- Created an OpenShift **Route** and learned the chain **Service → Route → External Load Balancer** with DCS-managed DNS.
- Learned that a Route requires a **PROD-type namespace**, and that explicit hosts must include the session hostname.
- Inspected a **Network Policy** and saw that **egress** is blocked on the air-gapped platform.

## Challenge

Do it yourself, unguided: the Route exists — now **confirm its host and prove the Route was
admitted**. Re-run the admission check when ready.

```examiner:execute-test
name: verify-route-admitted
title: Challenge — the Route is admitted
args:
- hello-dcs
timeout: 20
retries: 5
delay: 2
```

{{< note >}}
**Hint:** `oc get route hello-dcs` shows the host and admission status;
`oc describe route hello-dcs` shows the conditions in full.
{{< /note >}}

{{< note >}}
**Reveal** — if you deleted the Route earlier, re-create it:

```terminal:execute
command: oc apply -f route.yaml
```
{{< /note >}}

## Check Your Understanding

1. How do you reach a Service from another workload inside the cluster?

{{< note >}}
**Answer:** By its in-cluster DNS name, `<service>.<namespace>.svc` (here
`hello-dcs.<namespace>.svc:8080`). Pod IPs change; the Service name is stable.
{{< /note >}}

2. Why must a Route's host include the session hostname on {{< param product_short >}}?

{{< note >}}
**Answer:** Kyverno enforces it so published names stay namespaced and predictable, and
DCS-managed DNS can resolve them. A Route also requires a PROD-type namespace.
{{< /note >}}

3. Why does a call to `https://example.com` from inside a Pod fail?

{{< note >}}
**Answer:** {{< param product_short >}} is air-gapped — runtime egress to the internet is
blocked. Images and dependencies are mirrored into Harbor; controlled egress uses quota'd
egress IPs, not open internet access.
{{< /note >}}

## Next Steps

You've completed the core Foundations spine. Depending on your track, next up is deeper
Foundations (storage, RBAC, operators) or your track's first workshop.
