---
title: Summary
---

You've toured the whole {{< param product_name >}} lab environment. You now know your way
around the dashboard, the two terminal panes, the editor, the Console tab, and the
feedback form — everything the real labs use.

## What You Did

- Saw the two halves of the dashboard — **instructions** (left) and the **work area** tabs
  (right) — and the three clickable-action types: run a command, edit a file, verify.
- Ran a command in the **upper** terminal pane (`oc whoami`) and the **lower** pane
  (`oc status`).
- Opened a file in the **editor**.
- Visited the **Console** tab — the Kubernetes Dashboard view of your namespace.
- Submitted the **feedback** form.

## Check Your Understanding

1. The dashboard is split in two. What's on the **left**, and what's on the **right**?

{{< note >}}
**Answer:** The **left** shows the step-by-step **instructions** (the content you read and
click). The **right** is the **work area** — a set of tabs (Terminal, Editor, Console)
where the work happens, one visible at a time.
{{< /note >}}

2. The terminal is split into two panes. How does a clickable action send a command to the
   **lower** pane instead of the upper one?

{{< note >}}
**Answer:** By targeting terminal **session 2**. The upper pane is `execute-1` (session 1,
the default); the lower pane is `execute-2` (session 2). A "run a command" action with
`session: 2` runs in the lower pane.
{{< /note >}}

3. What is the **Console** tab — and what is it **not**?

{{< note >}}
**Answer:** It's the **Kubernetes Dashboard**, a visual view of the resources in your
namespace. It is **not** the OpenShift web console — that's a separate, richer tool you
tour in **A08**.
{{< /note >}}

## Next Steps

You're ready. Continue with **What is DCS?**, the first concept lab, where you'll learn
what the {{< param product_short >}} platform actually is before you deploy your first app.
