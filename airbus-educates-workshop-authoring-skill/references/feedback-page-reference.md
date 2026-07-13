# Feedback Page Reference (house standard)

Every workshop ends with a **`98-your-feedback.md`** page (between the last content
page and `99-workshop-summary.md`) that invites the learner to rate the workshop.
Feedback is collected by the **DCS Academy portal** (the `/form` route, backed by
CloudNativePG in prod) and surfaced in the portal's `/admin` view, on each course's
detail page as a live star rating, and in a Grafana dashboard.

## What the page does

It opens a **Feedback** dashboard tab pointing at the portal's form, pre-filled
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
url: "https://academy.{{< param ingress_domain >}}/form?workshop=<WORKSHOP-NAME>&session={{< param session_namespace >}}"
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
- The form is served by the portal at `academy.{{< param ingress_domain >}}/form`
  (same host as the catalog — the standalone `feedback.*` collector was absorbed into
  the portal). The path/params are stable; only the host tracks the portal.
- Keep it short: one tab, one form, back to the terminal.
