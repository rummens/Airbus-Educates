# Health & Resources

**An app with one replica, no probes and no resource numbers is not ready for production.**

You scale the sample app to four replicas and read what it costs against your
namespace budget.

Then you apply a deliberately oversized manifest and watch the **quota refuse it**, with the
Pods never scheduled, and fix it by sizing `requests` and `limits` properly.

With the app inside its budget you add **liveness** and **readiness** probes. Breaking
readiness on purpose takes one replica out of the Service while the others keep serving, and
deleting a Pod by hand shows the platform putting it back.

> **💡 Tip:** your session namespace carries a real quota, sized so that you can reach it.
> Reaching it is one of the exercises.

- **Track:** Build & Run
- **Audience:** Intermediate. You have deployed an app and read its logs before
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** the Core labs **Deploy Your First App** and **Configure & Troubleshoot Your App**. Nothing is carried over technically: this lab deploys its own app.

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
