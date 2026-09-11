# Short-Lived & Helper Containers

**Not every container should run forever.**

A database migration has to finish. A report runs nightly. A setup step must complete before
the app starts. A log shipper lives beside it.

This lab covers the four shapes a Deployment cannot express: **Jobs** that run to completion,
**CronJobs** that schedule them, **init containers** that must finish first, and **sidecars**
that run alongside — which on current Kubernetes are the same API as an init container plus
one line.

You also fail a Job on purpose, to watch it reach a verdict after its retries instead of
crash-looping forever, with every attempt's logs preserved.

> **💡 Tip:** the difference between an init container and a sidecar is `restartPolicy: Always`.
> That is genuinely the whole difference.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Deploy Your First App**. Helpful: **Health & Resources**.

## By the end of this lab you'll be able to

- Run work to completion with a Job and read its result.
- Explain `backoffLimit`, `restartPolicy` and `ttlSecondsAfterFinished`.
- Schedule work with a CronJob, trigger a run by hand, and suspend it.
- Use an init container for work that must finish before the app starts.
- Say what makes a container a sidecar, and when to reach for one.

## What you'll do

1. **Run** a Job and read the output of the Pod it keeps.
2. **Fail** a Job on purpose and watch it give up.
3. **Create** a CronJob, trigger it by hand, and suspend it.
4. **Apply** a Pod with an init container and a sidecar.
5. **Read**, from the app container, a file written by a container that already exited.
