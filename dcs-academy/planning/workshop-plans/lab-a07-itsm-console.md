# Workshop Plan: lab-a07-itsm-console

## 1. Workshop Metadata

- **Name:** `lab-a07-itsm-console`
- **Title:** The ITSM Console — Self-Service on DCS
- **Description:** Learn where DCS self-service ends and requests begin — which actions you do yourself with `oc` and which need an ITSM ticket — then tour the ITSM console and walk one request end to end.
- **Duration:** 20m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A01 (What is DCS?)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split` (used lightly — mostly for the sorting exercise's checks)
- Editor: enabled (view the request-mapping exercise file)
- OpenShift access: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **Screenshot assets:** page-bundle images of the ITSM console (request form, approval, provisioned result) — air-gapped, embedded locally via `{{< baseurl >}}`. Placeholders to be produced.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain that DCS self-service runs through **ITSM requests**, and where to find the ITSM console.
- Identify which actions require a ticket — **quota increases, image mirroring, new repos/catalogs, S3 buckets, security exceptions** — versus which are self-service via `oc` (deploy, scale, configmaps/secrets, expose within granted rights).
- Describe the request → approval → provisioning loop from a walked-through example (a quota increase).

## 4. Connection to Previous Workshop

**What the learner already knows** (from A01, and the A02–A05 happy path):
- What DCS is and how to work in the session with `oc`.
- Has hit the *edges* of self-service already — A04 noted Routes need a PROD namespace, A05 noted S3 comes via a ticket. This lab names the mechanism behind those asides.

**What is new in this workshop:**
- The ITSM request model as a first-class concept, and the console where it happens.

**What should NOT be re-taught:**
- No `oc` deploy/expose/storage mechanics — those were the earlier labs. This lab is about *what you can't just do yourself*.

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the ITSM Console workshop."

### exercises/self-service-vs-ticket.md
**Purpose:** Backs the sorting knowledge check on page 02 — a short list of tasks (scale a deployment, increase a quota, mirror an image, create a configmap, request an S3 bucket, add a new catalog, expose a Route) for the learner to categorise.
**Initial contents:** The task list with two empty columns ("self-service via `oc`" / "raise an ITSM ticket"), to be filled in during the exercise.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame self-service vs requests.
**Content outline:**
- `{{< param product_name >}}` framing; "you can't just click everything — some things are requests." What You'll Learn; time 20m / beginner.
- DCS-specific blurb + link `{{< param dcs_docs_base_url >}}/getting-started/requests`. No actions.

### 01-self-service-vs-requests.md
**Purpose:** Draw the line between `oc` self-service and ticketed actions.
**Content outline:**
- Two columns of examples: self-service (deploy, scale, env/config, expose within granted rights) vs ITSM request (quota increase, image mirroring, new repos/catalogs, S3, security exceptions). Tie each ticketed item back to where the learner met it (A04 PROD namespace, A05 S3).
- DCS-specific → `{{< param dcs_docs_base_url >}}/getting-started/requests` + blurb. No terminal actions on this page (concept).

### 02-map-the-tasks.md
**Purpose:** Active recall — sort tasks into self-service vs ticket.
**Content outline:**
- Open `exercises/self-service-vs-ticket.md` (`editor:open-file`); learner categorises the task list.
- **Knowledge check** (the examiner surrogate for a screenshot lab): a multiple-choice / matching check — "which of these needs a ticket?" → examiner validates the answer. This is the graded checkpoint of the lab.

### 03-itsm-console-tour.md
**Purpose:** Guided, screenshot-driven tour of the ITSM console.
**Content outline:**
- Annotated screenshots (console likely not reachable in-session — see Config note): where the console lives, the request catalog, how to open a request.
- Walk **one representative request end to end** — a **quota increase**: fill the form → submit → approval step → provisioning → the change appears on your namespace. Show each stage as a captioned screenshot.
- Emphasise the loop: request → approval → provisioning. DCS-specific → `{{< param dcs_docs_base_url >}}/getting-started/requests`.
- *(If the embeddability spike succeeds, this page becomes a live dashboard tab instead of screenshots — see Config note.)*

### 99-workshop-summary.md
**Purpose:** Recap and bridge into the rest of Core / the tracks.
**Content outline:**
- Recap: self-service vs ticket line; the ITSM console; the request→approval→provisioning loop.
- **Check Your Understanding** (3 Q): name two ticketed actions; is scaling a deployment a ticket?; what are the three stages of a request.
- Bridge: A08 tours the *other* console (OpenShift web console); the Developer/Security tracks lean on ITSM for mirroring, catalogs, and exceptions.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- Terminal is used minimally (the mapping exercise's checks); no `cd`, no cluster-mutating commands. This is a tour + knowledge-check lab, not a hands-on `oc` lab.

## 8. Design Notes

- Covers idea **5 (self-service flow)**. New content — consolidates the ITSM-request blurbs previously scattered across old A04/A05/A07 into one place.
- **Config note / open question:** the ITSM console is almost certainly **not reachable inside an air-gapped session**. Plan it as an annotated, **screenshot-driven guided tour**. Spike whether the ITSM console can be embedded as a session dashboard tab; if yes, upgrade page 03 to a live tab. Track as a task.
- Examiner strategy adapts to a screenshot lab: the graded check is the **self-service-vs-ticket knowledge check** (page 02), not a command examiner — every lab still has its verified checkpoint.
- Placed in the A06–A08 orientation tail: "now you know the landscape / next steps," after the hands-on happy path.
