---
title: What Is Broken?
---

The golden rule of debugging: **observe before you touch anything**. It's tempting to
start editing files, but you can't fix what you haven't diagnosed. So the first step is
always the same — ask the cluster what state your workload is actually in.

## Look at the Pods

Your terminal starts in `~/exercises`. List the Pods for the app:

```terminal:execute
command: oc get pods -l app=hello-dcs
```

Instead of the healthy `1/1 Running` you saw in earlier workshops, you'll see something
like this:

```
NAME                         READY   STATUS             RESTARTS   AGE
hello-dcs-7d9c8b6f4-abcde    0/1     ImagePullBackOff   0          2m
```

Read that line carefully — every column is a clue:

- **READY `0/1`** — zero of one containers are ready. The app is *not* serving traffic.
- **STATUS `ImagePullBackOff`** — this is the **failure signature**. Kubernetes tried to pull the container image, failed, and is now backing off (waiting longer between retries).
- **RESTARTS `0`** — the container never even started, so there's nothing to restart. That already tells you the problem is *before* the app runs — it's about getting the image, not running it.

A "failure signature" is just the recognisable shape of a problem. Learning to read
these — `ImagePullBackOff`, `CrashLoopBackOff`, `Pending`, readiness-failing — is most of
debugging. We'll map the common ones on a later page.

{{< note >}}
`oc get pods` is your first look, every time. `-l app=hello-dcs` filters to just this
app's Pods so you're not distracted by anything else in the namespace.
{{< /note >}}

## Confirm the Starting State

Let the examiner confirm what you just observed — that the app is currently **not** Ready.
This is the "before" picture; the whole workshop is about turning it green.

```examiner:execute-test
name: verify-not-ready
title: Confirm the app is currently broken (not Ready)
args:
- hello-dcs
timeout: 10
```

You've observed the symptom. **Don't fix anything yet** — next you'll gather the evidence
that turns `ImagePullBackOff` from a symptom into a root cause.
