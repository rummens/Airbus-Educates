---
title: The Two That Look Right
---

On most clusters these two are the answer to "make it reachable from outside". On
{{< param product_short >}} neither works, and the way to see that is to apply them.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/refused
```

## NodePort: a port on every node

```editor:open-file
file: ~/exercises/service-nodeport.yaml
```

```terminal:execute
command: oc apply -f service-nodeport.yaml && oc get svc hello-dcs-nodeport
```

```section:begin
name: breakdown-apply-nodeport
prefix: Breakdown
title: What each part of the command does
```

- **`oc apply -f service-nodeport.yaml`** — creates the NodePort Service from the file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc get svc hello-dcs-nodeport`** — shows the new Service; the `PORT(S)` column includes the node port it was given.

```section:end
name: breakdown-apply-nodeport
```

It is **created**, and the `PORT(S)` column shows something like `8080:30113/TCP`. That
second number is a port now listening on **every node in the cluster**.

```examiner:execute-test
name: verify-nodeport-assigned
title: Verify the NodePort Service was assigned a node port
timeout: 15
retries: .INF
delay: 2
```

It is the wrong tool on {{< param product_short >}} for two reasons:

- **It is not yours.** The port is on shared cluster nodes, outside your tenant boundary, and
  it collides with every other tenant who wants that number.
- **Nothing can reach it.** Outside traffic on {{< param product_short >}} arrives through a
  **controlled, monitored external load balancer**, and that edge is a security requirement.
  Node addresses are not routable for you to hand out.

## LoadBalancer: a request nobody answers

```editor:open-file
file: ~/exercises/service-loadbalancer.yaml
```

```terminal:execute
command: oc apply -f service-loadbalancer.yaml && oc get svc hello-dcs-lb
```

```section:begin
name: breakdown-apply-loadbalancer
prefix: Breakdown
title: What each part of the command does
```

- **`oc apply -f service-loadbalancer.yaml`** — creates the LoadBalancer Service from the file.
- **`&&`** — run the next command only if `oc apply` succeeded.
- **`oc get svc hello-dcs-lb`** — shows the new Service, including its `EXTERNAL-IP` column.

```section:end
name: breakdown-apply-loadbalancer
```

Look at `EXTERNAL-IP`:

```
NAME           TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)
hello-dcs-lb   LoadBalancer   10.217.4.90    <pending>     8080:30732/TCP
```

**`EXTERNAL-IP` stays `<pending>`.** A LoadBalancer Service is a request to the
infrastructure for an address, and it needs a provider to fulfil it. On an on-prem cluster
without one, nothing answers.

```examiner:execute-test
name: verify-loadbalancer-pending
title: Verify the LoadBalancer Service never receives an external address
timeout: 30
retries: 3
delay: 5
```

{{< warning >}}
**⚠️ Watch out:** the Service is not in an error state. It reports as healthy and does
nothing, which makes it harder to spot. A `<pending>` external IP here means the wrong Service
type was chosen; there is no fault to debug.
{{< /warning >}}

## What you use instead

A [**Route**]({{< param dcs_docs_base_url >}}/concepts/networking). It is the OpenShift object
that publishes a Service through the platform's own edge:

1. your **Service** keeps doing its in-cluster job;
2. a **Route** names a host on the platform's domain;
3. the platform's **external load balancer** terminates traffic and forwards it in.

One constraint, which the **DEV vs PROD Namespaces** lab covers: a Route needs a
**PROD-type** namespace. This session is DEV-type, which is why you did not create one
here.

Creating a Route is the Core **Expose Your App** lab.

## Clean up the two that do not work

```terminal:execute
command: oc delete svc hello-dcs-nodeport hello-dcs-lb
```

```examiner:execute-test
name: verify-wrong-types-removed
title: Verify both unsupported Services are gone
timeout: 15
retries: .INF
delay: 2
```

A permanently pending LoadBalancer left behind is confusing for the next person in the
namespace.
