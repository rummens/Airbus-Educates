# Logs

**Metrics tell you that something changed. Logs tell you what happened.**

You practise reading logs with intent: by workload rather than Pod name, across every replica,
bounded by time, and live.

Then the flag that pays for the whole lab — `--previous`, which reaches the output of a
container that has **already crashed and been replaced**. That is where a crash explains
itself.

Then the limit: you delete the workload and watch its logs become unreachable. `oc logs` can
only speak for containers that still exist.

The last page is the fix — the collector, the log store, LogQL, retention, and the rule about
secrets that matters far more once every line is centrally kept.

> **💡 Tip:** reaching for `--previous` first is the difference between a two-minute diagnosis
> and twenty minutes of guessing.

- **Track:** Operate & Observe
- **Audience:** Intermediate
- **Duration:** ~20 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Configure & Troubleshoot Your App**. Helpful: **Metrics & Monitoring**.

## By the end of this lab you'll be able to

- Explain where a container's logs live and who rotates them.
- Read logs by workload, across replicas, by time window, and live.
- Recover a crashed container's output.
- Say exactly when `oc logs` stops being able to help.
- Describe aggregated logging on DCS, and what LogQL asks for.

## What you'll do

1. **Deploy** an app and make it talk.
2. **Read** its logs four different ways.
3. **Crash** a workload on purpose and recover the fatal error.
4. **Delete** it and watch the logs go with it.
5. **Meet** the aggregated store that solves it.
