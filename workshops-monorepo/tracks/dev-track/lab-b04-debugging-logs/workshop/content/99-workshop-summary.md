---
title: Summary
---

You walked into a broken app and walked out with a repeatable way to fix broken apps on
**{{< param product_name >}}** — a method, not a lucky guess.

## What You Did

- **Observed** the failure first — read the Pod state and named the signature (`ImagePullBackOff`).
- **Read the signals** with the three lenses: `oc describe` (events), `oc get events`, and `oc logs` (`--previous` for crashes).
- **Formed one hypothesis** from the signature — a tag not mirrored to Harbor.
- **Fixed and verified** — the smallest change (`:2.0` → `:1.0`), then confirmed recovery.

## The loop, to keep

**Observe → read the signals → hypothesise → fix → verify.** It works for every failure
signature — you just change *which lens* the evidence lives in.

| Signature | First lens |
|---|---|
| `ImagePullBackOff` / `ErrImagePull` | `oc describe` events → check the Harbor mirror |
| `CrashLoopBackOff` | `oc logs --previous` |
| `Pending` (unscheduled) | `oc describe` events → quota/resources |
| `Running` but `0/1` Ready | `oc describe` (probe events) + `oc logs` |

## Challenge

Nothing to re-break here — the challenge is the habit. Next time a Pod misbehaves, resist
the redeploy. Run `oc describe pod` and `oc logs` **first**, name the signature, then make
one change.

## Check Your Understanding

1. A Pod shows `ImagePullBackOff`. Which command shows you *why*, and where do you look?

{{< note >}}
**Answer:** `oc describe pod <name>` — read the **Events**. A pull failure is a kubelet
event (`Failed to pull image…`), not something in the app's logs.
{{< /note >}}

2. A Pod is `CrashLoopBackOff`. Why is `oc logs --previous` the right tool?

{{< note >}}
**Answer:** The current container may be too short-lived to inspect. `--previous` shows the
logs of the last **exited** container — where the app printed why it died.
{{< /note >}}

3. On {{< param product_short >}}, why is `ImagePullBackOff` so often a **mirroring** problem rather than a typo?

{{< note >}}
**Answer:** The platform is air-gapped — images only come from Harbor. If a tag wasn't
mirrored, no cluster can pull it. Promoting a version includes mirroring the tag.
{{< /note >}}

4. Why "observe before you fix" instead of just redeploying?

{{< note >}}
**Answer:** A blind redeploy often reproduces the same fault and hides the cause. Reading
the signals gives you one testable hypothesis and the smallest correct change.
{{< /note >}}

## Next Steps

Optional next: **Stateful Workloads & Storage** — apps that hold data fail in new ways.
Or jump to the **Observability** module for fleet-wide logs, metrics and alerts, so you
catch these signals before a user does.
