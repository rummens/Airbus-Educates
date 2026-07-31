# Workshop Plan: lab-a00-environment-tour

## 1. Workshop Metadata

- **Name:** `lab-a00-environment-tour`
- **Title:** Your Workshop Environment
- **Description:** A quick tour of the DCS Academy lab environment — the split terminals, the code editor, the Kubernetes Dashboard console tab, and the feedback form — so you know your way around before you start deploying.
- **Duration:** 10m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** None (very first lab in the academy; can precede A01)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#follow-ups-from-2026-07-16-review-queued--details-not-yet-authored-author-still-reviewing)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split` (the tour teaches the upper/lower split)
- Editor: enabled (the tour opens a file)
- Web console: **enabled** — this is the **Kubernetes Dashboard** console tab (NOT the OpenShift web console; that is toured in A08). Requires `security.token.enabled: true`.
- Examiner: `enabled: true`
- Image registry / docker / vcluster / git: **not** needed
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **vcluster decision:** `false` — no cluster-scoped work; UI orientation only in the plain session namespace.
- **lifecycle label:** `dev` — creates no Route/Ingress.

## 3. Learning Objectives

By the end the learner can:
- Describe the two-part dashboard layout (instructions | work area) and the three clickable-action types (run a command, edit a file, verify/examiner).
- Use the **split terminal** — run a command in the upper (`execute-1`) and lower (`execute-2`) pane.
- Open a file in the **editor** via a clickable action.
- Switch to the **Console** tab (Kubernetes Dashboard) and understand it as a read-only visual view of the session namespace.
- Find and use the **Feedback** form.

## 4. Connection to Previous Workshop

None — this is the entry point (numbered A00 so A01–A08 keep their numbers). Assumes no prior knowledge. Deliberately lighter than A01, which starts the actual concepts.

## 5. Exercise Files to Create

- `exercises/README.md` — a short friendly welcome file, used as the demo file the editor page opens (so the editor tour shows real content).
- `workshop/content/02-the-dashboard-layout/dashboard-layout.svg` — copy of `docs/dcs-academy/img/dashboard-layout.svg` (air-gapped: local page-bundle asset, never an external image).

## 6. Workshop Instruction Pages

(2026-07-31: page **01-quick-actions** inserted after learner feedback that the clickable
boxes were not understood until chapter 3; the later pages were renumbered.)

- **`00-workshop-overview.md`** — mandatory intro page + first-time note (links the portal Help page). Frames the lab as a UI tour; What You'll Learn; Prerequisites (none); Your Environment; 10m / beginner. No actions.
- **`01-quick-actions.md`** — the clickable boxes, up front: the four kinds (run a command / open-edit a file / verify / open a tab), then one of each tried on this page — `echo … > ~/exercises/quick-actions.txt` → examiner `verify-quick-action` → `editor:open-file` on that file → back to the Terminal. Ends with the Slides box, now that "how to get back" has been taught.
- **`02-the-dashboard-layout/index.md`** — the split screen: **Instructions** (left) | **Work area** tabs (right), tab-by-tab table incl. Feedback. Embed the layout SVG. Tip `{{< note >}}` (watch which tab is visible). No commands.
- **`03-the-terminal.md`** — the split terminal (upper `execute-1` / lower `execute-2`), starts in `~/exercises`, uses `oc`. Guided:
  - upper: `oc whoami` → examiner `verify-whoami` (identity non-empty).
  - lower (`session: 2`): `oc status` → examiner `verify-status` (runs against the project).
- **`04-the-editor.md`** — the VS Code editor on `~/exercises`; `editor:open-file` on `exercises/README.md`; explain that editor actions open files and make edits for you. No terminal command (no examiner needed — editor action only).
- **`05-the-console.md`** — the **Console** tab = the **Kubernetes Dashboard**, a read-only visual view. `dashboard:reload-dashboard` to the session-namespace workloads view (empty now — honest: you deploy in A01). Short note that it is not the OpenShift web console (toured in the Console track) + that its permission warnings are expected. Then `dashboard:open-dashboard` Terminal to return.
- **`98-your-feedback.md`** — standard feedback page; doubles as the tour of the Feedback tab (the learner actually submits).
- **`99-workshop-summary.md`** — recap + bridge to A01. **Check Your Understanding** (3 Q): the two dashboard halves; the two terminal panes and how to target the lower one; what the Console tab is (and what it is NOT).

## 7. Terminal Working Directory Tracking

- Split terminal; both panes start in `~/exercises`. No `cd`. Commands namespace-scoped to the session namespace (default context), no `-n` needed. Upper = session 1, lower = session 2 — tracked independently.

## 8. Design Notes

- **Numbered A00** on purpose — inserts before A01 without renumbering A01–A08 (avoids a second rename pass / deploy churn).
- **Console = Kubernetes Dashboard, not OpenShift console.** A00 tours the session-chrome + k8s Dashboard; **A08** tours the real OpenShift web console (embedding-limited — see the `educates-openshift-console-limitation` memory). Keep the two distinct in wording.
- Only 2 commands (both reused from A01's examiner tests) — the lab is a UI tour, not a concept lab, so it stays ~10m and the examiner-per-command rule is satisfied cheaply.
- References the learner-facing `docs/dcs-academy/environment-guide.md` + its `dashboard-layout.svg`; the SVG is copied into the page bundle for air-gap.
- Establishes the click-don't-type habit before A01/A02.
