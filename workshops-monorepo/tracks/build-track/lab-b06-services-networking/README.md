# Services & Cluster Networking

**"Just expose it" hides at least five different answers.**

A Service is not one thing. The `type` field changes what gets built, what lands in DNS, and
whether anything outside the cluster can reach it at all.

You walk the types a tenant actually uses on DCS — **ClusterIP**, **headless**,
**ExternalName** — resolving each one through cluster DNS by hand so you can see what came
back and why.

Then the two that look like the obvious way out: you apply a **NodePort** and a
**LoadBalancer**, watch exactly what each does and does not buy you here, and learn why the
platform hands you a **Route** instead.

> **💡 Tip:** the headless Service you meet here is the same one a StatefulSet needs in the
> next lab.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Expose Your App**. Helpful: **Health & Resources**, since endpoints follow readiness.

## By the end of this lab you'll be able to

- Name the Service types and say what each one is for.
- Resolve a Service through cluster DNS and explain the answer.
- Tell a ClusterIP and a headless Service apart by their DNS records.
- Use an ExternalName Service as a stable name for something elsewhere.
- Say why NodePort and LoadBalancer are the wrong tools on DCS, and what replaces them.

## What you'll do

1. **Deploy** two replicas and front them with a ClusterIP Service.
2. **Resolve** the name and get one address — the Service's own.
3. **Go headless** and get one address per Pod instead.
4. **Alias** something outside your namespace, and follow the CNAME.
5. **Apply** a NodePort and a LoadBalancer, see what happens, and clean them up.
