---
title: Summary
---

One label, one policy, two very different answers to the same YAML.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Read** the `dcs.airbus/namespace-type` label on two namespaces, and the admission policy
   that reads it.
2. **Deployed** an unsized workload to DEV, where it was accepted without comment.
3. **Tried** to publish it from DEV, and was refused: a Route needs a PROD-type namespace.
4. **Applied** the same unsized manifest to PROD and was refused again — at `oc apply`, with
   the failing path named.
5. **Sized** the workload, got it admitted, and published the identical Route from PROD.
6. **Compared** the two running states, and named what promotion actually is.

## Check Your Understanding

1. What technically distinguishes a PROD namespace from a DEV one here?

{{< note >}}
**❓ Answer:** a **label** — `dcs.airbus/namespace-type` — and the **admission policy** that
matches on it. Same cluster, same Kubernetes, same registry; the policy is the difference.
{{< /note >}}

2. Your Deployment is refused by PROD with a message about `resources`. Where did the
   rejection happen, and what exists afterwards?

{{< note >}}
**❓ Answer:** at **admission**, during `oc apply` — so **nothing** was created. That is the
point of an admission policy: not a Pod that starts and fails later, but a change that never
lands.
{{< /note >}}

3. Why is a Route refused in a DEV namespace?

{{< note >}}
**❓ Answer:** a Route publishes the app on the platform's **external edge** with a real
hostname. That is a production act, and a namespace for unfinished work should not be able to
make half-built things publicly reachable.
{{< /note >}}

4. Why is editing PROD directly worse than it looks, even when it works?

{{< note >}}
**❓ Answer:** the change was never tested in DEV, and the **next promotion overwrites it** —
silently. The thing that was keeping PROD working disappears, and nobody remembers it was ever
there.
{{< /note >}}

## Next Steps

**Operators on DCS** is next: the pattern behind the platform services you use, the difference
between a CRD and a CR, and the ownership split — the platform owns the operator, you own the
instance it manages.
