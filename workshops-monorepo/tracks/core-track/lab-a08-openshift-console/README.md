# The OpenShift Console — A Guided Tour

**Everything you did with `oc` has a UI. Here's where each command lives in the console — and when to reach for which.**

> **Rough draft.** The console-tour approach is still being decided. The in-session
> Console tab is the Kubernetes Dashboard; the real OpenShift web console can't be embedded,
> so those views are placeholder screenshots. The `oc`-parity commands are live. Complete
> enough to review.

You've deployed, configured, exposed, and persisted an app entirely from the command line.
This closing Core lab tours the OpenShift web console and maps each view — Workloads,
Networking, Storage, Config — back to the `oc` command that does the same thing, so you can
move fluently between the two and know when each is the faster tool.

- **Track:** Core / Fundamentals · Lab 8
- **Audience:** Beginner — you've done A01 (A02–A04 helpful)
- **Duration:** ~15 min
- **Format:** Guided tour + `oc`-parity checks (part screenshot-driven)
- **Prerequisites:** A01 (Deploy Your First App).

## By the end of this lab you'll be able to

- Navigate the console: perspectives, Workloads, Networking, Storage, Config.
- Map each console view to its `oc` equivalent.
- Decide when the console is faster and when the CLI wins.
