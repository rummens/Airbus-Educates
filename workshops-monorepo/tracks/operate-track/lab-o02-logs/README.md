# Logs

**Read Pod logs with `oc`, and learn where they stop being enough.**

You practise reading logs with intent: by workload rather than Pod name, across every replica,
bounded by time, and live.

Then `--previous`, which reaches the output of a container that has **already crashed and
been replaced**. That output usually contains the error that caused the crash.

Then the limit: you delete the workload and watch its logs become unreachable. `oc logs`
only works for containers that still exist.

The last page covers what fills that gap: the collector, the log store, LogQL, retention, and
the rule about secrets, which matters more once every line is centrally kept.

> **💡 Tip:** on a crash-looping Pod, run `--previous` first. It usually shows the error
> straight away.

- **Track:** Operate & Observe
- **Audience:** Intermediate
- **Duration:** ~20 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** the Core lab **Configure & Troubleshoot Your App**. Helpful: **Metrics & Monitoring**.

## By the end of this lab you'll be able to

- Explain where a container's logs live and who rotates them.
- Read logs by workload, across replicas, by time window, and live.
- Recover a crashed container's output.
- Say exactly when `oc logs` stops being able to help.
- Describe aggregated logging on DCS, and what LogQL asks for.

## What you'll do

1. **Deploy** an app and generate some log lines.
2. **Read** its logs four different ways.
3. **Crash** a workload on purpose and recover the fatal error.
4. **Delete** it and watch the logs go with it.
5. **Meet** the aggregated store that solves it.
