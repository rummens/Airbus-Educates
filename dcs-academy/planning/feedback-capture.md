# End-of-Workshop Feedback Capture

**Status:** **BUILT (Option A+B)** — service live + verified on CRC. · **Owner:** DCS Academy · **Applies to:** every workshop

## As built (2026-07)

- **Collector service** `feedback-collector` (`images/feedback-collector/`): stdlib-only Python + **SQLite on a PVC**. Endpoints: `/form` (HTML form), `POST /feedback`, `POST /analytics` (Educates webhook sink), `/admin` (token-gated report: per-course + aggregate + comments), `/metrics` (Prometheus), `/healthz`. CNPG swap seam via `DATABASE_URL` (SQLite is v1).
- **Both Likert + comments stored**: the form captures a 1–5 rating, a 1–5 clarity score, and a comment — all in one table. One-click ratings (analytics events) are also stored.
- **Chart**: `dcs-academy-workshops/templates/60-feedback-collector.yaml` (PVC, Deployment `Recreate`+RWO, Service, edge Route `feedback.<ingressDomain>`, admin-token Secret) + `61-feedback-monitoring.yaml` (ServiceMonitor). Toggle/config under `values.feedback`. TrainingPortal `spec.analytics.webhook.url` wired to the collector.
- **Reporting**: `/admin` HTML view **and** a Grafana dashboard (`dcs-academy-platform/dashboards/feedback.json`) — avg rating/clarity by course, response/comment counts, aggregate, responses-over-time — via the existing Thanos datasource.
- **Per-workshop page**: `98-your-feedback.md` (opens the **Feedback** tab → the form) added to A01–A09; house-standard template in the authoring skill; review-skill rubric checks for it.
- **Verified on CRC**: form serves, POST stores, analytics webhook stores, `/metrics` per-course correct, `/admin` gated (401 without token), and **data persists across pod restart**.

**Prod prerequisite:** make the `ghcr.io/rummens/feedback-collector` package **public** (like the other academy images) so clusters pull it without a secret; set `feedback.adminToken` (or `existingSecret`); ensure user-workload monitoring is on for the ServiceMonitor.

---

## Original proposal (for reference)

**Status:** Proposed (not yet built) · **Owner:** DCS Academy · **Applies to:** every workshop

## Goal

At the end of **every** workshop, capture:
1. A **Likert rating** (1–5) — "How would you rate this workshop?" (and optionally a second scale: "How clear were the instructions?").
2. An **optional free-text comment**.

Must work on the **fully air-gapped** platform — no external form services (Google Forms, Typeform, etc. are unreachable from a session). Everything stays in-cluster.

## Constraint: what Educates gives us

Educates has a built-in **analytics webhook** on the `TrainingPortal` (`spec.analytics.webhook.url`) plus a **`report-analytics-event`** clickable action. Any page can fire a custom event (with an arbitrary JSON payload) that the portal POSTs to an in-cluster URL. Session/workshop/user identifiers are attached automatically. This is the air-gapped-friendly backbone — no per-workshop bespoke UI needed for the rating.

The gap: clickable actions can't collect **free text** (no text-input widget). The comment needs a small form. Two ways to close that gap — see options.

## Recommended approach (lazy, reuses what's there)

**A. Likert via analytics events (zero extra UI).**
Add a standard final page `98-your-feedback.md` to every workshop (between the last content page and `99-workshop-summary.md`, or fold into the summary). It renders five clickable rating buttons; each fires a `report-analytics-event` with `{ event: "workshop.rating", workshop: "<name>", score: N }`. One click = rating captured. Optionally a second row for a "clarity" score.

**B. Comment via a tiny in-cluster collector + form tab.**
Stand up one small **feedback-collector** service (in the academy namespace), exposed to sessions as a **dashboard tab** ("Feedback") via a session ingress. It serves a minimal HTML form (the 1–5 scale + a comment textarea) and a `POST /feedback` endpoint that stores `{workshop, session, score, comment, ts}`. The same collector can **also** be the analytics webhook target, so ratings from (A) and comments from (B) land in one store. This keeps everything in-cluster and needs exactly one small deployment.

If (B) is too much for v1, ship (A) alone (ratings only) and add the comment form later — the analytics event already carries the signal that matters most.

## Reporting

- Store to a lightweight DB (a **CloudNativePG** instance — dogfoods Module F) or even append-only to a PVC for v1.
- Surface in **Grafana** (already wired up on this platform — see the Grafana/OpenShift monitoring setup): a dashboard of average score per workshop, response count, and a comment feed. Ratings-over-time flags workshops that need work.

## Standard feedback page — template to add to every workshop

Add as a house standard (author it once in the `airbus-educates-workshop-authoring` skill as a page template, like the mandatory intro page):

```
# Your Feedback

Your rating helps us improve {{< param product_name >}} training. It takes 10 seconds.

**How would you rate this workshop?**
[ ★ 1 ] [ ★ 2 ] [ ★ 3 ] [ ★ 4 ] [ ★ 5 ]   ← each button = a report-analytics-event action

**How clear were the instructions?**
[ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

Optional comment: open the **Feedback** tab to leave a note.   ← only if option B is built
```

(The star buttons are `report-analytics-event` clickable actions; the comment line is only present when the collector/form tab exists.)

## Build checklist

- [ ] Decide v1 scope: **(A) ratings only** vs **(A)+(B) ratings + comments**. *(Recommend A+B if the collector is cheap; else A now, B next.)*
- [ ] Add the `98-your-feedback.md` page template to the authoring skill (mandatory page, like the intro page) + a review-skill rubric check ("every workshop has the feedback page").
- [ ] Backfill the page into A01/A02 (built) and include it in every planned workshop.
- [ ] If (B): build the `feedback-collector` (form tab + `POST /feedback` + analytics-webhook sink) and deploy it to the academy namespace; wire `TrainingPortal.spec.analytics.webhook.url` to it.
- [ ] Storage: PVC (v1) or CloudNativePG.
- [ ] Grafana dashboard: avg score/workshop, response count, comments.
- [ ] Privacy: feedback is tied to session/user IDs by Educates — decide whether to anonymise at collection (recommend storing aggregate + comment, dropping user ID) for candid feedback.

## Open questions

- Is the analytics webhook enabled on the DCS-hosted portal, or does that need a platform change?
- One shared collector for the whole academy, or per-portal?
- Anonymous vs attributed feedback — affects candour and any data-classification handling.
