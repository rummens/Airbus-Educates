# Workshop Plan: lab-a02-deploy-first-app

## 1. Workshop Metadata

- **Name:** `lab-a02-deploy-first-app`
- **Title:** Deploy Your First App *(the quick win)*
- **Description:** Get your own app running on DCS fast — create a Deployment from a Harbor image, customise it, reach it, change it and watch it roll out — then peek at the YAML behind it to see how Kubernetes really works.
- **Duration:** 30m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A01 (What is DCS?)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view the revealed YAML; no hand-editing)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: **not** enabled — keep the quick win CLI-first; the console tour is A08.
- Examiner: `enabled: true`
- Budget: `medium` (small deployment + a little rollout headroom)
- Workshop image: `dcs-workshop-base`
- Sample app: `{{< param dcs_registry >}}/samples/hello-dcs:1.0` — Harbor-mirrored, non-root, HTTP on port 8080.
- **vcluster decision:** `false` — plain session namespace. A single-app deploy needs nothing cluster-scoped; the session namespace *is* the learner's workspace.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:
- Deploy an existing Harbor image to their namespace with `oc create deployment`.
- Customise the running app with an environment variable (`oc set env`).
- Reach the app locally (session proxy / `oc port-forward` + `curl`).
- Change config and watch the Deployment roll out a new version.
- Read the generated YAML and explain the Deployment → ReplicaSet → Pod ownership chain and how labels/selectors tie them together.

## 4. Connection to Previous Workshop

**Already known** (from A01): what DCS is; containers vs images; *why* Kubernetes (scheduling, self-healing, scaling, declarative); how to run `oc` and find the session namespace (`oc whoami`, `oc project`). Do **not** re-explain orientation commands or re-motivate Kubernetes — A01 did that; this workshop is the payoff.

**What is new here:**
- Creating a real workload imperatively (`oc create deployment`) from a Harbor image.
- Customising it live (`oc set env`) and reaching it locally.
- Watching a rollout happen.
- **Reading the YAML** that `oc` generated — the bridge from imperative "do this" to declarative "desired state," which every later Core lab (A03–A05) builds on.

**What should NOT be re-taught:** the concept of *why* declarative/self-healing matters (A01 established it — here we make it concrete); basic `oc` orientation.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder: "Exercise files for Deploy Your First App. In this lab you create the Deployment with `oc` — no manifest to start."

Note: this lab is deliberately **imperative-first** — the learner *generates* the Deployment with `oc create deployment` rather than applying a pre-written manifest. The YAML is *revealed* at the end (`oc get deploy -o yaml`), not authored. So no `deployment.yaml`/`service.yaml` starter files (that changes in A03, where declarative manifests begin).

## 6. Workshop Instruction Pages

Quick-win first; keep momentum; defer depth to the final reveal page.

- **`00-workshop-overview.md`** — intro + first-time note. "Let's get something running." Objectives; prerequisite A01; introduce the **hello-dcs** sample app (a tiny web server on 8080, image in Harbor at `{{< param dcs_registry >}}`, pulled air-gapped from the internal registry — one-line blurb + `{{< param dcs_docs_base_url >}}` pointer, no deep dive). No actions beyond framing.
- **`01-deploy-it.md`** — the fast win. `terminal:execute` `oc create deployment hello-dcs --image={{< param dcs_registry >}}/samples/hello-dcs:1.0`; `oc rollout status deploy/hello-dcs`; expected output. Fold in *just enough*: "a Deployment tells DCS to keep one copy of this image running." Examiner: 1 ready replica.
- **`02-customise-it.md`** — make it yours. `oc set env deploy/hello-dcs GREETING="Hello from <name>"` (whatever env the sample reads); explain env vars as the simplest way to change behaviour without rebuilding the image. `oc rollout status`. Examiner: the env var is set on the Deployment (`oc set env --list` / describe).
- **`03-reach-it.md`** — see it respond. Reach the app locally: `oc port-forward deploy/hello-dcs 8080:8080` in the **lower split terminal** (`execute-2`), then `curl -s localhost:8080` in the **upper** (`execute-1`). Explain this is a *local* tunnel for testing — real external exposure (a Route) comes in A04 (forward pointer, don't teach). Examiner: `curl` returns HTTP 200 and the customised greeting.
- **`04-change-and-watch.md`** — the rollout, made visible. In the lower terminal `watch oc get pods -l app=hello-dcs` (`execute-2`); in the upper, change the env var again (`oc set env deploy/hello-dcs GREETING=...`) and watch old pod terminate / new pod start — self-healing/declarative in action, the A01 promise made concrete. `oc rollout status`. Re-`curl` to confirm the new value. Examiner: rollout complete and app serves the new greeting.
- **`05-whats-behind-it.md`** — the reveal (imperative → declarative bridge). `oc get deploy hello-dcs -o yaml` (open in editor via `editor:open-file` on a saved copy, or view inline); `editor:select-matching-text` to highlight `spec.replicas`, `spec.selector.matchLabels`, and `template.metadata.labels`. Explain the **Deployment → ReplicaSet → Pod** ownership chain: `oc get all -l app=hello-dcs` shows the ReplicaSet the Deployment created and the Pod the ReplicaSet created. Labels/selectors are the glue. Point out: everything you did imperatively is captured in this desired-state document — that's what A03 onward will write directly. Examiner: `oc get rs -l app=hello-dcs` shows a ReplicaSet owned by the Deployment (or: `oc get all -l app=hello-dcs` succeeds and shows deploy+rs+pod).
- **`99-workshop-summary.md`** — recap: deploy → customise → reach → roll out → read the YAML. Deliberate gap: config is set ad-hoc with `oc set env` and doesn't scale to many settings/secrets → motivates **A03 (Configure & Troubleshoot)**. **Check Your Understanding** (4 Q): what a Deployment guarantees; what `oc set env` triggers; what owns a Pod; what labels/selectors do.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`. No `cd`.
- **Split terminal:** upper `execute-1` = commands/`curl`; lower `execute-2` = long-running `oc port-forward` and `watch oc get pods`. Track that port-forward stays running in `execute-2` while `curl` runs in `execute-1`.
- Patterns: `oc create deployment`, `oc set env deploy/…`, `oc rollout status deploy/…`, `oc port-forward deploy/… 8080:8080`, `curl -s localhost:8080`, `oc get all -l app=hello-dcs`, `oc get deploy … -o yaml`.

## 8. Design Notes

- Covers **course-topics ideas 2 and 7**. This is **the flagship quick win** — a learner's own app running on DCS within minutes. Keep pages short and the momentum high; the only "depth" page is the final reveal.
- **Hybrid style (deliberate):** imperative first for speed and confidence, declarative revealed last so the learner *earns* the YAML instead of being handed it. This is the merge of old A02 (Kubernetes Essentials — declarative-heavy, 9 pages) + old B01 (Deploy First App) into one tight lab. Depth that was in old A02 (scaling/self-healing internals, exec/rsh, full querying tour, Service DNS) is intentionally NOT here — scaling/health and deeper querying move to the Developer track; exposure moves to A04; Services proper move to A04.
- **hello-dcs is the shared, evolving sample app** across A02–A05 — keep the footprint minimal so A03 can add config + a fault, A04 a Service/Route, A05 a PVC.
- **Local reach via port-forward** (not a Service yet) keeps A02 self-contained — Services + real Routes are the whole point of A04, so don't pre-empt them.
- Explicit resource requests aren't set here (imperative `create deployment` gives defaults) — acceptable for one small replica within the medium budget; A03+ manifests can add them.
