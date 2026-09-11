# Build & Run + Operate & Observe — track plan

**Created:** 2026-09-11. Working plan for the two tracks that replace the old Developer track.
Baseline = the **finished Core + Console tracks** — do not edit them; copy their style,
structure and features. Standards: `airbus-educates-workshop-authoring-skill/references/`;
rubric: `airbus-educates-course-review-skill`.

## Decisions locked (2026-09-11)

- The **old Developer (B01–B08) and Security (C01–C05) built labs are obsolete.** They were
  authored to the pre-baseline standard and never published. `git mv` both track folders to
  `workshops-monorepo/_superseded/` — outside `tracks/`, so the helm globs
  (`tracks/*/track.yaml`, `tracks/*/*/resources/workshop.yaml`) stop seeing them and no
  Workshop/Track CR is emitted. They stay browsable as a content quarry.
- The Developer track **splits in two**:
  - **Build & Run** — track id `build`, order `20`, labs `lab-b01…` (the `b` code is free again).
  - **Operate & Observe** — track id `operate`, order `25`, labs `lab-o01…`.
  - Security keeps order `30` for whenever it is replanned.
- **Operate & Observe owns the platform-mechanism labs** (RBAC/tenancy, DEV vs PROD + promotion,
  operators) on top of metrics and logs. Build & Run is purely "get my app built and running well".
- All four extra topics are in v1: **Jobs/CronJobs, PDB + graceful shutdown, init containers /
  sidecars, pod scheduling**.
- **Console labs live in the topic's own track**, not only in the Console track. Every terminal
  lab with a strong GUI story gets an **optional paired console lab** placed right after it:
  builds, health & resources, autoscaling, metrics, logs. The pedagogical contract holds — the
  terminal lab *teaches* the concept, the console lab only *applies* it in the GUI.
- **No lab-to-lab dependencies, ever.** A terminal lab and its console lab **deploy as two
  independent labs**: each provisions its own namespace and its own resources, and neither reads
  state the other left behind. "Prerequisite" is curricular only — named in the description so a
  learner knows the reading order — never technical. Same rule between terminal labs: no lab
  assumes an object another lab created.
- **The portal gets a visual "Optional" hint** (see §5) — optional stops being prose-only.

## Domain facts confirmed by the author (2026-09-11)

**Harbor project model** — this supersedes the older "pull-only, don't teach pushing" rule:

- A Harbor project is **optional** for a tenant, and is scoped **per namespace** today. A
  **per-tenant** model is the eventual target — teach per-namespace, name the direction.
- **DEV namespace project: push and pull, no CVE limitation.**
- **PROD namespace project: no push at all; pull only images with CVE severity < 9.**
- If a required image cannot meet the PROD threshold, a **security exception process** exists.
- **How an image reaches a PROD project**, given it takes no push: either **promotion from the
  DEV project via a Harbor mirror**, or pulled from the **green catalog** — the cleared /
  golden-standard images. b03 teaches both paths; the green catalog is the easy road.
- Workshop containers still use **`skopeo` only** (no docker/podman).

**Monitoring** — user-workload monitoring is **enabled**, and tenants **can create
`ServiceMonitor`s**. Whether the Thanos / Loki query APIs are reachable from a session pod is
unconfirmed: **author against them, and back every read with a screenshot fallback** so the lab
still teaches if the API is blocked.

---

## 1. Layout

### Build & Run (`build`, order 20) — 10 labs, ≈ 4h

| Code | Title | Level | Est. | Teaches |
|---|---|---|---|---|
| b01 | Docker to Kubernetes | intermediate | 25m | compose/`docker run` → Deployment/Service/ConfigMap; what does not translate on DCS (SCC/non-root, Harbor, no `latest`) |
| b02 | Build Your Image on DCS | intermediate | 30m | git as a build source; BuildConfig (S2I + Dockerfile strategy); ImageStream; output pushed to Harbor; rebuild triggers |
| b03 | Harbor: Projects, Push & Scan | intermediate | 30m | the tenant's **optional Harbor project**, scoped per namespace today; **DEV pushes anything / PROD takes no push and pulls only CVE < 9**; the **green catalog** of cleared images; promotion DEV → PROD via a **Harbor mirror**; the **security exception** route; catalogs (DCS / allowed-external / proxy-cache); robot accounts; `skopeo` pull/inspect/push; reading a scan report and the gate; mirroring/quota via ITSM |
| b04 | Health & Resources | intermediate | 25m | liveness/readiness/startup probes; requests vs limits; LimitRange defaults; the namespace budget; self-healing |
| b05 | Autoscaling | intermediate | 20m | HPA on CPU (and why it needs requests); interaction with quota and `replicas`; **VPA as observe-only** (operator-provided); when not to autoscale |
| b06 | Services & Cluster Networking | intermediate | 20m | ClusterIP / NodePort / LoadBalancer / ExternalName / **headless**; cluster DNS names; endpoints and selectors; **why DCS hands you a Route instead** (forward-ref to o04) |
| b07 | Stateful Workloads | intermediate | 25m | StatefulSet vs Deployment; stable identity; `volumeClaimTemplates` (a PVC per replica); headless Service pairing; ordered rollout; scale-down leaves the PVCs |
| b08 | Short-Lived & Helper Containers | intermediate | 25m | run-to-completion: **Job** (parallelism, backoffLimit) and **CronJob** (schedule, concurrencyPolicy); **init containers** (ordering, migrations) and **native sidecars** (same API, `restartPolicy: Always`) |
| b09 | Resilience & Scheduling | intermediate | 25m | **PodDisruptionBudget** vs a node drain; **graceful shutdown** (SIGTERM, `terminationGracePeriodSeconds`, preStop); pod **anti-affinity** and **topologySpreadConstraints** for HA of the tenant's own app |
| b10 | Dev Spaces *(optional tail)* | intermediate | 18m | git as an in-cluster IDE; devfile; Harbor-mirrored UDI; how it differs from BuildConfigs and the Educates editor |

**Optional console labs in this track** (each placed directly after its terminal lab):

| Code | Pairs with | Est. | Shows in the GUI |
|---|---|---|---|
| tour-b02-builds | b02 | 10m | the Builds / BuildConfig views, a build's log stream, ImageStreams and their tags, Start build from the UI |
| tour-b04-health | b04 | 10m | probes and resource fields on a Deployment, a Pod's conditions and restart count, the project's quota and LimitRange pages |
| tour-b05-autoscaling | b05 | 8m | adding an HPA from a Deployment's Actions menu, the replica graph reacting, why the field shows a target utilisation |

### Operate & Observe (`operate`, order 25) — 5 labs, ≈ 2h

| Code | Title | Level | Est. | Teaches |
|---|---|---|---|---|
| o01 | Metrics & Monitoring | intermediate | 25m | what the platform scrapes for free vs what you must expose; **ServiceMonitor**; PromQL against the tenant-visible query endpoint; the OpenShift console monitoring views (screenshot-driven — the real console cannot be embedded in a session) |
| o02 | Logs with LokiStack | intermediate | 20m | the aggregation path (collector → LokiStack → gateway); **LogQL** queries; label vs line filters; finding the logs of a Pod that no longer exists; retention (`oc logs` itself is Core) |
| o03 | RBAC & Tenancy | intermediate | 25m | **Tenant → Namespaces** (no "project" layer); Role vs ClusterRole, RoleBinding vs ClusterRoleBinding; `oc auth can-i` before/after a grant; `--as` impersonation; quotas and the ITSM increase |
| o04 | DEV vs PROD Namespaces | intermediate | 20m | the policy posture split — **PROD enforces Kyverno and can create Routes; DEV is looser and cannot**; promotion DEV → PROD (never edit in place); why the split exists |
| o05 | Operators on DCS | advanced | 30m | controller + reconcile; CRD vs CR; OLM/OperatorHub; the **DCS ownership model** (platform owns the operator, tenant owns the instance). Capstone that points at the Operators track (Module F) |

**Optional console labs in this track:**

| Code | Pairs with | Est. | Shows in the GUI |
|---|---|---|---|
| tour-o01-metrics | o01 | 12m | Observe → Metrics (run a PromQL query), Dashboards, Targets showing your own ServiceMonitor being scraped, the Developer perspective's per-workload graphs |
| tour-o02-logs | o02 | 10m | Observe → Logs (the Loki console plugin), a LogQL query in the UI, severity filters, the Logs tab on a single Pod |

Later in this track: **Alerts** (needs o01 first) and any SLO material.

### What is deliberately out

- **NetworkPolicy authoring** — not tenant self-service yet; Core teaches it as observe.
- **Operators deep-dive** (GitLab, Argo CD, CloudNativePG) — Module F.
- **Alerts** — after o01 lands.
- Helm charts, Tekton/Pipelines, blue-green/canary, service mesh, tracing — deferred.
- **Security & Compliance** — the whole track is replanned separately; note that *all image
  scanning now lives in b03*, so the revived Security track keeps only the governance /
  provenance / classification angle.

---

## 2. What "same style and features as Core/Console" means

Non-negotiable per lab, applied from the first commit (this is what the obsolete labs lacked):

1. **Slides** — `workshop/slides/{index.html,slides.md}` + `applications.slides.enabled: true`,
   one slide per content page, each page opens its slide with a `dashboard:reload-dashboard` block.
2. **Feedback tab pre-declared** in `session.dashboards` (always visible; completion still fires
   on form submit) + the `98-your-feedback.md` page.
3. **Skimmable formatting** — bold key terms, ≤3-line one-idea paragraphs, actions/choices as
   lists, `{{< note >}}`/`{{< warning >}}` led by `**💡 Tip:**` / `**⚠️ Watch out:**`.
4. **Examiner conventions** — one check per command; `✅`/`❌` in the *script* messages; the
   `title:` stays plain text (no emoji, no bold) because the action block is the state indicator;
   failures name expected / found / next step.
5. **An SVG diagram** on every concept page with a mechanism worth drawing (Core averages 2/lab).
6. **Knowledge check** on the summary page.
7. **`README.md` prospectus** + `academy.dcs/details` catalog metadata (Console-track shape).
8. **No hardcoded infrastructure** — `${DCS_REGISTRY}` + `envsubst < f.yaml | oc apply -f -`,
   incl. anything in `session.objects`; param trio in `workshop/config.yaml` as a **list**.
9. **Cross-references by lab name** ("the Expose Your App lab"), never `A01`/`b03` codes.
10. **`oc` only**, every image from Harbor.
11. **vcluster vs session namespace decided and justified** per lab.
12. **Durations tuned to observed medians** after the first live runs, not guessed.

For the **console labs**, the standards are the console-tour skill's instead: a hidden
`ConsoleLab` CR plus a paired `workshop.yaml` that pre-deploys the resources it points at and
carries `academy.dcs/console-lab`, `academy.dcs/lab-format`, `academy.dcs/orphaned: "0s"` and
`academy.dcs/expires`; `academy.dcs/details` is the prospectus (there is no README); every
navigation step is followed by a step that shows something on the page it opened; step text
stays **plain text, no emoji**; the CLI equivalent is named, never phrased as an instruction.

**Optional labs carry a real badge** once the portal change in §5 ships: set
`academy.dcs/optional: "true"` on the Workshop CR, keep saying it in the `description` /
`details` too, and order the lab right after the one it complements.

**Each console lab is self-contained.** Its folder holds the `ConsoleLab` CR *and* a
`workshop.yaml` that provisions the namespace and every resource the tour points at — the tour
never depends on a terminal-lab session having run.

---

## 3. Work plan

### Phase 0 — layout + domain truth (no content yet)

1. `git mv` `tracks/dev-track` and `tracks/security-track` → `_superseded/`; drop their
   `test/workshops/smoke-plans/lab-b0*.json` / `lab-c0*.json`; confirm `helm template` no longer
   emits those Workshops/Tracks.
2. Create `tracks/build-track/track.yaml` (`build`, order 20) and
   `tracks/operate-track/track.yaml` (`operate`, order 25), both `availability: disabled`.
3. Rewrite the planning docs to this layout: `course-topics.md`, `course-module-b.md` (→ Build
   & Run), a new module doc for Operate & Observe, `course-brief.md` track list, `tasks.md`.
   Retire the 13 obsolete `workshop-plans/lab-b0*.md` / `lab-c0*.md`.
4. **Confirm the domain facts** that the new content depends on (see §4) — the Harbor project
   model and what monitoring/logging expose to a tenant are the two that block b03 and o01/o02.
5. Write the 15 per-workshop plans with the **course-design skill**, build order first.

### Phase 0b — portal: the Optional badge

Small, self-contained, and it unblocks honest catalog metadata for every optional lab:

1. `images/dcs-academy-portal/portal/k8sclient.py` — add `"optional": _lbl(meta, "optional") == "true"`
   to the course dict (next to `lab_format`).
2. `portal/templates/_macros.html` — a third pill in `meta_pills()` when `c.optional`, plus
   `data-optional` on the tile so the existing filter bar can use it; style it in `static/`.
3. Decide what the tile's **"Lab N of M"** counter does with optional labs — count them, or
   number only the required path (recommended: number the required path, badge the rest).
4. Test in `test/portal/` (90% coverage gate), then rebuild + push
   `ghcr.io/rummens/dcs-academy-portal` and let ArgoCD sync.
5. Core's "What is DCS?" could take the same label as a one-line change — **not doing it** while
   Core is frozen; mention it and let the author decide.

### Phase 1 — author Build & Run, one lab per turn

b01 → b02 → b03 → b04 → b05 → b06 → b07 → b08 → b09 → b10.
Per lab: plan → author (workshop-authoring skill) → **gates** → `FIXES.md` line if learner-visible.

Console labs are authored **with their terminal lab**, not in a later pass — the terminal lab
owns the concepts the tour applies, and the pairing is what keeps the tour from re-teaching them.
They still ship as **separate, independently deployable labs** with their own provisioning.

### Phase 2 — author Operate & Observe

o01 → o02 → o03 → o04 → o05. Same loop. o01/o02 may degrade to screenshot + fixture labs if
the stack is not tenant-reachable (decide at Phase 0, not mid-authoring).

### Phase 3 — publish each track

Tune durations to observed medians · set `academy.dcs/order` · track description + `details` ·
full-track run `./run_track.sh workshops-monorepo/tracks/<track>` · course-review skill over the
whole track · flip `availability: available` · `FIXES.md` entry for the track going live.

### Gates — a lab is done only with all four

1. static: `helm template` clean, YAML parses, param trio present, no `kubectl`
2. `coverage_check.py` (every command has a smoke test) + `link_check.py`
3. live smoke green on CRC: `deploy_workshop.py` → `smoke_test.py` + a written smoke plan
   (env-specific XFAILs documented the way Core did)
4. course-review skill clean

---

## 4. Blockers to resolve in Phase 0

Each unresolved item degrades its lab to concept/fixture-only — decide before authoring, not after.

| # | Needed | Blocks |
|---|---|---|
| 1 | ~~Harbor project model + promotion path~~ **RESOLVED** (see Domain facts): green catalog, or mirror from DEV. Remaining: **who triggers the mirror** (self-service in Harbor vs ITSM) and what the green catalog is called in the docs. | b03 |
| 2 | **Push-capable Harbor project + robot account** reachable from a session | b02 (build output), b03 (push step) |
| 3 | **Air-gapped-reachable git build source** + mirrored S2I builder image | b02 |
| 4 | ~~User-workload monitoring / ServiceMonitor rights~~ **RESOLVED** (both yes). Remaining: is the **query endpoint reachable from a session pod**, and with which token? Author against it + screenshot fallback. | o01 |
| 5 | **LokiStack** reachable from a session (gateway route/service + token + tenant scoping); is the **Loki console plugin** installed (needed for tour-o02-logs)? | o02 |
| 6 | **Kyverno** present on the test cluster | o04 |
| 7 | **CloudNativePG operator** + mirrored operand images | o05 |
| 8 | **VPA operator** present, or teach VPA as observe-only | b05 |
| 9 | **Multi-node** test cluster for anti-affinity / topology spread (CRC is single-node → likely narrate + screenshot) | b09 |
| 10 | **RWX storage class** for per-replica PVCs | b07 |
| 11 | **Dev Spaces** instance + mirrored UDI, else keep b10 a concept lab | b10 |
| 12 | `hello-dcs` needs a **`/metrics` endpoint** if o01 is to scrape a real tenant app (else scrape a platform-provided target) | o01, tour-o01 |
| 13 | Console labs need the **academy console plugin** present on the target cluster and the labs reachable from the portal launcher (already true for the Console track) | all 5 tours |
