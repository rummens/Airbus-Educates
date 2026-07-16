# Workshop Plan: lab-b01-deploy-first-app

## 1. Workshop Metadata

- **Name:** `lab-b01-deploy-first-app`
- **Title:** Deploy Your First App on DCS
- **Description:** Take the sample app from a Harbor image to a running, reachable workload in your DEV namespace on DCS — deploy it, expose it, and confirm it responds.
- **Duration:** 40m
- **Difficulty:** beginner
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** Module A (Foundations) — esp. A02 (Kubernetes Essentials), A03 (Namespace Model), A06 (Networking)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view/edit manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled (see the Deployment/Pod/Service visually)
- Examiner: `enabled: true`
- Budget: `medium`
- **vcluster decision:** `false` — native OpenShift session namespace. A single-app developer task needs no cluster-admin or cluster-scoped objects; the session namespace *is* the learner's DEV namespace.
- Workshop image: `dcs-workshop-base`
- Sample app image: `{{< param dcs_registry >}}/samples/hello-dcs:1.0` (Harbor-mirrored, non-root, port 8080) — **the evolving sample app carried across B01–B05.**

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Deploy the sample app to their DEV namespace with a Deployment + Service.
- Expose the app through the Educates session ingress and reach it in a browser.
- Verify the app is healthy from both the CLI and the web console.
- Explain why self-service exposure in a DEV namespace uses the session proxy, while a real external Route requires a PROD namespace (recap A06).

## 4. Connection to Previous Workshop

**Already known** (from Module A): Deployment/Service basics and `oc apply`/`oc scale` (A02); the DEV vs PROD namespace model and that DEV is self-service without Kyverno enforcement (A03); in-cluster DNS and that an external **Route needs a PROD namespace** (A06).

**New here:** the end-to-end *developer* workflow against one real app you will keep evolving; exposing an app via the **Educates session ingress** (a dashboard tab) rather than a raw Service `curl`.

**Do NOT re-teach:** what a Deployment/Service is (A02); the namespace model (A03); Route mechanics (A06 — reference only).

## 5. Exercise Files to Create

- `exercises/deployment.yaml` — Deployment `hello-dcs`, image `{{< param dcs_registry >}}/samples/hello-dcs:1.0`, 1 replica, `resources` requests/limits within the medium budget, containerPort 8080, `app: hello-dcs` labels.
- `exercises/service.yaml` — Service `hello-dcs`, port 8080 → targetPort 8080, selector `app: hello-dcs`.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; objectives; prerequisites; introduce the sample app (hello-dcs) and that it returns to it every workshop in this track. Open `deployment.yaml` (`editor:open-file`).
- **`01-meet-the-sample-app.md`** — what the app is (a tiny web server on 8080), where its image lives (`{{< param dcs_registry >}}` in Harbor, pull-only), why an air-gapped platform pulls from Harbor not Docker Hub (recap A04). VM-world analogy (light): "the image is your golden VM template in the internal catalog." Check: none (concept).
- **`02-deploy-the-app.md`** — apply the Deployment (`terminal:execute` `oc apply -f deployment.yaml`), `oc rollout status`, expected output. Examiner: 1 ready replica.
- **`03-give-it-a-stable-address.md`** — Pods are ephemeral → a Service; apply `service.yaml`; `oc get endpoints hello-dcs`; in-cluster `curl` from the terminal. Examiner: service has endpoints; responds 200.
- **`04-expose-it-to-your-browser.md`** — expose via the **session ingress** (dashboard tab) so you can see the app in a browser; note that this is the *session* proxy — a real external **Route** would require a PROD namespace and platform sign-off (reference A06, don't re-teach). Examiner: the app's page loads (HTTP 200 through the ingress).
- **`05-iterate.md`** — the developer inner loop: bump replicas to 2 with `oc scale`, re-`curl`, watch the console; roll the image tag and `oc rollout status`. Examiner: 2 replicas ready.
- **`99-workshop-summary.md`** — recap deploy → expose → verify → iterate. Note what's deliberately hard-coded (config baked into the image/manifest) → motivates **B02 Config & Secrets**. Check Your Understanding (4–5 Q). Suggest B02 next.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes; all commands run from `~/exercises`.
- Patterns: `oc apply -f <file>`, `oc get/describe`, `oc rollout status deploy/hello-dcs`, split-terminal `watch oc get pods`.

## 8. Design Notes

- Covers **course-topics idea 7** (deploying an app).
- Establishes the **hello-dcs sample app** as the shared, evolving artifact for B01–B05; keep the manifests minimal so later workshops can add config (B02), probes/resources (B03), a fault (B04) and a PVC (B05).
- Runs in a **DEV-style session namespace** (native, no Kyverno) — consistent with the DCS self-service DEV model (A03). No vcluster.
- **Deliberate limitation:** config is baked in → B02 externalises it. Exposure is session-only → real Routes/PROD are Architect/ops territory (A06 already framed this).
