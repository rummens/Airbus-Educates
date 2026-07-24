# Feedback Page Reference (house standard)

Every workshop ends with a **`98-your-feedback.md`** page (between the last content
page and `99-workshop-summary.md`) that invites the learner to rate the workshop.
Feedback is collected by the **DCS Academy portal** (the `/form` route, backed by
CloudNativePG in prod) and surfaced in the portal's `/admin` view, on each course's
detail page as a live star rating, and in a Grafana dashboard.

## The Feedback tab is always visible

**Pre-declare the Feedback tab** in `resources/workshop.yaml` so it is present for the
whole session, not created only on the last page. Learners can give feedback whenever
they like, and the last page simply switches to the tab.

This is safe for trophies: a lab is marked **completed only when the form is submitted**
(the portal's `POST /feedback` → `mark_progress("completed")`), never when the tab is
merely opened. A permanently-visible tab therefore does not mark labs done early.

Declare it under `spec.session.dashboards` (uses Educates `$(...)` data variables):

```yaml
# Path: spec.session
dashboards:
- name: Feedback
  url: "$(ingress_protocol)://academy.$(ingress_domain)/form?workshop=<WORKSHOP-NAME>&session=$(session_namespace)"
```

The form captures a 1–5 rating, a 1–5 clarity score, and an optional comment, stored
per course.

## Page 98 template

The page opens the already-present tab (it no longer creates it):

```markdown
---
title: Your Feedback
---

Before you finish, please take 15 seconds to rate this workshop. Your feedback
directly shapes how **{{< param product_name >}}** training improves.

## Leave your feedback

Open the **Feedback** tab (always available at the top of your session) and fill in
the short form — a rating, how clear the instructions were, and an optional comment:

```dashboard:open-dashboard
name: Feedback
```

{{< note >}}
The form has two quick 1–5 ratings and a comment box. One submit and you're done.
{{< /note >}}

```dashboard:open-dashboard
name: Terminal
```
```

## Rules

- Replace `<WORKSHOP-NAME>` with the workshop's `metadata.name` (drives per-course reporting) in the `dashboards` entry.
- No examiner checks on this page — feedback is voluntary, not verified.
- Completion/trophies fire only on form **submit**, not on opening the tab — so it is safe to leave the tab always visible.
- The form is served by the portal at `academy.$(ingress_domain)/form` (same host as the
  catalog). The path/params are stable; only the host tracks the portal.
- Keep it short: one tab, one form, back to the terminal.
