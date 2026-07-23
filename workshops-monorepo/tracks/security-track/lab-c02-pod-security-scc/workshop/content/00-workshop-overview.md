---
title: Workshop Overview
---

Welcome to this workshop, part of **{{< param product_name >}}**. Every workload you run on
{{< param product_short >}} is admitted under a **restricted** security policy — root is off the
table, privilege is off the table, and images must not assume they own the box. In this lab you'll
see *why* that policy exists, watch a Pod that ignores it get **rejected the moment you apply it**,
and then fix the Pod so it complies.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

The rules come from two standard OpenShift mechanisms — **Security Context Constraints (SCC)** and
the **Pod Security Standards (PSA)** — working together at admission time. They are not
{{< param product_short >}} inventions, so we link them to their upstream docs. What *is*
{{< param product_short >}}-specific is the **governance** behind them: the platform sets a secure
floor for every tenant, and raising it is a deliberate, governed exception — never a self-service
toggle.

## What You'll Learn

By the end of this workshop you will be able to:

- Explain what **SCC** and the **Pod Security Standards** are, and why {{< param product_short >}}
  runs tenant workloads under **restricted**.
- Describe the **arbitrary-UID** requirement and why an image must not assume a fixed UID (least of all root).
- Deploy a Pod with a correct restricted `securityContext` and confirm the SCC that admitted it.
- Read an admission **rejection** and identify which control was violated.
- Remediate a workload's `securityContext` (`runAsNonRoot`, drop `ALL` capabilities,
  `seccompProfile`, no privilege escalation) so it is admitted.
- Recognise when **baseline** is legitimately needed, and that raising the policy is a governed
  **Security Exception**.

## Prerequisites

- **lab-a01-kubernetes-essentials** — you should be comfortable applying a manifest with `oc apply`
  and reading `oc get` / `oc describe`.
- Familiarity with [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) and basic
  [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) usage.

No prior experience with SCC, PSA, or `securityContext` is assumed — we introduce all three.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} session namespace. That namespace already **enforces the restricted
policy** — exactly as a real tenant namespace does — so the rejections you'll see here are the same
ones you'd hit in production. Commands are run with `oc` in the terminal.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Managing Security Context Constraints (OpenShift)](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html)
- [Pod Security Standards (Kubernetes)](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Configure a Security Context for a Pod or Container (Kubernetes)](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

## Leaving the workshop

Want to switch labs or come back later? This opens the **{{< param product_name >}}**
portal in a **new browser tab** — your session here keeps running.

```dashboard:open-url
url: "https://academy.{{< param ingress_domain >}}/"
title: Open the DCS Academy portal
```
