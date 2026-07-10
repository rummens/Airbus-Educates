# Workshop Plan: lab-a02-kubernetes-essentials

## 1. Workshop Metadata

- **Name:** `lab-a02-kubernetes-essentials`
- **Title:** Kubernetes Essentials on DCS
- **Description:** Deploy your first workload on DCS with `oc` — Pods, Deployments, and Services — and learn to inspect and scale it.
- **Duration:** 45m
- **Difficulty:** beginner
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

- **`00-workshop-overview.md`** — intro page (objectives, prerequisite A01, environment, 45m/beginner). Align framing with the DCS docs' "Kubernetes Fundamentals" 4-layer model (Infrastructure → Workloads → Networking → Config & Storage) so learners map this workshop onto the portal's mental model.
- **`01-pods-and-deployments.md`**
  - `editor:open-file` deployment.yaml; explain [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) (upstream links).
  - `terminal:execute` `oc apply -f deployment.yaml` → **experience note** (rollout takes a moment) + polling examiner check `readyReplicas >= 1`.
  - `oc get pods` → check: a `hello-dcs-*` pod is Running.
  - `oc describe deployment/hello-dcs` → check: deployment exists (assert selector/replicas).
- **`02-services.md`**
  - `editor:open-file` service.yaml; explain [Service](https://kubernetes.io/docs/concepts/services-networking/service/).
  - `oc apply -f service.yaml` → check: service `hello-dcs` exists with an endpoint.
  - `oc rollout status` / curl in-cluster: `curl http://hello-dcs.$SESSION_NAMESPACE.svc:8080` → check: HTTP 200 / expected body.
- **`03-scaling-and-inspection.md`**
  - `oc scale deployment/hello-dcs --replicas=3` → polling check: 3 ready replicas within budget.
  - `oc get pods` → check: 3 running pods.
  - `oc logs deployment/hello-dcs` → check: log output present.
  - `oc get events` → observational; check asserts no crash-loop events for the app.
- **`99-workshop-summary.md`** — recap Pod/Deployment/Service. **Challenge** (unguided): scale to 2 replicas and confirm within quota (examiner-validated) + hint + reveal-solution. **Check Your Understanding** (3 Q): what a Deployment manages; how to reach a Service in-cluster; what `oc scale` changes.

## 7. Terminal Working Directory Tracking

- Single terminal in `~/exercises`. Manifests referenced by relative name (`deployment.yaml`). No `cd`.

## 8. Design Notes

- First real hands-on; keep the sample app trivial (a hello HTTP server) so focus stays on Kubernetes objects, not app logic.
- Explicit `resources` on the Deployment models good practice and avoids quota exhaustion when scaling (see kubernetes-access-reference budget guidance).
- The `hello-dcs` sample image is a shared academy asset — reuse it in A03/A06 to avoid mirroring more images.
- Console tab used lightly to reinforce the CLI actions visually; guide back to terminal after each `terminal:execute`.
- Sets up A03 (same workload deployed across namespace types) and A06 (exposing it externally).
