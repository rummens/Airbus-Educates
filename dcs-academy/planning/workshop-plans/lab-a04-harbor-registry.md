# Workshop Plan: lab-a04-harbor-registry

## 1. Workshop Metadata

- **Name:** `lab-a04-harbor-registry`
- **Title:** Working with Harbor
- **Description:** Use the DCS Harbor registry — pull and push images, understand projects, and see how vulnerability scanning gates images.
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
- Registry auth: push/pull uses a Harbor **robot account** (DCS's automation credential model), provided to the session via `REGISTRY_*` env or a mounted secret. (Confirmed from customer docs — robot accounts are the DCS pattern.)
- Examiner: `enabled: true`
- Workshop image: **`dcs-tools`** (needs `podman`/`buildah`, `skopeo`)
- Params: trio; images via `{{< param dcs_registry >}}`

## 3. Learning Objectives

- Explain why DCS uses a single air-gapped registry (Harbor) and how images arrive via **catalogs** (DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog).
- Pull an image from a catalog and run it on DCS.
- Push an image to a Harbor project using a **robot account**.
- Explain how external images are brought in via an **image-mirroring ITSM request**.
- Read a Harbor vulnerability scan result and explain the gate.
- Know that Harbor also stores Helm charts, and that PROD namespaces cannot use the Proxy-Cached Catalog.

## 4. Connection to Previous Workshop

A02 deployed an image that Harbor already hosts; the learner has seen images referenced but not managed them. This workshop is about the registry itself — pulling, pushing, scanning. Reuses `oc` knowledge; introduces `podman`/`skopeo`.

## 5. Exercise Files to Create

- `exercises/Containerfile` — a tiny app image built on a Harbor-mirrored base (`{{< param dcs_registry >}}/base/ubi-micro:latest` or similar OpenShift-friendly base).
- `exercises/app/` — minimal app content to bake in.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **Harbor registry** blurb + link `{{< param dcs_docs_base_url >}}/concepts/registry`.
- **`01-registry-and-catalogs.md`** — concept. Air-gapped → single trusted source. **Catalogs**: DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog (and its PROD restriction). Projects, robot accounts, scan gates, Helm charts. Inline blurbs + DCS docs; [OCI images](https://kubernetes.io/docs/concepts/containers/images/) upstream, [Harbor](https://goharbor.io/docs/) upstream.
- **`02-pull-and-run.md`**
  - `podman pull {{< param dcs_registry >}}/samples/hello-dcs:1.0` (from a DCS catalog) → **experience note** (pull) + check: image present locally.
  - `oc run` / apply the pulled image → check: pod running.
- **`03-build-and-push.md`**
  - `editor:open-file` Containerfile.
  - `podman build -t {{< param dcs_registry >}}/<project>/myapp:1.0 .` → experience note + check: local image built.
  - Log in with the **robot account** (`podman login` using `REGISTRY_*`) → check: login succeeds.
  - `podman push {{< param dcs_registry >}}/<project>/myapp:1.0` → check: manifest exists in Harbor (via `skopeo inspect`).
- **`04-mirroring-and-scanning.md`**
  - Concept: bringing an external image in = an **image-mirroring ITSM request** (External→DCS Harbor / DCS Harbor→DCS Harbor). Model the outcome (image already mirrored); link the ITSM process. No live external pull (air-gapped).
  - Trigger/inspect the scan for the pushed image (`trivy` from `dcs-tools`, or query Harbor) → check: scan result retrieved.
  - Show a deliberately vulnerable image being flagged/blocked by the gate → diagnose-style check + hint. DCS-specific gate → docs.
- **`99-workshop-summary.md`** — recap pull/push/scan. **Check Your Understanding** (3 Q): why a single registry; what a scan gate does; where images live. Answers link DCS docs.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. `podman build` uses `.` (the exercises dir) — no `cd`. Track that build context is `~/exercises`.

## 8. Design Notes

- **Push auth resolved from customer docs:** DCS uses Harbor **robot accounts**. Remaining implementation detail: the exact per-session robot-account provisioning + target project (a small P2, not a design unknown).
- Uses `dcs-tools` (build tooling) — the only Foundations workshop that needs it.
- Every image reference already Harbor-scoped via `{{< param dcs_registry >}}`; `collect-images.sh` will pick up the base and sample images to mirror.
- Mirroring/onboarding is an ITSM ticket in reality — the workshop teaches the *model*, not a live mirror (air-gapped, and mirroring is async/ticketed).
- Scanning intro here is deepened in Security track C01 — keep Foundations at "read the result, understand the gate," not remediation.
- Helm-chart storage in Harbor is mentioned here; hands-on Helm belongs in the Developer track.
