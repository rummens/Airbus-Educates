# Autoscaling

**Setting the replica count by hand only works while you are watching.**

A **HorizontalPodAutoscaler** takes that decision over. It reads your Pods' CPU use,
compares it with the `requests` you set, and moves the replica count to hold a target.

You create one, watch it read live metrics, drive the app under load from your own terminal
and see it scale out.

Then why scale-**in** is deliberately slow, what a stabilisation window is for, and what
happens when the **namespace budget** rather than the load is the real ceiling.

The last page covers **VPA**, the other autoscaler, which tunes `requests` instead of replica
count, and why you do not point both at the same resource.

> **⚠️ Watch out:** an HPA on CPU cannot work at all without CPU `requests`. That is the
> first thing this lab checks.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~20 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** **Health & Resources** — this lab builds on the `requests` you set there.

## By the end of this lab you'll be able to

- Explain how an HPA turns CPU metrics plus your CPU requests into a replica count.
- Create an HPA with `autoscaling/v2` and read its conditions and events.
- Drive an app under load and watch it scale out.
- Explain why scale-in is slow, and what a stabilisation window protects.
- Set `maxReplicas` from the namespace budget instead of from expected load.
- Say what VPA does differently.

## What you'll do

1. **Deploy** an app with an explicit CPU request.
2. **Create** an HPA and read its status.
3. **Load** the app from your terminal and watch replicas appear.
4. **Read** the scaling events and the conditions behind them.
5. **Reason** about scale-in and about the budget ceiling.
