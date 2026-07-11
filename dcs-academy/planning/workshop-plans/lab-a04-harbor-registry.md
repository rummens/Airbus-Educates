# Workshop Plan: lab-a04-harbor-registry

## 1. Workshop Metadata

- **Name:** `lab-a04-harbor-registry`
- **Title:** Working with Harbor
- **Description:** Use the DCS Harbor registry — pull images from catalogs, browse the Harbor UI, and see how vulnerability scanning gates images. (Pull-only; pushing is out of scope in Foundations.)
- **Duration:** 45m
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A02 (Kubernetes Essentials on DCS)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Registry auth: **pull** uses a Harbor **robot account** (DCS's automation credential model), provided to the session via `REGISTRY_*` env or a mounted secret, scoped **read-only**. (Confirmed from customer docs — robot accounts are the DCS pattern.)
- Examiner: `enabled: true`
- Workshop image: **`dcs-workshop-base`** — no build tooling needed. Image inspection/pull is done with **`skopeo` only**. **No `docker`/`podman` inside the workshop container** (avoids double-virtualization); `skopeo` daemonless is added to the base image (see Design Notes / air-gapped-images-reference). Drop `podman`/`buildah` from the flow entirely.
- Harbor UI: attempt to embed the Harbor registry UI as a dashboard tab / ingress so learners browse projects, tags, and scan results visually (feasibility flagged — see Design Notes).
- Params: trio; images via `{{< param dcs_registry >}}`

## 3. Learning Objectives

- Explain why DCS uses a single air-gapped registry (Harbor) and how images arrive via **catalogs** (DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog).
- Pull an image from a catalog (with `skopeo`, using a read-only robot account) and run it on DCS.
- Browse a Harbor **project** in the Harbor UI — tags, digests, scan results.
- Explain how external images are brought in via an **image-mirroring ITSM request**.
- Read a Harbor vulnerability scan result and explain the gate.
- Know that Harbor also stores Helm charts, and that PROD namespaces cannot use the Proxy-Cached Catalog.
- Understand that **pushing** to Harbor needs a dedicated Harbor project and is out of scope for Foundations (conceptual only).

## 4. Connection to Previous Workshop

A02 deployed an image that Harbor already hosts; the learner has seen images referenced but not managed them. This workshop is about the registry itself — catalogs, pulling, browsing, scanning. Reuses `oc` knowledge; introduces `skopeo` (daemonless, no docker/podman).

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/pod-from-catalog.yaml` — a Pod/Deployment referencing a catalog image by digest, to show a catalog pull landing on the cluster.

*(No `Containerfile`/build context — pushing and building are out of scope. Everything is pull/inspect with `skopeo` + the Harbor UI.)*

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **Harbor registry** blurb + link `{{< param dcs_docs_base_url >}}/concepts/registry`.
- **`01-registry-and-catalogs.md`** — concept. Air-gapped → single trusted source. **Catalogs**: DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog (and its PROD restriction). Projects, robot accounts (pull), scan gates, Helm charts. Inline blurbs + DCS docs; [OCI images](https://kubernetes.io/docs/concepts/containers/images/) upstream, [Harbor](https://goharbor.io/docs/) upstream.
- **`02-inspect-and-pull.md`**
  - `skopeo inspect docker://{{< param dcs_registry >}}/samples/hello-dcs:1.0` (read-only robot account) → check: manifest/digest returned.
  - `oc apply -f pod-from-catalog.yaml` (references the catalog image) → polling check: pod running from the catalog pull.
  - Explain why `skopeo` (daemonless, no docker/podman inside the container) and why pull uses a read-only robot account.
- **`03-browse-harbor-ui.md`**
  - `dashboard:open-dashboard` **Harbor** tab → learner browses the project, sees tags/digests and the scan result for `hello-dcs`. (If UI embedding proves infeasible, fall back to `skopeo`/`oc` output + annotated screenshots — see Design Notes.)
  - Concept: **pushing** needs a dedicated Harbor project (GitOps-managed repos + robot account with push rights) — describe the model; explicitly out of scope here (no per-session push project). DCS docs link.
- **`04-mirroring-and-scanning.md`**
  - Concept: bringing an external image in = an **image-mirroring ITSM request** (External→DCS Harbor / DCS Harbor→DCS Harbor). Model the outcome (image already mirrored); link the ITSM process. No live external pull (air-gapped).
  - Inspect the scan result for a catalog image (Harbor UI, or `skopeo`/Harbor API query) → check: scan result retrieved.
  - Show a deliberately vulnerable image being flagged/blocked by the gate → diagnose-style check + hint. DCS-specific gate → docs.
- **`99-workshop-summary.md`** — recap catalogs/pull/browse/scan (and why push is ticketed). **Check Your Understanding** (3 Q): why a single registry; what a scan gate does; why push needs a dedicated project. Answers link DCS docs.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. All commands are `skopeo`/`oc` against remote refs — no build context, no `cd` needed.
- Dashboard tab visibility: after the Harbor tab is shown, any later `terminal:execute` switches back to Terminal — guide the learner back to the Harbor tab when needed.

## 8. Design Notes

- **No double-virtualization:** no `docker`/`podman` inside the workshop container. All image work uses **`skopeo`** (daemonless). Add `skopeo` to `dcs-workshop-base` (image-manifest/base rebuild). This drops the need for `dcs-tools` here — A04 now runs on `dcs-workshop-base`.
- **Pull-only:** pushing needs a dedicated, GitOps-managed Harbor project + push-capable robot account per session, which is too much to auto-provision. Foundations teaches pushing as a *concept* only; the robot account provided to the session is **read-only**.
- **Harbor UI integration (open question → to validate):** embed the Harbor registry UI as a dashboard tab / session ingress so learners browse projects, tags, and scan results. Feasibility depends on Harbor UI auth (SSO/robot) and whether it can be reverse-proxied through the session — spike this in `tasks.md`. Fallback: `skopeo inspect` / Harbor API output + annotated screenshots.
- Every image reference already Harbor-scoped via `{{< param dcs_registry >}}`; `collect-images.sh` will pick up the sample images to mirror.
- Mirroring/onboarding is an ITSM ticket in reality — the workshop teaches the *model*, not a live mirror (air-gapped, and mirroring is async/ticketed).
- Scanning intro here is deepened in Security track C01 — keep Foundations at "read the result, understand the gate," not remediation.
- Helm-chart storage in Harbor is mentioned here; hands-on Helm belongs in the Developer track.