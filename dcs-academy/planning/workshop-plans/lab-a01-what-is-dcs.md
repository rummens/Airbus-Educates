# Workshop Plan: lab-a01-what-is-dcs

## 1. Workshop Metadata

- **Name:** `lab-a01-what-is-dcs`
- **Title:** What is DCS?
- **Description:** Get oriented on the Digital Container Service — what it is, how containers and images fit, and how to work in the DCS environment with `oc` and the OpenShift web console.
- **Duration:** 30m (was 20m; +10m for the guided console tour)
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** None (first workshop in the academy)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (learners view a diagram/manifest, no heavy editing)
- OpenShift access: enabled (session namespace/project pre-provisioned); `security.token.enabled: true`
- Web console: enabled (console tour)
- Examiner: `enabled: true`
- Image registry / docker / vcluster / git: **not** needed
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)

## 3. Learning Objectives

By the end the learner can:
- Explain what DCS is (on-prem, multi-national EU, OpenShift-based, air-gapped) and where it fits.
- Describe containers and images at a high level.
- Navigate the session environment (terminal, editor, console) and run first `oc` commands.
- Identify their project and confirm cluster access.

## 4. Connection to Previous Workshop

None — this is the entry point. Assumes no container or Kubernetes knowledge.

## 5. Exercise Files to Create

- `exercises/README.md` — "Exercise files for the DCS Foundations workshop."
- `workshop/content/01-what-is-dcs/dcs-architecture.png` — architecture diagram (page-bundle asset, embedded; air-gapped so local, not external). Placeholder to be produced.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — mandatory intro page: `{{< param product_name >}}` framing; What You'll Learn; Prerequisites (none, links to [containers](https://kubernetes.io/docs/concepts/containers/) and [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)); Your Environment (terminal/editor/console, `oc`, air-gapped); Time 20m / beginner. No actions.
- **`01-what-is-dcs/index.md`** — concept page. Mirror the customer-docs narrative: containers vs VMs (the "private house vs modern apartment" analogy), the Airbus Commercial → Defence & Space OpenShift journey, and the DCS **mission** (Namespace as a Service on a shared, air-gapped, EU multi-national platform). Note **shared vs dedicated managed clusters**. Blurb + DCS docs (`/services/overview`, placeholder); containers & images primer (upstream links). Embed `dcs-architecture.png` via `{{< baseurl >}}`. No commands.
- **`02-your-environment.md`** — first hands-on. Guided `terminal:execute` actions, each with an examiner check:
  - `oc whoami` → check: identity is non-empty.
  - `oc version` → check: client+server reachable.
  - `oc project -q` → check: a project is set (assert it equals `$SESSION_NAMESPACE`).
  - `oc status` → check: command succeeds against the project.
- **`03-console-tour.md`** — **guided tour of the OpenShift web console** (task: every learner should know the console before their track). `dashboard:open-dashboard` Console, then walk the key areas with callouts (annotated screenshots + "click here" prose, since console internals can't be examiner-checked directly):
  - **Perspectives:** Developer vs Administrator; when to use each.
  - **Project selector / your namespace** — confirm it matches the session namespace from page 02.
  - **Workloads** (Deployments/Pods) — where the things you'll create in A02 show up; Topology view.
  - **Builds/Networking (Routes)/Storage (PVCs)** — signpost where A04/A06/A07 land, without going deep.
  - **Events & Pod logs/terminal** — the console's own debugging surface (previews B04).
  - **Search + the "Getting started"/help** entry points.
  - Anchor each area to the `oc` command that does the same thing (console ↔ CLI parity), reinforcing the `oc`-first habit.
  - Verification: return to terminal, `oc get all` → check succeeds (proves the same objects the console shows are reachable via `oc`). Guide the learner back to the Console tab as needed (dashboard tab visibility).
- **`99-workshop-summary.md`** — recap; what's next (A02). **Check Your Understanding** (3 Q): what makes DCS air-gapped; container vs image; where in the console you'd find your running Pods (or the `oc` equivalent).

## 7. Terminal Working Directory Tracking

- Single terminal, starts in `~/exercises`. No `cd`. All commands namespace-scoped to the session project (default context), no `-n` needed.

## 8. Design Notes

- Deliberately light and confidence-building — first contact for all audiences (dev, security, architect).
- Establishes the `oc`-only, product-framed, docs-linked, every-command-verified pattern the whole academy follows.
- Architecture diagram is a reusable asset; consider sharing it across Foundations pages.
- Sets up A02 (hands-on Kubernetes) and A03–A07 (DCS spine).
- **Console tour (task):** the built A01 currently has only a one-line console note; `03-console-tour.md` upgrades it to the academy's single guided console tour so it's covered **once** in Foundations. This also justifies the already-enabled `console` app (see A01/A02 review: console was enabled but unused). Keep it navigational, not deep — later labs open the console for their specific area. Console internals aren't examiner-checkable, so verify via the paired `oc` command instead.
