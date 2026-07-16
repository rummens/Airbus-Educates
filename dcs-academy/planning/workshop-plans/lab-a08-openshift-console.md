# Workshop Plan: lab-a08-openshift-console

## 1. Workshop Metadata

- **Name:** `lab-a08-openshift-console`
- **Title:** The OpenShift Console — A Guided Tour
- **Description:** Everything you did with `oc` has a UI. Tour the OpenShift web console — Workloads, Networking, Storage, Config — mapped one-to-one to the commands you already know, and learn when the console is the faster tool.
- **Duration:** 25m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A02 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split` (used for the `oc` parity call-outs)
- Editor: enabled (view resources, no editing)
- OpenShift access: enabled; `security.token.enabled: true`
- **Console/Dashboard tab:** the session "Console" tab is the **k8s Dashboard usable as the session SA** (real OpenShift console cannot be iframed — see Config note / Design Notes).
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **Screenshot assets:** page-bundle images of the real OpenShift console views (perspectives, Topology, Route, PVC, ConfigMaps/Secrets) — air-gapped, embedded locally via `{{< baseurl >}}`, for the parts that can't be shown in the session tab. Placeholders to be produced.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Navigate the OpenShift web console — perspectives, Workloads, Networking, Storage, ConfigMaps/Secrets.
- Map each console view to the `oc` command that does the same thing (console ↔ CLI parity).
- Decide when the console is the faster tool and when the CLI wins.

## 4. Connection to Previous Workshop

**What the learner already knows** (from the A01–A05 happy path):
- Deployed an app (A02), configured/fixed it (A03), exposed it with a Route (A04), gave it a PVC (A05) — all with `oc`.
- These are the *exact* objects the console tour points at, so the learner sees their own work in the UI.

**What is new in this workshop:**
- The web console as a navigation surface, and the habit of translating between UI and `oc`.

**What should NOT be re-taught:**
- No re-teaching of Deployments, Routes, PVCs, ConfigMaps/Secrets — those were A02–A05. This lab *locates* them in the console, it doesn't re-explain them.

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the OpenShift Console workshop." Tour + parity call-outs; no manifests to apply.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame the tour as "the UI for what you already know."
**Content outline:**
- `{{< param product_name >}}` framing; "everything you did with `oc` has a UI." What You'll Learn; time 25m / beginner.
- Console/perspectives concept → upstream OpenShift docs. Note the session Console tab is the k8s Dashboard; some real-console views are shown as annotated screenshots. No actions.

### 01-perspectives-and-workloads.md
**Purpose:** Orient in the console and find the app from A02.
**Content outline:**
- Open the Console tab (`dashboard:open-dashboard`). Perspectives (Developer vs Administrator) and when to use each; the project/namespace selector matches the session namespace.
- **Workloads** — Deployments/Pods; Topology view — locate the app deployed in A02.
- `oc` parity call-out: return to terminal, `oc get deploy,pods` (`terminal:execute`) → examiner check: succeeds — same objects the console shows. Console → [upstream](https://docs.openshift.com/container-platform/latest/web_console/web-console-overview.html).

### 02-networking-and-storage.md
**Purpose:** Find the Route (A04) and the PVC (A05) in the console.
**Content outline:**
- **Networking** — Services & Routes; find the Route created in A04, click through to the external URL. Annotated screenshot of the real console's Route view if the session tab can't show it.
- **Storage** — PersistentVolumeClaims; find the PVC from A05, read its storage class and bound state.
- `oc` parity call-outs: `oc get route` and `oc get pvc` (`terminal:execute`) → examiner checks: both succeed. Route/PVC constructs → upstream.

### 03-config-and-when-to-use-which.md
**Purpose:** Config objects, plus the judgement call — console vs CLI.
**Content outline:**
- **ConfigMaps/Secrets** — where the config from A03 lives; note Secrets are shown masked in the UI.
- `oc` parity: `oc get configmap,secret` (`terminal:execute`) → examiner check: succeeds.
- **When the console is faster** (visual topology, quick log peek, one-off inspection, onboarding) vs **when the CLI wins** (scripting, repeatability, bulk ops, air-gapped speed). One knowledge check on picking the right tool for a scenario.

### 99-workshop-summary.md
**Purpose:** Recap and close out Core.
**Content outline:**
- Recap: perspectives, Workloads, Networking, Storage, Config — each with its `oc` twin; when to reach for which.
- **Check Your Understanding** (3 Q): which perspective for topology; the `oc` command equivalent to the console's Routes view; one case where the CLI beats the console.
- Close Core: "you've deployed, configured, exposed, persisted, learned the terms, and now know both consoles — pick a track next."

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd`, no `-n` — all `oc` parity commands target the session namespace via the default context. Terminal is used only to mirror what the console shows.

## 8. Design Notes

- Covers idea **2 (console parity)**. Content is the OpenShift-console tour **split out of old A01** (old A01 grew a `03-console-tour.md`; this lab is its new home, now anchored to the app the learner actually built in A02–A05).
- **Config note / console-embedding constraint (confirmed):** the real OpenShift console can't be iframed (`frame-ancestors DENY`) and there's no SSO-user propagation into the session; the session "Console" tab is the **k8s Dashboard usable as the session SA**. Where the session tab can't show a real-console view, deliver that part **screenshot-driven** (annotated). See auto-memory *educates-openshift-console-limitation* and `HANDOVER-console-openshift.md`. Track the screenshot production as a task.
- **Examiner strategy:** console internals aren't examiner-checkable, so every page verifies via the **paired `oc` command** instead — this doubles as the console↔CLI parity teaching point.
- Placed last in the A06–A08 orientation tail; it is the final Core lab before learners branch into a track. Reinforces the `oc`-first habit while showing the UI exists.
