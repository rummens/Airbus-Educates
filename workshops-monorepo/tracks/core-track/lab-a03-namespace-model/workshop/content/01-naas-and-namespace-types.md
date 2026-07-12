---
title: Namespace as a Service
---

Before you create anything, it's worth understanding *why* {{< param product_short >}}
hands you namespaces the way it does — because it shapes everything else on the platform.

## Namespace as a Service

A [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
is Kubernetes' isolation boundary — a place where your workloads, config, and quota live,
separate from everyone else's. On {{< param product_short >}} the namespace is the thing
you actually consume: you don't get a cluster, you get **namespaces**. This is
**[Namespace as a Service (NaaS)]({{< param dcs_docs_base_url >}}/naas/dev-prod-lifecycle)** —
the platform runs the cluster; you request namespaces and fill them with your apps.

{{< note >}}
"Project" is just OpenShift's word for a namespace — the same object, not a separate
thing. You'll see both terms; they mean the same boundary.
{{< /note >}}

## DEV vs PROD: two lifecycle types

Every {{< param product_short >}} namespace is one of two **lifecycle types**, and the
difference is the whole point of this workshop:

| | **DEV** | **PROD** |
|---|---|---|
| Purpose | fast iteration, experimentation | running the real thing |
| **Admission policy** | **no Kyverno gate** | **Kyverno policies enforced** |
| Change style | edit freely | **promote** a tested manifest in |
| Proxy-Cached Catalog | usable | **not** usable |

The headline row is **admission policy**. PROD namespaces enforce
[Kyverno](https://kyverno.io/docs/) policies — rules checked *at the moment you apply a
resource* — so a non-compliant workload is rejected before it ever runs. DEV namespaces
have no such gate, so you can move fast. Everything else (change control, catalog access)
follows from that same "PROD is guarded, DEV is free" idea.

Think of DEV as your workshop bench and PROD as the certified production line: you build
and tinker on the bench, then move a finished, inspected part onto the line — you don't
re-machine parts on the running line.

## Your virtual cluster

This lab runs in a **virtual cluster** — a private, throwaway cluster inside your session
where *you* are the admin. That's what lets you create both namespace types and a policy,
which you couldn't do in a shared tenant. Confirm it's ready:

```terminal:execute
command: oc get namespaces
```

You should see the built-in namespaces (like `default`, `kube-system`). The list works —
that's all we need for now; you'll add your own next.

```examiner:execute-test
name: verify-oc-namespaces
title: Virtual cluster is ready
timeout: 30
retries: .INF
delay: 2
```
