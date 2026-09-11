# Health & Resources

**One replica, no probes, no resource numbers: that is a demo, not a service.**

You scale the sample app to four replicas and read what it actually costs against your
namespace budget.

Then you apply a deliberately oversized manifest and watch the **quota refuse it** — Pods
never even scheduled — and fix it by right-sizing `requests` and `limits`.

With the app fitting its budget, you give it **liveness** and **readiness** probes, break
readiness on purpose to see one replica quarantined while the others keep serving, and delete
a Pod by hand to watch the platform put it back.

> **💡 Tip:** your session namespace carries a real quota, sized so you can hit it on purpose.
> Hitting it is the lesson, not an accident.

- **Track:** Build & Run
- **Audience:** Intermediate — you have deployed an app and read its logs before
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** the Core labs **Deploy Your First App** and **Configure & Troubleshoot Your App**. Nothing is carried over technically — this lab deploys its own app.

## By the end of this lab you'll be able to

- Scale a Deployment and reason about replica count against a namespace budget.
- Read a `ResourceQuota` to tell whether a rollout has room to land.
- Diagnose a quota rejection from cluster events and fix it by right-sizing.
- Explain what readiness protects versus what liveness protects, and configure both.
- Explain what brings a deleted Pod back.

## What you'll do

1. **Deploy** the app with no resource numbers, and **scale** it to four replicas.
2. **Read** the quota to see the cost of that decision.
3. **Break** it on purpose with an oversized manifest, and diagnose the rejection.
4. **Right-size** requests and limits, recovering the rollout.
5. **Probe** it, break readiness, and watch one replica get quarantined.
6. **Delete** a Pod and watch the platform replace it.
