---
title: Form a Hypothesis
---

You've observed the signature (`ImagePullBackOff`) and read the evidence (the `Failed`
event: image `hello-dcs:2.0` **not found**). Now connect them into a single sentence you
can act on:

> **Hypothesis:** the Deployment asks for image tag `:2.0`, but that tag was never
> mirrored into the {{< param product_short >}} Harbor registry — so the pull fails. The
> fix is to point the Deployment at a tag that *is* in Harbor.

That's the whole art of it: **signature + evidence → a specific, testable cause**. A good
hypothesis names one thing to change and predicts what success looks like (here: the image
pulls, the Pod goes Ready).

## Map the Signature

The reason this loop is worth learning is that the *same four steps* diagnose very
different faults. What changes is which signature you see and where the evidence lives:

| Signature | Usual cause | Where the evidence is |
|---|---|---|
| `ImagePullBackOff` / `ErrImagePull` | Wrong image name or tag; tag not mirrored to Harbor; missing pull secret | `oc describe` **Events** (`Failed to pull`) |
| `CrashLoopBackOff` | App starts, then exits with an error (bad config, missing env, failed connection) | `oc logs --previous` |
| `Pending` (never scheduled) | Not enough quota/resources; unschedulable | `oc describe` **Events** (`FailedScheduling`) |
| `Running` but `0/1` READY | Readiness probe failing — app up but not healthy | `oc describe` (probe events) + `oc logs` |

Our case is the first row. Notice how the *evidence location* follows from the signature:
a pull failure is a kubelet event, so you look in `describe`; a crash is the app talking,
so you look in `logs`.

## A Familiar Move

If you've run VMs, this is the same instinct as **reading the boot console before you
rebuild the machine**. You don't wipe and redeploy on a hunch — you look at what the system
is telling you, form one hypothesis, and make the smallest change that tests it. Same
discipline here; the console is just `oc describe` and `oc logs`.

With a hypothesis in hand, you're ready to make the fix — and, just as importantly, to
verify it.
