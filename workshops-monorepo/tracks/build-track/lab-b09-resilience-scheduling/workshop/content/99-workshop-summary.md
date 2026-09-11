---
title: Summary
---

The platform can move your Pods whenever it needs to. After this lab it can do that without
costing you anything.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Separated** involuntary disruption (a node dies) from voluntary (a drain), and matched
   each to its defence.
2. **Declared** a PodDisruptionBudget and read from its status how many Pods the platform may
   take right now.
3. **Squeezed** it to zero by scaling to the floor, and saw why a budget nobody can satisfy
   blocks the maintenance that keeps the cluster patched.
4. **Timed** a real shutdown, and found the full grace period being spent because the app
   ignores `SIGTERM`.
5. **Asked** for replicas to be spread, and chose between a spread you prefer and one you
   require.

## Check Your Understanding

1. Your PDB says `minAvailable: 2` and you run 2 replicas. What does `disruptionsAllowed`
   read, and why is that a problem?

{{< note >}}
**❓ Answer:** **0**. You promised two must stay and you only have two, so the platform may
take none. A drain **waits**, the node is not patched, and eventually somebody overrides your
budget. The fix is more replicas than the floor, not a lower floor.
{{< /note >}}

2. A Pod is deleted. What happens first — the Service stops routing to it, or the container
   is told to stop?

{{< note >}}
**❓ Answer:** **both start at once**, and neither is instant. That race is what `preStop` is
for: pausing before `SIGTERM` gives the endpoint removal time to propagate, so in-flight and
just-routed requests still find a Pod that is serving.
{{< /note >}}

3. Deleting a Pod took the whole 30-second grace period. What does that tell you about the
   image?

{{< note >}}
**❓ Answer:** it does not handle `SIGTERM`. A well-behaved app catches it, stops accepting new
connections, finishes what it has and exits — so the Pod goes **early**. Waiting the full
period means the kubelet had to `SIGKILL` it. That is a property of the image, not something a
manifest can fix.
{{< /note >}}

4. When would you choose `DoNotSchedule` over `ScheduleAnyway`?

{{< note >}}
**❓ Answer:** when co-location is genuinely unacceptable — quorum members that must not share
a failure domain — and you accept the cost: a Pod that cannot satisfy the spread stays
**Pending** rather than running in the wrong place.
{{< /note >}}

## Next Steps

That is the **Build & Run** track: your app is built, configured, sized, autoscaled, reachable,
stateful where it needs to be, and now survivable.

**Operate & Observe** picks up from here — metrics and logs for the app you just made
resilient, the tenancy and RBAC model underneath it, and the DEV to PROD promotion path.
