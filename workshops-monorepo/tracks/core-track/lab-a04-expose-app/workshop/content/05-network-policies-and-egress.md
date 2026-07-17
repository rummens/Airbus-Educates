---
title: Network Policies & Egress
---

Exposing an app is only half the network story. The other half is what's *allowed* — and
on a shared, air-gapped platform, the defaults are restrictive on purpose.

## Network policies isolate workloads

A [**NetworkPolicy**](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
controls which traffic may reach a Pod, matched by **labels**. On {{< param product_short >}}
the posture is locked down by default, and one has been pre-provisioned for your app.

{{< note >}}
**Observe only.** Tenants can't self-create NetworkPolicies on {{< param product_short >}}
yet — it's on the roadmap. So here you *inspect* one rather than author it.
{{< /note >}}

```terminal:execute
command: oc describe networkpolicy allow-hello-dcs-ingress
```

```examiner:execute-test
name: verify-networkpolicy
title: Verify the NetworkPolicy is present
timeout: 10
```

Read the `PodSelector` (`app=hello-dcs`) and the ingress rule (TCP 8080): it says *only*
traffic to port 8080 on the app's Pods is allowed in.

## Air-gapped means no way out

{{< param product_short >}} is air-gapped: workloads have **no route to the public
internet**. Prove it — try to reach an external site from inside the app's Pod:

```terminal:execute
command: oc exec deploy/hello-dcs -- python3 -c "import urllib.request; urllib.request.urlopen('https://example.com', timeout=5)"
```

It **fails** (times out or refuses) — exactly as intended. By default an app gets
everything it needs from *inside* the platform (images from Harbor, packages from internal
mirrors), never the open internet.

{{< note >}}
**There is a controlled exception.** Specific external resources *can* be reached through
a managed egress proxy — but this is **not on by default**. Each destination must be
**explicitly whitelisted and enabled** (via a request to the platform team), so egress
stays deny-by-default and every allowed route is deliberate and auditable. "Air-gapped"
means *no open path out*, not *no path ever*.
{{< /note >}}

```examiner:execute-test
name: verify-egress-blocked
title: Verify egress to the public internet is blocked
timeout: 15
```

{{< note >}}
On a lab cluster that happens to have internet access, this check may not pass — the real
{{< param product_short >}} platform blocks it. That's an environment difference, not a
mistake on your part.
{{< /note >}}
