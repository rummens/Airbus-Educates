# Short-Lived & Helper Containers

**Some containers are meant to stop, or to run beside your app.**

Examples: a database migration that must finish, a nightly report, a setup step before the
app starts, and a log shipper beside it.

This lab covers the four shapes a Deployment cannot express: **Jobs** that run to completion,
**CronJobs** that schedule them, **init containers** that must finish first, and **sidecars**
that run alongside, which on current Kubernetes are an init container with one extra line.

You also fail a Job on purpose and watch it stop after its retries and report `Failed`,
instead of crash-looping, with every attempt's logs preserved.

> **💡 Tip:** an init container with `restartPolicy: Always` is a sidecar; no other field
> changes.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Deploy Your First App**. Helpful: **Health & Resources**.

## By the end of this lab you'll be able to

- Run work to completion with a Job and read its result.
- Explain `backoffLimit`, `restartPolicy` and `ttlSecondsAfterFinished`.
- Schedule work with a CronJob, trigger a run by hand, and suspend it.
- Use an init container for work that must finish before the app starts.
- Say what makes a container a sidecar, and when to reach for one.

## What you'll do

1. **Run** a Job and read the output of the Pod it keeps.
2. **Fail** a Job on purpose and watch it stop after its retries.
3. **Create** a CronJob, trigger it by hand, and suspend it.
4. **Apply** a Pod with an init container and a sidecar.
5. **Read**, from the app container, a file written by a container that already exited.
