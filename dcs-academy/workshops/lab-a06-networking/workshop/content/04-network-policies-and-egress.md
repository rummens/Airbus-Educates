---
title: Network Policies and Egress
---

Exposing an app is half the story; the other half is *controlling* traffic. On the shared,
air-gapped {{< param product_short >}} platform, two mechanisms matter:
**Network Policies** (who can talk to whom inside the cluster) and **egress restrictions**
(what can leave it).

## Network Policies (observe)

A [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
selects Pods by **label** and states which traffic is allowed. On the shared cluster the
default posture is restrictive, and policies isolate workloads from each other. One has
been pre-provisioned in your namespace — inspect it:

```terminal:execute
command: oc get networkpolicy
```

```examiner:execute-test
name: verify-netpol-present
title: A NetworkPolicy is present to inspect
args:
- allow-hello-dcs-ingress
timeout: 10
```

```terminal:execute
command: oc describe networkpolicy allow-hello-dcs-ingress
```

Read the `PodSelector` (it targets `app=hello-dcs`) and the ingress rule (allow TCP 8080).
That's how label-based isolation works: traffic is permitted only where a policy says so.

{{< note >}}
On {{< param product_short >}} today, **tenants cannot create Network Policies
themselves** — it's on the roadmap. So here you *observe* a policy the platform
provisioned rather than authoring one. When self-service lands, this becomes a hands-on
step.
{{< /note >}}

## Egress is restricted (air-gapped)

{{< param product_short >}} is air-gapped: workloads generally cannot reach the public
internet. Prove it from inside the running Pod:

```terminal:execute
command: |-
  oc exec deploy/hello-dcs -- curl -s -m 5 -o /dev/null -w '%{http_code}\n' https://example.com || echo "blocked (no response)"
```

You should see it **fail or time out** — the call doesn't leave the platform. This is why
every image comes from Harbor and every dependency is mirrored in: there is no reaching out
to the internet at runtime. Where controlled egress is needed, it's granted through quota'd
**egress IPs**, not an open door.

```examiner:execute-test
name: verify-egress-blocked
title: External egress is blocked
args:
- hello-dcs
timeout: 15
```
