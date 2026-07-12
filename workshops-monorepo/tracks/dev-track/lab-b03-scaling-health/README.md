# lab-b03-scaling-health — Scaling, Health & Resources

Developer-track (Module B) workshop. The learner makes the `hello-dcs` sample app resilient
and quota-friendly: scale it, hit the namespace quota with an oversized request, right-size
requests/limits, and add readiness + liveness probes.

- **Track:** Developer (`academy.dcs/track: dev`), order 30 · **Difficulty:** intermediate · **Duration:** 40m
- **Prerequisites:** B01 (Deploy Your First App).
- **Sample app:** `hello-dcs` (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`), pre-deployed via `session.objects` (1 replica, no probes — the learner adds them).
- **Budget:** `medium` — deliberately sized so an oversized request is rejected, then right-sized.
- **Session:** native OpenShift namespace (no vcluster); the namespace budget *is* the quota.
