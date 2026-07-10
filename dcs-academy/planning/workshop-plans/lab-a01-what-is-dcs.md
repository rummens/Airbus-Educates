# Workshop Plan: lab-a01-what-is-dcs

## 1. Workshop Metadata

- **Name:** `lab-a01-what-is-dcs`
- **Title:** What is DCS?
- **Description:** Get oriented on the Digital Container Service — what it is, how containers and images fit, and how to work in the DCS environment with `oc`.
- **Duration:** 20m
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
  - Console tour: `dashboard:open-dashboard` Console; brief note pointing at overview. (Observational — check asserts project is accessible.)
- **`99-workshop-summary.md`** — recap; what's next (A02). **Check Your Understanding** (3 Q): what makes DCS air-gapped; container vs image; which command shows your project.

## 7. Terminal Working Directory Tracking

- Single terminal, starts in `~/exercises`. No `cd`. All commands namespace-scoped to the session project (default context), no `-n` needed.

## 8. Design Notes

- Deliberately light and confidence-building — first contact for all audiences (dev, security, architect).
- Establishes the `oc`-only, product-framed, docs-linked, every-command-verified pattern the whole academy follows.
- Architecture diagram is a reusable asset; consider sharing it across Foundations pages.
- Sets up A02 (hands-on Kubernetes) and A03–A06 (DCS spine).
