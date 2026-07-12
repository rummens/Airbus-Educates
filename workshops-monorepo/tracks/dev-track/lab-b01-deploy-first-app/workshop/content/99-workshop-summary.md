---
title: Summary
---

You took a real application from a Harbor image to a running, reachable workload on
**{{< param product_name >}}** — and ran the developer loop end to end.

## What You Did

- Met the **hello-dcs** sample app and saw its image comes from **Harbor** via `{{< param dcs_registry >}}` (air-gapped — no external registries).
- **Deployed** it with a Deployment and confirmed the rollout.
- Gave it a stable in-cluster address with a **Service** and reached it by DNS.
- **Exposed** it to your browser through the Educates **session ingress**.
- **Iterated**: scaled to two replicas and rolled out a change without downtime.

## Challenge

Now do it yourself, unguided. **Scale the `hello-dcs` Deployment to 2 replicas.** When you
think it's done, run the check.

```examiner:execute-test
name: verify-replicas
title: Challenge — deployment scaled to 2 replicas
args:
- hello-dcs
- "2"
timeout: 5
retries: 5
delay: 2
```

{{< note >}}
**Hint:** `oc scale deployment/<name> --replicas=<n>`.
{{< /note >}}

{{< note >}}
**Reveal solution** — if you're stuck, run this:

```terminal:execute
command: oc scale deployment/hello-dcs --replicas=2
```
{{< /note >}}

## Check Your Understanding

1. The app's image is `{{< param dcs_registry >}}/samples/hello-dcs:1.0`. Why does it come from Harbor and not Docker Hub?

{{< note >}}
**Answer:** {{< param product_short >}} is air-gapped — clusters can't reach public
registries. Every image is mirrored into Harbor and pulled from there via the registry
variable, so the workshop deploys unchanged on any {{< param product_short >}} cluster.
{{< /note >}}

2. You reached the app in a browser via the **session ingress**. Why is that not the same as a production **Route**?

{{< note >}}
**Answer:** The session ingress is a temporary, per-session proxy for the lab. A real
external Route requires a **PROD namespace** (with the platform's policy and sign-off) — as
covered in Networking. DEV namespaces are self-service but not publicly routed.
{{< /note >}}

3. You scaled to two Pods without touching the Service. How does traffic reach the new Pod?

{{< note >}}
**Answer:** The Service selects Pods by label (`app: hello-dcs`). The new Pod carries that
label, so the Service picked it up automatically and load-balances across both.
{{< /note >}}

4. During `oc rollout restart`, why did the app stay reachable?

{{< note >}}
**Answer:** A Deployment rolls out gradually — new Pods must become **Ready** before old
ones are removed, and the Service only routes to Ready Pods. So there's no gap in service.
{{< /note >}}

## Next Steps

Next in the Developer track: **Configuration & Secrets** — right now the app's settings are
baked into the image and manifest. You'll move them into a **ConfigMap** and a **Secret**
and roll out a config change without rebuilding.
