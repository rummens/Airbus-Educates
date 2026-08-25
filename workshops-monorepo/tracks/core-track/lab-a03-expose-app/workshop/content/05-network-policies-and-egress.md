---
title: Network Policies & Egress
---

Exposing an app is one part of networking. The other part is which traffic is *allowed* to
and from the app. On a shared, air-gapped platform the defaults are restrictive on purpose.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/network
```

## Network policies isolate workloads

A [**NetworkPolicy**](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
controls which traffic may reach a Pod, matched by **labels**. On {{< param product_short >}}
traffic is restricted by default, and one policy has been pre-provisioned for your app.

{{< note >}}
**⚠️ Observe only.** Tenants can't self-create NetworkPolicies on {{< param product_short >}}
yet — it's on the roadmap. So here you *inspect* one rather than author it.
{{< /note >}}

```terminal:execute
command: oc describe networkpolicy allow-hello-dcs-ingress | tee ~/exercises/netpol.txt
```

```examiner:execute-test
name: verify-networkpolicy
prefix: After the describe
title: Verify you inspected the NetworkPolicy
timeout: 10
```

Read the `PodSelector` (`app=hello-dcs`) and the ingress rule (TCP 8080): it says *only*
traffic to port 8080 on the app's Pods is allowed in.

## Air-gapped means no outbound internet access

{{< param product_short >}} is air-gapped: workloads have **no route to the public
internet**. Confirm this by trying to reach an external site from inside the app's Pod.
`oc exec` runs a command inside a running container; `deploy/hello-dcs` selects a Pod from
that Deployment; everything after `--` is the command to run in the container (here a short
Python one-liner, where `-c` passes the code as a string):

```terminal:execute
command: oc exec deploy/hello-dcs -- python3 -c "import urllib.request; urllib.request.urlopen('https://example.com', timeout=5)" > ~/exercises/egress.txt 2>&1; echo "exit=$?" >> ~/exercises/egress.txt; cat ~/exercises/egress.txt
```

It **fails** (it times out or is refused), which is the intended result. By default an app
gets everything it needs from inside the platform (images from Harbor, packages from
internal mirrors), never from the open internet.

{{< note >}}
**📌 There is a controlled exception.** Specific external resources *can* be reached through
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
**⚠️ Watch out:** on a lab cluster that happens to have internet access, this check may not pass — the real
{{< param product_short >}} platform blocks it. That's an environment difference, not a
mistake on your part.
{{< /note >}}
