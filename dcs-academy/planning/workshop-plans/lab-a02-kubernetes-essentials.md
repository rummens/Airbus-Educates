# Workshop Plan: lab-a02-kubernetes-essentials

## 1. Workshop Metadata

- **Name:** `lab-a02-kubernetes-essentials`
- **Title:** Kubernetes Essentials on DCS
- **Description:** Deploy your first workload on DCS with `oc` — Pods, Deployments, and Services — and learn to inspect and scale it.
- **Duration:** 40m (guided, clickable — most finish faster than the page count suggests)
- **Difficulty:** beginner → intermediate
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A01 (What is DCS?)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view/apply manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (see Deployments/Pods visually)
- Examiner: `enabled: true`
- Budget: `medium` (small deployment + scaling headroom)
- Workshop image: `dcs-workshop-base`
- Sample image: `{{< param dcs_registry >}}/samples/hello-dcs:1.0` (Harbor-mirrored, OpenShift-friendly non-root)

## 3. Learning Objectives

- Create a Deployment and a Service with `oc`.
- Inspect Pods/Deployments with `oc get`/`oc describe`, and read logs/events.
- Reach a Service in-cluster by DNS.
- Scale a Deployment and observe the result.
- Explain the Pod → Deployment → Service relationship.

Mapped to DO180 modules 2–4 (CLI & API, run pods, deploy managed & networked apps).

## 4. Connection to Previous Workshop

A01 covered orientation and first `oc` commands. Learner knows how to find their project and run `oc`. Do **not** re-explain `oc whoami`/projects. Start deploying.

## 5. Exercise Files to Create

- `exercises/deployment.yaml` — Deployment `hello-dcs`, image `{{< param dcs_registry >}}/samples/hello-dcs:1.0`, 1 replica, explicit `resources` requests/limits (respect budget), container port 8080.
- `exercises/service.yaml` — Service `hello-dcs`, port 8080 → targetPort 8080, selector matches Deployment.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

**One concept per page** (content-depth standard). Each page leads with what/why/how, shows expected output, explains flags, and has ≥1 examiner check.

- **`00-workshop-overview.md`** — intro page (objectives, prerequisite A01, environment). Frame with the DCS "Kubernetes Fundamentals" 4-layer model (Infrastructure → Workloads → Networking → Config & Storage).
- **`01-creating-resources.md`** — *how you create resources.* Imperative vs declarative; `oc create deployment --dry-run=client -o yaml`; `--help`/`oc explain`; why production keeps manifests in git. Check: deployment still **absent** after dry-run (proves dry-run creates nothing).
- **`02-the-deployment-resource.md`** — what a Deployment is/why; `editor:open-file` deployment.yaml; `oc apply`; `oc rollout status`; expected output. Experience note + polling check (1 ready replica).
- **`03-deployments-replicasets-pods.md`** — the ownership hierarchy Deployment→ReplicaSet→Pod; `oc get all -l app=hello-dcs`; why you don't edit ReplicaSet/Pod directly; cascade delete. Checks: pods running; deployment exists.
- **`04-labels-and-selectors.md`** — what/why labels; how Deployment & Service select Pods; querying by label. Check: pods carry `app=hello-dcs`.
- **`05-querying-resources.md`** — inspecting: `oc get -o wide/-o yaml/-o name`, `oc describe`, `oc explain`. Check: deployment exists (shared across the observational commands).
- **`06-scaling-and-self-healing.md`** — `oc scale` to 3; **split-terminal** `watch` + delete a pod → auto-recreated; config drift and `oc apply` reset. Checks: 3 replicas; pods running.
- **`07-application-logging.md`** — why logs; `oc logs deployment/…`, `--tail`, `-f`; deployment vs pod logs. Check: logs present.
- **`08-accessing-containers.md`** — `oc exec` / `oc rsh` for debugging; ephemerality (don't fix things live). Check: exec works.
- **`09-services-and-networking.md`** — Pods ephemeral, IPs change → Service; ClusterIP, endpoints, in-cluster DNS FQDN; `oc apply` service; `oc get endpoints`; `curl`. (External exposure stays in A06.) Checks: service has endpoints; responds 200.
- **`99-workshop-summary.md`** — recap. **Challenge** (unguided): scale to 2, confirm within quota (examiner-validated) + hint + reveal. **Check Your Understanding** (4–5 Q across the concepts).

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Manifests referenced by relative name (`deployment.yaml`). No `cd`.

## 8. Design Notes

- First real hands-on; keep the sample app trivial (a hello HTTP server) so focus stays on Kubernetes objects, not app logic.
- Explicit `resources` on the Deployment models good practice and avoids quota exhaustion when scaling (see kubernetes-access-reference budget guidance).
- The `hello-dcs` sample image is a shared academy asset — reuse it in A03/A06 to avoid mirroring more images.
- Console tab used lightly to reinforce the CLI actions visually; guide back to terminal after each `terminal:execute`.
- Sets up A03 (same workload deployed across namespace types) and A06 (exposing it externally).
