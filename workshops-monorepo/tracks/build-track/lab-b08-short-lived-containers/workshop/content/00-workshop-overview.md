---
title: "Short-Lived & Helper Containers"
---

Everything you have deployed so far was meant to run **forever**. A Deployment's whole job
is to notice that a container stopped and start it again.

That is wrong for a lot of real work.

A database migration has to **finish**. A report runs **nightly**. A setup step must
complete **before** the app starts. A log shipper lives **beside** it.

This lab covers the shapes a Deployment cannot express, on
**{{< param product_name >}}**.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Run work to completion with a [**Job**](https://kubernetes.io/docs/concepts/workloads/controllers/job/), and read its result.
- Explain `backoffLimit`, `restartPolicy` and `ttlSecondsAfterFinished`, and watch a failing Job **give up** instead of crash-looping.
- Schedule work with a [**CronJob**](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/), and trigger a run by hand to test it.
- Use an [**init container**](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) for work that must finish before the app starts.
- Explain what makes a container a [**sidecar**](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) — and why it is the same API as an init container.

## Prerequisites

- The Core lab **Deploy Your First App** — Deployments, Pods and reading logs.
- Helpful: **Health & Resources**, since every container here still gets requests and limits.

{{< note >}}
**📌 Note:** nothing is carried over from another lab. You create everything here, in your
own namespace.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**, pointed at your own
namespace. All commands run with `oc`.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) — completions, parallelism and backoff.
- [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) — schedules, concurrency policy and history limits.
- [Sidecar Containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) — the native sidecar, and how it differs from an ordinary container.
