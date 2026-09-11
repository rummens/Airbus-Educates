---
title: Summary
---

"Expose it" is now five specific decisions instead of one vague one.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Deployed** two replicas, so every Service had more than one endpoint to show.
2. **Resolved** a **ClusterIP** Service and got exactly one address — the Service's own.
3. **Made it headless** and got one address **per ready Pod** instead, with nothing proxying.
4. **Aliased** something outside your namespace with **ExternalName**, and followed the CNAME
   through to its target.
5. **Applied** a **NodePort** and a **LoadBalancer**, saw exactly what each one does and does
   not buy you on this platform, and removed them.

## Check Your Understanding

1. You resolve a Service name and get back two addresses. What kind of Service is it?

{{< note >}}
**❓ Answer:** a **headless** Service (`clusterIP: None`). A ClusterIP Service always resolves
to exactly one address — its own virtual IP — no matter how many Pods are behind it.
{{< /note >}}

2. A teammate says their `LoadBalancer` Service "isn't working" and shows you `<pending>`
   under EXTERNAL-IP. What do you tell them?

{{< note >}}
**❓ Answer:** nothing is broken — there is no provider on an on-prem cluster to fulfil the
request, so it will stay pending forever. Outside traffic arrives through the platform's own
edge, so the object they want is a **Route** in a PROD-type namespace.
{{< /note >}}

3. Why is an ExternalName Service not enough to reach a system outside the platform?

{{< note >}}
**❓ Answer:** it only creates a **name**. {{< param product_short >}} is air-gapped and egress
is deny-by-default, so the destination still has to be allowed through the **managed egress
proxy** — a request, not a manifest.
{{< /note >}}

4. What does a headless Service give a StatefulSet that a ClusterIP Service cannot?

{{< note >}}
**❓ Answer:** a **stable per-Pod name** — `db-0.<service>.<namespace>.svc.cluster.local` —
because DNS answers per Pod rather than with one shared virtual IP. That is how a client
addresses one specific replica.
{{< /note >}}

## Next Steps

You now have a name per Pod that survives a restart. **Stateful Workloads** uses exactly that:
a **StatefulSet** with its own headless Service, a **PersistentVolumeClaim per replica**, and
an ordered rollout — the pieces an app needs when its replicas are not interchangeable.
