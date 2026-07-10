# DCS Academy — Course Brief

## Course Vision

The DCS Academy teaches teams to use the **Digital Container Service (DCS)** — Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. It takes learners from container fundamentals through to deploying, observing, and securing real applications on DCS.

The academy is organised as a shared **Foundations** core that every learner completes, followed by role-specific tracks (Developer, Security & Compliance, Architect / Onboarding) and a cross-track Observability module. This lets a mixed audience share a common baseline understanding of DCS before specialising.

Scope: **comprehensive** — a multi-module curriculum (10+ workshops) using a core/elective model, built incrementally starting with Foundations and the Developer track.

## Target Audience

Tenant-facing (consumers of DCS, not platform operators). Three audiences, each with its own track and skill progression:

- **App developers** (intermediate → advanced) — deploy and run their applications on DCS.
- **Security & compliance** (intermediate → advanced) — image scanning, policy, secrets, supply chain, EU data-residency.
- **Architects / onboarding** (beginner → intermediate) — orientation, service catalog, tenancy and reference architectures.

Foundations assumes no prior container knowledge and brings everyone to a shared baseline; tracks assume Foundations is complete.

## Product / Service

- **Product name** (`product_name`): `Digital Container Service (DCS)`
- **Short form** (`product_short`): `DCS`
- **Image registry** (`dcs_registry`): Harbor project — placeholder `harbor.example.dcs/dcs-academy` until confirmed
- **Docs portal** (`dcs_docs_base_url`): placeholder `https://docs.example.dcs` until confirmed
- **Base images:** `dcs-workshop-base`, `dcs-tools`

## Delivery Platform

Delivered on the Educates training platform, targeting **OpenShift**. Each workshop is a self-contained, interactive, browser-based environment with an embedded terminal, VS Code editor, and step-by-step instructions. Commands target OpenShift via `oc`. The platform is **fully air-gapped** — all images come from Harbor and external sites are unreachable from within a session.

## Course Structure

| Module | Theme | Type |
|---|---|---|
| **A — Foundations** | Kubernetes essentials + DCS essentials (namespace types, Harbor, tenancy, networking) | Core (everyone) |
| **B — Developer** | Deploy, configure, scale, debug apps on DCS | Elective track |
| **C — Security & Compliance** | Scanning, pod security, secrets, supply chain, data-residency | Elective track |
| **D — Architect / Onboarding** | Service catalog, tenancy design, reference architectures | Elective track |
| **E — Observability** | Metrics, logs, alerts for tenant apps | Elective (cross-track) |

## Navigation Model

Core/elective:

- **Core** = Module A (Foundations). Sequential; every learner completes it first. It establishes the shared baseline and the DCS-specific concepts all tracks rely on.
- **Electives** = Modules B, C, D, E. Each branches off Foundations. Within a track, workshops are sequential (they share a per-track sample app). Across tracks they are independent — a learner can take Developer without Security. Observability (E) has an additional prerequisite: a deployed application (from Developer B01, or equivalent).
- Every workshop states its prerequisites explicitly.

## Design Principles

- **Fully guided experience.** All code interaction — viewing, running, modifying — is driven through Educates clickable actions. Learners click, they do not type commands or edit files by hand.
- **Per-track sample app.** Each track carries one evolving sample application, reused across its workshops for continuity.
- **Realistic multi-namespace.** Where the prod/dev namespace model must be tangible, workshops use a virtual cluster so learners see both namespace types.
- **Conceptual material folded in.** Scene-setting is delivered as "observe and diagnose" exercises or as the introduction page, not as standalone text-only workshops.
- **Air-gapped by design.** No external images or in-session internet access is assumed.

## House Standards

Enforced by the `airbus-educates-workshop-authoring` skill (see its references):

- OpenShift/`oc`; Routes / session proxy over raw Ingress.
- Mandatory introduction page on every workshop.
- Hybrid doc links: standard constructs → upstream docs; DCS-specific concepts → `dcs_docs_base_url` with an inline blurb.
- Variablization + the mandatory param trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`).
- Air-gapped images from Harbor; shared `dcs-workshop-base` / `dcs-tools`.
- Examiner step checks + a knowledge check per workshop.

## Scope and Growth Path

v1 target: **Foundations (A) + Developer (B)**, proving the format end to end. Then add Security (C), Architect (D), and Observability (E). Natural later expansion: a CI/CD & GitOps module (Tekton/OpenShift Pipelines, Argo CD), stateful/storage deep-dive, and advanced networking — all deferred from v1.
