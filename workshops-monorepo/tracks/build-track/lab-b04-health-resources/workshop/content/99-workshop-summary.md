---
title: Summary
---

Your `hello-dcs` app went from one unmonitored replica to four right-sized, self-proving,
self-healing ones — all inside the budget its namespace was actually given.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Deployed** the app with no resource numbers at all, **scaled** it to four replicas, and
   read the `ResourceQuota` to see what that cost.
2. **Applied** a deliberately oversized manifest and watched the quota refuse it — the Pods
   were never even scheduled.
3. **Right-sized** `requests` and `limits` to what the app needs, recovering the rollout with
   headroom to spare.
4. **Read** the liveness and readiness probes, **broke** readiness on purpose, and watched one
   replica leave the Service endpoints while the other three kept serving.
5. **Deleted** a running Pod and watched the ReplicaSet replace it.

## Check Your Understanding

1. You scale a Deployment from 4 to 6 replicas and the rollout sticks at 5 of 6 ready. What
   is the most likely cause?

{{< note >}}
**❓ Answer:** the namespace `ResourceQuota` has no room for the sixth Pod's
`requests`/`limits` — the same admission rejection you triggered on purpose here.
`oc describe quota` and `oc get events` are where you confirm it.
{{< /note >}}

2. A Pod is running but stuck, answering nothing. Does a **readiness** probe fix that on its
   own?

{{< note >}}
**❓ Answer:** no. Readiness only decides whether the Pod is in the Service's endpoints — it
takes a stuck Pod out of rotation but leaves the hung container running forever. Only a
**liveness** probe failing repeatedly makes the kubelet kill and restart the container.
{{< /note >}}

3. What is the practical difference between `requests` and `limits` on the same container?

{{< note >}}
**❓ Answer:** `requests` is what the Pod is guaranteed, and what the scheduler and the
namespace quota count against it. `limits` is the ceiling — exceed it on memory and the
container is `OOMKilled`; exceed it on CPU and it is throttled, not killed.
{{< /note >}}

4. You delete a Pod belonging to a Deployment. What actually brings a replacement back?

{{< note >}}
**❓ Answer:** the Deployment's **ReplicaSet**, reconciling the actual replica count back up
to `spec.replicas`. Nothing you ran created that Pod — the platform's reconciliation loop did.
{{< /note >}}

## Next Steps

You set the replica count by hand. **Autoscaling** is the next lab: letting a
**HorizontalPodAutoscaler** move that number for you as load changes — and why it cannot work
at all without the `requests` you set here.
