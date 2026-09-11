---
title: The Types, and Which Ones You Get
---

Every Service has a **selector** (which Pods) and **ports** (which port). The `type` decides
what the platform builds around that.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/types
```

![The five Service types side by side: ClusterIP with one virtual IP, headless with one DNS record per Pod, ExternalName as a CNAME, NodePort opening a port on every node, LoadBalancer needing an external provider — with Route as the supported way out on DCS](service-types.svg)

## The five

- **ClusterIP** — one stable virtual IP, load-balanced across ready Pods. The default, and
  what you want for in-cluster traffic.
- **Headless** (`clusterIP: None`) — no virtual IP. DNS returns **one record per ready Pod**,
  so the client picks. For clients that must address a *specific* replica.
- **ExternalName** — no selector, no endpoints, no proxying. A **CNAME** in cluster DNS, so
  one stable in-cluster name can point at something that lives elsewhere.
- **NodePort** — the same port opened on **every node** in the cluster.
- **LoadBalancer** — asks the infrastructure for an external address. Needs a provider that
  answers.

## What that means here

On {{< param product_short >}} you use the first three. The last two exist in the API and you
can create them, but:

- a **NodePort** puts a port on shared nodes, outside your tenant boundary, and nothing from
  outside is allowed to reach a node directly anyway — the platform's **controlled external
  load balancer** is the only edge, by security requirement;
- a **LoadBalancer** has no provider to answer it on an on-prem cluster, so it never gets an
  address.

The supported way out is a [**Route**]({{< param dcs_docs_base_url >}}/concepts/networking),
which the Core **Expose Your App** lab covers — and which needs a **PROD-type** namespace.

{{< note >}}
**💡 Tip:** you will prove both of those claims yourself on the last page, rather than taking
them on trust.
{{< /note >}}

Next: the default type, and what DNS actually returns for it.
