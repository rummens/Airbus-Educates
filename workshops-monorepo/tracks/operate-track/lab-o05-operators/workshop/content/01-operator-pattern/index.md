---
title: The Operator Pattern
---

Everything you have deployed so far (a Deployment, a ConfigMap, a Secret) is a single
built-in resource. A real application is usually several: a database needs storage
provisioned, a primary elected, replicas configured, backups scheduled, and all of that kept
correct as Pods restart or fail.

An [**Operator**](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is that
operational knowledge encoded once, in software.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/pattern
```

## Controller plus reconciliation

An Operator is a **controller**: a process that runs continuously, watches one kind of
object, and changes the cluster to match what that object declares. The loop is called
**reconciliation**: read the desired state, compare it with the actual state, act to close the
gap, and repeat. It runs continuously rather than once at creation.

That is the same control loop a Deployment's controller uses to keep your replica count
correct, applied to a whole application's operational knowledge instead of to a Pod count. In
practice an Operator is a specialist's runbook for one piece of software, automated.

## What it watches, what it manages

An Operator watches instances of a **Custom Resource**, which the next page defines, and
from what it finds creates and maintains the ordinary building blocks underneath: Pods, a
StatefulSet, Services and Secrets for credentials. You do not touch those. You edit the
Custom Resource, and the Operator keeps the pieces underneath correct.

![A Custom Resource declares desired state; the Operator reconciles it into managed workloads](operator-loop.svg)

{{< note >}}
**📌 Note:** the reconciliation loop never stops. If a Pod the Operator manages is deleted,
or a setting is changed out of band, the next reconciliation pass puts it back. That is the
same self-healing as a Deployment, applied to a whole application.
{{< /note >}}

You watch that loop run when you create your own Custom Resource on page 03. First, two
more terms: CRD against CR, and how an Operator gets onto the cluster.

- [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [OpenShift Operators overview](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/operators/understanding-operators#olm-what-operators-are)
