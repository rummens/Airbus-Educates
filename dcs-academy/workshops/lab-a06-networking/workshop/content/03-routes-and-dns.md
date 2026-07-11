---
title: Routes and DCS DNS
---

The session proxy is great for a lab, but a real published address uses an OpenShift
**[Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html)**.
Understanding the Route also means understanding the DCS traffic chain.

## The DCS traffic chain

On {{< param product_short >}}, traffic to a published app flows:

**Service → Route → External Load Balancer → client**, with **DCS-managed DNS** resolving
the Route's hostname. The Service load-balances across your Pods in-cluster; the Route
gives that Service an external hostname; the External Load Balancer at the cluster edge
accepts the outside traffic; DCS DNS points the hostname at that edge. See the
[DCS networking overview]({{< param dcs_docs_base_url >}}/networking/overview).

## A Route needs a PROD-type namespace

Here's a {{< param product_short >}}-specific rule worth remembering: **an OpenShift Route
requires a PROD-type namespace.** Kyverno enforces this — you can't publish an external
address straight out of a DEV namespace (recall the DEV/PROD distinction from the
namespaces workshop). This lab's namespace is provisioned so the Route is admitted; on the
real platform you'd create the Route in a PROD namespace.

## Create the Route

```editor:open-file
file: ~/exercises/route.yaml
```

Note it sets **no host** — OpenShift auto-assigns one that includes this namespace (e.g.
`hello-dcs-<namespace>.<apps-domain>`). Apply it:

```terminal:execute
command: oc apply -f route.yaml
```

```examiner:execute-test
name: verify-route-admitted
title: The Route is admitted with a host
args:
- hello-dcs
timeout: 20
retries: 5
delay: 2
```

Look at the host it was given:

```terminal:execute
command: oc get route hello-dcs -o jsonpath='{.spec.host}{"\n"}'
```

{{< note >}}
**DCS hostname policy:** when you *do* set a host explicitly on {{< param product_short >}},
it must include your session hostname or Kyverno rejects the Route. That's how the platform
keeps published names namespaced and predictable, with DCS-managed DNS resolving them.
{{< /note >}}
