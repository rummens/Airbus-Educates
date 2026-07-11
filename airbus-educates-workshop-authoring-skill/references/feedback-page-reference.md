# Feedback Page Reference (house standard)

Every workshop ends with a **`98-your-feedback.md`** page (between the last content
page and `99-workshop-summary.md`) that invites the learner to rate the workshop.
Feedback is collected by the academy's **feedback-collector** service (SQLite on a
PV; see `dcs-academy/planning/feedback-capture.md`) and surfaced in `/admin` and a
Grafana dashboard.

## What the page does

It opens a **Feedback** dashboard tab pointing at the collector's form, pre-filled
with this workshop's name and the session namespace. The form captures a 1–5
rating, a 1–5 clarity score, and an optional comment — all stored per course.

## Template

```markdown
---
title: Your Feedback
---

Before you finish, please take 15 seconds to rate this workshop. Your feedback
directly shapes how **{{< param product_name >}}** training improves.

## Leave your feedback

Open the **Feedback** tab and fill in the short form — a rating, how clear the
instructions were, and an optional comment:

```dashboard:create-dashboard
name: Feedback
url: "https://feedback.{{< param ingress_domain >}}/form?workshop=<WORKSHOP-NAME>&session={{< param session_namespace >}}"
```

{{< note >}}
The form has two quick 1–5 ratings and a comment box. One submit and you're done.
{{< /note >}}

```dashboard:open-dashboard
name: Terminal
```
```

## Rules

- Replace `<WORKSHOP-NAME>` with the workshop's `metadata.name` (drives per-course reporting).
- No examiner checks on this page — feedback is voluntary, not verified.
- The collector host is `feedback.{{< param ingress_domain >}}` (edge Route). If a
  workshop runs where that Route differs, adjust the host; the path/params are stable.
- Keep it short: one tab, one form, back to the terminal.
