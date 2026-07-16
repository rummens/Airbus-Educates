# Workshop Plan: lab-a06-terms-namespaces-tenancy

## 1. Workshop Metadata

- **Name:** `lab-a06-terms-namespaces-tenancy`
- **Title:** Terms — Namespaces & Tenancy
- **Description:** Name the DCS terms you keep hearing — Namespace, Tenant, and the DEV/PROD namespace types — and *see* namespace isolation for real by deploying the same app into two namespaces at once. Vocabulary plus a hands-on isolation demo, not the deep governance model.
- **Duration:** 30m
- **Difficulty:** beginner
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A02 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (learners view/apply provided manifests; no hand-typing)
- OpenShift access: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Params: the trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`)
- **No vcluster** — two *peer* namespaces are enough to show isolation; vcluster is reserved for the DEV/PROD *policy* demo (Developer B06). This lab stays on the shared session cluster.
- **Two extra namespaces, pre-provisioned by Educates via `session.objects`:** create `{{ session_namespace }}-app-a` and `{{ session_namespace }}-app-b`, each with a `RoleBinding` granting the session service account `edit` so the learner can deploy into both. (See the authoring skill's `session-objects-reference`.) Names are session-scoped variables — never hardcoded. Clean-up is automatic when the session ends.
- Sample app: **hello-dcs** (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`) in CLI mode — the isolation demo only needs the pods to exist and be inspectable, not exposed.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Define a **Namespace**: the unit of isolation and consumption on DCS (Namespace as a Service), what it holds, and what makes one the *active* namespace in your context.
- **Deploy the same app into two different namespaces and observe isolation first-hand** — identical names coexist, each namespace lists only its own objects, and an action in one namespace does not affect the other.
- **List concrete reasons to split workloads across namespaces** — e.g. running separate DEV / QA / PROD instances of one app, team/blast-radius isolation, independent quotas and RBAC, and naming freedom.
- Explain the **Tenant → Namespaces** model: a Tenant is the org-level unit that owns one or more Namespaces; there is **no separate "project" layer** — "project" is just OpenShift's word for a namespace.
- State that **DEV** and **PROD** namespace types exist and differ (governance details deferred to the Developer track).

## 4. Connection to Previous Workshop

**What the learner already knows** (from A02: Deploy Your First App, and A01):
- Runs `oc`, finds their project, deploys and inspects a workload in a namespace.
- Has been *working inside* a namespace this whole time without a name for it.
- Knows the DCS **cluster** model (Sandbox/PROD) from A01 — call out that a cluster is *not* a namespace, to head off confusion.

**What is new in this workshop:**
- The vocabulary: Namespace, Tenant, DEV/PROD types.
- A **hands-on isolation demo across two namespaces** and the reasoning for why you'd split things up.

**What should NOT be re-taught:**
- No Deployment/Service internals (A02) — reuse the deploy skill, don't re-explain it.
- No `oc` orientation basics beyond a one-line recap.

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the Terms — Namespaces & Tenancy workshop."

### exercises/app.yaml
**Purpose:** The identical Deployment the learner applies into *both* namespaces to demonstrate name isolation. Applied with `oc apply -f app.yaml -n <namespace>` (namespace supplied on the command line, so the same file targets both).
**Initial contents:** A minimal `hello-dcs` Deployment named `hello` (fixed name on purpose — the point is that the same name lives independently in each namespace), image `{{< param dcs_registry >}}/samples/hello-dcs:1.0`, MODE=CLI, non-root, small resource requests. No hardcoded namespace in the manifest. **Note:** if the image ref needs `${DCS_REGISTRY}` substitution, apply via `envsubst < app.yaml | oc apply -n <ns> -f -` (house pattern).

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame the lab as "you've been using these things — here are their names, and here's isolation for real."
**Content outline:**
- `{{< param product_name >}}` framing; pick up from A02 ("everything you deployed lived *somewhere* — let's name that place, then watch two of them stay out of each other's way").
- What You'll Learn; 30m / beginner. DCS-specific blurb + link `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access` (overview only). No actions.

### 01-what-is-a-namespace.md
**Purpose:** Define Namespace as the DCS unit of isolation and consumption.
**Content outline:**
- Concept, folded onto the learner's own app: a Namespace groups and isolates your workloads; on DCS it's the consumption unit (Namespace as a Service). "Active namespace" = the one your `oc` context points at.
- `oc project` (`terminal:execute`) → examiner check: reports the current project. Note "project" == "namespace" (OpenShift wording), no separate layer.
- `oc get all` (`terminal:execute`) → examiner check: succeeds — the objects from A02 all live in this one namespace.
- `Namespace` construct → [upstream](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/); NaaS framing → `{{< param dcs_docs_base_url >}}/concepts/tenancy-and-access` + blurb.

### 02-isolation-in-action.md
**Purpose:** Prove isolation by deploying the same app into two pre-provisioned namespaces.
**Content outline:**
- Point out the two namespaces Educates pre-created for you: `{{ session_namespace }}-app-a` and `-app-b` (`oc get ns | grep app-` — examiner check: both exist).
- Open `app.yaml` (`editor:open-file`) — one Deployment named `hello`, no namespace baked in.
- Apply it into **both** namespaces (split terminal): `oc apply -f app.yaml -n {{ session_namespace }}-app-a` (`execute-1`) and `... -n ...-app-b` (`execute-2`). Two examiner checks: rollout available in each.
- **Same name, two independent copies:** `oc get deas/pods -n ...-app-a` vs `-n ...-app-b` → each lists only its own `hello`; the identical name coexists with no clash. Examiner checks per namespace.
- **Actions don't leak:** scale `hello` to 0 (or delete a pod) in `-app-a`; show `-app-b` is untouched (`oc get pods` in both). Examiner check: `-app-b` still Running while `-app-a` changed.
- Fold the takeaway inline: the namespace is the isolation boundary — names, objects, and actions are scoped to it.

### 03-why-split-into-namespaces.md
**Purpose:** Turn the demo into the reasons a real tenant uses multiple namespaces.
**Content outline:**
- Now that they've *seen* it, name the reasons (concise, DCS-flavoured):
  - **Separate instances of one app** — e.g. **DEV / QA / PROD** copies of the same service, each in its own namespace, same names, independent lifecycles. (Forward pointer: the DEV/PROD *namespace-type* governance is A06→B06.)
  - **Team / blast-radius isolation** — a mistake in one namespace can't take down another.
  - **Independent quotas & RBAC** — each namespace gets its own resource budget and access rules (deep dive: Developer B05).
  - **Naming freedom** — the `hello` clash you *didn't* get is the point; teams don't have to coordinate names.
- One knowledge check (radio): "You want DEV, QA and PROD copies of the same app with the same names running at once — what gives you that cleanly?" → separate namespaces.

### 04-tenants-and-namespace-types.md
**Purpose:** Place the namespace in the Tenant → Namespaces model and name the DEV/PROD types.
**Content outline:**
- **Tenant → Namespaces**: the Tenant is the org-level owner (accountability/recharging); it owns one or more Namespaces. Explicitly dispel the "project is a third layer" confusion.
- **DEV vs PROD** namespace types *exist* and behave differently — say so, defer the mechanics ("you'll see exactly how in the Developer track, B06").
- `oc get namespace $(oc project -q) -o jsonpath='{.metadata.labels}'` (or `oc describe namespace ...`) (`terminal:execute`) → examiner check: labels/annotations printed; use them to point out the tenant/type markers on the learner's own namespace.
- Distinguish once more: **cluster** (Sandbox/PROD, from A01) ≠ **namespace type** (DEV/PROD).

### 99-workshop-summary.md
**Purpose:** Recap and bridge to the Developer track.
**Content outline:**
- Recap: Namespace (unit of isolation/consumption), isolation seen across two namespaces, why you split, Tenant → Namespaces (no project layer), DEV/PROD types exist.
- **Check Your Understanding** (3 Q): what a namespace isolates; one concrete reason to use multiple namespaces; whether "project" is a separate layer.
- Bridge forward: the *deep* model is the Developer track — **B05** (RBAC, Tenancy & Namespaces) and **B06** (DEV/PROD policy enforcement, e.g. Kyverno on PROD, Route capability).

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises` (where `app.yaml` lives).
- No `cd`. The learner's *own* namespace is the default context (no `-n`); the two demo namespaces are always addressed with an explicit `-n {{ session_namespace }}-app-a|-app-b`.
- Command patterns: `oc apply -f app.yaml -n <ns>`, read-only `oc get`/`describe`, `oc scale`.

## 8. Design Notes

- Covers ideas **3 (light)** and **5 (light)** — vocabulary plus a concrete isolation demo. Draws terms from old A03 (Namespace model) and old A05 (Access & Tenancy); the deep governance model (DEV/PROD policy enforcement, RBAC internals, quotas, Kyverno) is deliberately **not** here — it moves to Developer B05/B06.
- **Made active (2026-07-16 author note):** rather than observe-only, Educates pre-provisions two extra namespaces and the learner deploys the same app into both to *see* isolation (same name coexists, actions don't leak), then the reasons-to-split page lands with evidence behind it. This is the "be more active explaining NS" change.
- **Session provisioning risk:** creating two namespaces + RoleBindings per session needs the Educates session SA to have namespace-create rights (a `session.objects` cluster-scoped grant). Validate on the target cluster; on a restricted cluster, fall back to two pre-created fixed namespaces or a single-namespace label demo. Track in tasks.
- **Deliberate gap:** learner is told DEV/PROD namespace *types* differ but not *how* (Kyverno, Route capability) — the hook into B06. Keep the phrasing curiosity-inducing.
- **Tenancy model (confirmed):** two levels only — Tenant → Namespaces. Never teach a three-level Namespace→Project→Tenant model. Mention "project" only to dispel confusion.
- Placed *after* the hands-on happy path (A01–A05), part of the A06–A08 "now you know the landscape" tail; but unlike A07/A08 it is genuinely hands-on.
