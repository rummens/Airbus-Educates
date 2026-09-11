# Workshop Plan: lab-b01-docker-to-k8s

## 1. Workshop Metadata

- **Name:** `lab-b01-docker-to-k8s`
- **Title:** From Docker to Kubernetes
- **Description:** Migrate a docker-compose file for `hello-dcs` onto DCS object by object — container to Deployment, ports to Service, environment to ConfigMap — then face the four lines the platform rejects outright.
- **Duration:** 25m (tune to the observed median after the first live runs)
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `10` — the on-ramp lab
- **Prerequisites (curricular only):** Core — *Deploy Your First App*, *Configure & Troubleshoot Your App*
- **product_name:** Digital Container Service (DCS)
- **Status:** Re-authored 2026-09-11 for the Build & Run track, from the superseded dev-track lab.

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled — the learner fills in a placeholder and reads three manifests
- Console (Kubernetes Dashboard): **not** enabled — nothing here needs it, and the GUI story for builds is its own console lab later in the track
- Slides: `enabled: true` — one slide per page, deck copied verbatim from the skill
- Examiner: `enabled: true`
- Budget: `medium` (one 1-replica Deployment with modest requests)
- Workshop image: `dcs-workshop-base`
- Sample app: `{{< param dcs_registry >}}/samples/hello-dcs:1.0`, applied via `envsubst`
- **vcluster decision:** `false` — a plain session namespace. Nothing cluster-scoped is created, and the lesson is about workload objects, not cluster topology.
- **Self-contained:** the lab applies its own Deployment, Service and ConfigMap. No `session.objects` pre-deploy, and no state from any other lab (house rule: no lab-to-lab dependencies).

## 3. Learning Objectives

After completing this workshop, the learner will be able to:
- Map the Docker/compose model onto Kubernetes objects — container → Pod/Deployment, `ports:` → Service, `environment:` → ConfigMap, `volumes:` → Volume.
- Explain the shift from imperative (`docker run`) to declarative (desired state the platform reconciles).
- Translate a compose service into a working Deployment + Service + ConfigMap and prove it runs.
- Name the compose lines DCS rejects — an external `:latest` image, `user: root`, `privileged: true`, a host bind mount — and the control that rejects each.

## 4. Connection to the rest of the course

**Already known** (Core): what a Deployment, Pod, Service and ConfigMap *are*; rollouts; `oc` basics. This lab does not re-teach them — it teaches the **mapping** and the **DCS constraints**.

**Deliberately not here:** building an image from source (that is b02), exposing the app outside the cluster (Core taught the Route; the service-type depth is b06), probes and resources (b04).

## 5. Exercise Files

- `docker-compose.yml` — the source of truth being migrated, including the four lines that will not translate.
- `deployment.yaml` — the target Deployment with `REPLACE_WITH_HARBOR_IMAGE` for the learner to fill in.
- `service.yaml` — the migration of `ports:`.
- `configmap.yaml` — the migration of `environment:`.
- `exercises/README.md` — what each file is for.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — framing, first-time note, objectives, prerequisites, environment, time/difficulty.
- **`01-the-mental-model/`** — imperative vs declarative, the four-row mapping table, **SVG** (`mental-model.svg`). Read-only page; the compose file is opened in the editor and the check asserts it is there to read.
- **`02-container-to-deployment.md`** — fill in the Harbor image, apply with `envsubst`, see 1/1 ready. Teaches the `envsubst` house pattern.
- **`03-ports-to-service.md`** — apply the Service, reach it over cluster DNS, `HTTP 200`.
- **`04-env-to-configmap.md`** — show the greeting *before*, apply the ConfigMap, wire it with `oc set env --from`, watch the rollout serve the migrated value.
- **`05-what-doesnt-translate/`** — the four rejected lines, one control each, **SVG** (`rejected-lines.svg`). Ends with the graded questions on the constraints.
- **`98-your-feedback.md`** — the standard feedback page (tab pre-declared in `workshop.yaml`).
- **`99-workshop-summary.md`** — recap, 4-question Check Your Understanding, forward pointer to *Build Your Image on DCS*.

## 7. Examiner Coverage (one per command)

| Check | Asserts |
|---|---|
| `verify-compose-readable` | the compose source is present in the session (the page's read-only step) |
| `verify-deployment-ready` | the migrated Deployment has 1 ready replica |
| `verify-deployment-image` | the image is the Harbor reference, not the placeholder |
| `verify-service` | the Service exists and has endpoints |
| `verify-service-dns` | the Service answers HTTP 200 over cluster DNS |
| `verify-greeting-default` | before the ConfigMap, `GREETING` is unset in the container |
| `verify-configmap` | the ConfigMap exists |
| `verify-greeting-configured` | the Deployment references the ConfigMap **and** the app serves the migrated greeting |

## 8. Terminal Working Directory

- **Starting directory:** `~/exercises`. No `cd`.
- **Split terminal:** upper (`execute-1`) for all commands; lower (`execute-2`) for the rollout watch on page 04.

## 9. Design Notes

- The lab is the track's **on-ramp**: Docker-native developers get a bridge before the build labs.
- `envsubst < f.yaml | oc apply -f -` is introduced here and reused for the rest of the track — it is the house pattern for any manifest carrying `${DCS_REGISTRY}`.
- Page 05 is the DCS payload: the mapping is the easy half, the constraints are the half that changes how people build.
