# Workshop Plan: lab-a01-what-is-dcs

## 1. Workshop Metadata

- **Name:** `lab-a01-what-is-dcs`
- **Title:** What is DCS?
- **Description:** Get oriented on the Digital Container Service — what it is, who it's for, how containers and images fit, why Kubernetes beats plain Docker for running apps, and how to move around the workshop session so you're ready to deploy in A02.
- **Duration:** 20m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** None (first workshop in the academy)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (learners view a diagram/manifest; no editing)
- OpenShift access: enabled (session namespace pre-provisioned); `security.token.enabled: true`
- Web console: **not** enabled — the guided console tour moved out to A08. Keep A01 light.
- Examiner: `enabled: true`
- Image registry / docker / vcluster / git: **not** needed
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **vcluster decision:** `false` — no cluster-scoped work; orientation only in the plain session namespace.

## 3. Learning Objectives

By the end the learner can:
- Explain what DCS is (on-prem, air-gapped, multi-national EU, OpenShift-based) and who it's for (tenant-facing consumers, not operators).
- Describe the DCS **cluster model** — Sandbox vs PROD — and that the only difference is feature-rollout timing (Sandbox one month ahead) and maintenance-notice/SLA.
- Describe containers and images at a high level.
- State **why Kubernetes beats plain Docker** for running apps: scheduling, self-healing, scaling, declarative desired-state.
- Navigate the session (terminal, editor, `oc`) and run first `oc` commands — ready to deploy in A02.

## 4. Connection to Previous Workshop

None — this is the entry point. Assumes no container or Kubernetes knowledge. (See Design Notes for what deliberately moved *out* of the old A01.)

## 5. Exercise Files to Create

- `exercises/README.md` — "Exercise files for the What is DCS? workshop."
- `workshop/content/dcs-architecture.png` (or an inline **SVG diagram**) — the DCS big-picture: tenant → namespace on a shared, air-gapped OpenShift platform. Air-gapped, so a local page-bundle asset, never an external image. Placeholder to be produced.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — mandatory intro page with the first-time note. `{{< param product_name >}}` framing; What You'll Learn; Prerequisites (none — links to [containers](https://kubernetes.io/docs/concepts/containers/) and the [`oc` CLI](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)); Your Environment (terminal/editor/`oc`, air-gapped). 15m / beginner. No actions.
- **`01-what-is-dcs.md`** — concept, folded tight. The DCS **mission**: Namespace-as-a-Service on a shared, air-gapped, EU multi-national OpenShift platform; who it's for (tenant teams consuming DCS, not running it); benefits — air-gapped/sovereign, managed, self-service. Embed the architecture diagram/SVG. DCS-specific blurb + `{{< param dcs_docs_base_url >}}/services/overview` (placeholder); no commands.
- **`02-dcs-clusters.md`** — **new.** DCS runs as more than one **cluster**; a tenant meets two kinds: **Sandbox** and **PROD**. They are **essentially identical** — same platform, same capabilities — with one axis of difference: **feature-rollout timing + maintenance/SLA**.
  - Monthly feature flow: **DEV/QA → Sandbox → PROD**. A new platform feature lands on **Sandbox in month 1** and **PROD in month 2** (one month behind).
  - **Sandbox** — try new platform features first; maintenance windows announced **shorter-term** → slightly lower SLA.
  - **PROD** — run production workloads; features arrive proven a month later; longer maintenance notice / higher SLA.
  - That rollout-timing + maintenance-notice difference is the **only** difference — Sandbox is not smaller or weaker.
  - **Clarify (avoid confusion):** a **cluster** (Sandbox/PROD) is not the same as a **DEV/PROD namespace type** (covered in A06 / Developer B06). Cluster = *where* the platform runs; namespace type = *how a namespace is governed*.
  - DCS-specific blurb + `{{< param dcs_docs_base_url >}}/concepts/clusters` (placeholder). No commands.
- **`03-containers-and-images.md`** — containers vs VMs (the "modern apartment vs private house" analogy — appropriate here at level 1); image = the built artifact, container = a running instance; where DCS images live (Harbor, `{{< param dcs_registry >}}`, pull-only — one-line forward pointer, not a deep dive). Upstream links for containers/images. No commands.
- **`04-why-kubernetes-not-just-docker.md`** — **new.** Docker runs a container on one box; that's fine on your laptop, not for a shared platform. What Kubernetes/OpenShift adds, folded as four plain-language wins (VM-world analogy per point, level-appropriate):
  - **Scheduling** — you say "run this," the platform picks where; no hand-placing on a host.
  - **Self-healing** — a crashed container is restarted / rescheduled automatically.
  - **Scaling** — ask for N copies, up or down, without redeploying by hand.
  - **Declarative desired-state** — you describe what you want; the platform continuously reconciles to it (contrast with imperative `docker run`).
  - This is the "why" behind everything in A02–A05. Upstream K8s intro link. No commands (kept conceptual; hands-on lands in A02).
- **`05-your-session.md`** — first hands-on. Guided `terminal:execute`, each with an examiner check:
  - `oc whoami` → check: identity non-empty.
  - `oc version` → check: client + server reachable.
  - `oc project -q` → check: a project is set (assert it equals `$SESSION_NAMESPACE`).
  - `oc status` → check: succeeds against the project.
  - One line on the editor + split terminal (`execute-1`/`execute-2`) so the learner knows the layout before A02.
- **`99-workshop-summary.md`** — recap; bridge to A02 ("now let's get your own app running"). **Check Your Understanding** (4 Q): what makes DCS air-gapped; the one real difference between the Sandbox and PROD clusters; container vs image; one thing Kubernetes gives you that plain Docker doesn't.

## 7. Terminal Working Directory Tracking

- Single terminal, starts in `~/exercises`. No `cd`. All commands namespace-scoped to the session namespace (default context), no `-n` needed.

## 8. Design Notes

- **Trimmed from old A01:** the entire OpenShift web console tour is **removed** — it becomes its own workshop, **A08 (The OpenShift Console)**. This drops A01 from ~30m back to a deliberately light ~15m first-contact lab. Console app is therefore not enabled here.
- **Added:** the "why Kubernetes over plain Docker" page — the conceptual justification for the whole A02–A05 happy path. Kept conceptual (no cluster work) so A01 stays short; the hands-on payoff is A02.
- Establishes the academy-wide pattern: `oc`-only, product-framed, hybrid doc links, every command examiner-verified.
- Architecture diagram/SVG is a reusable asset — candidate to share across Core pages.
- Sets up **A02** (deploy the quick-win app) directly; A06 later gives the vocabulary for the namespace the learner just inspected.
