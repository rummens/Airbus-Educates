# Workshop Plan: lab-b06-dev-prod-namespaces

## 1. Workshop Metadata

- **Name:** `lab-b06-dev-prod-namespaces`
- **Title:** DEV vs PROD Namespaces & Policies
- **Description:** The two DCS namespace types differ by policy posture. See a DEV and a PROD namespace side by side, watch a Route get blocked in DEV and succeed in PROD, inspect the Kyverno policy PROD enforces, and understand why you promote instead of editing PROD in place.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B05 (RBAC, Tenancy & Namespaces)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-b--developer-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view + apply manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- **Virtual cluster: enabled** (`spec.session.applications.vcluster.enabled: true`) — gives cluster-scoped rights to create/inspect *two* namespaces so DEV and PROD are visible side by side. vcluster component images must be Harbor-mirrored (see air-gapped-images-reference).
- Web console: enabled (view the namespaces, Routes, policy)
- Examiner: `enabled: true`
- Workshop image: `dcs-workshop-base`
- Sample image: reuse `{{< param dcs_registry >}}/samples/hello-dcs:1.0`
- Params: the trio.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Distinguish the DCS **DEV vs PROD** namespace types by their **policy posture**, not just their names.
- Explain the two concrete differences: **PROD enforces harsher policies (Kyverno) AND can create Routes**; **DEV has looser policies BUT cannot create Routes**.
- Deploy a workload to DEV, observe a Route being blocked there, and create the Route successfully in PROD.
- Read the Kyverno policy that PROD enforces and explain what it checks.
- Describe promotion (DEV → PROD — don't edit PROD in place) and the trade-off the split buys.

## 4. Connection to Previous Workshop

**What the learner already knows** (from B05: RBAC, Tenancy & Namespaces, and Core A06):
- The Tenant → Namespaces model and that DEV/PROD types *exist* (A06 named them; B05 deepened tenancy + RBAC).
- How to read a namespace's labels and its RBAC/quota.
- From **Core A04** (Routes): a Route exposed the app — and *required a PROD namespace*. That requirement was stated but not explained.

**What is new in this workshop:**
- *Why* A04's Route needed PROD — the DEV-cannot-Route / PROD-can-Route rule, seen live.
- The Kyverno admission-policy mechanism that makes PROD stricter.
- The promotion model and the loose-DEV / strict-PROD trade-off.

**What should NOT be re-taught:**
- Do not re-teach Deployment/Service mechanics (Core A02) or Route basics (Core A04) — reuse them, focus on *where* they run and *what policy applies*.
- Do not re-define Tenant/Namespace vocabulary (A06) or RBAC (B05).

## 5. Exercise Files to Create

### exercises/README.md
Placeholder: "Exercise files for the DEV vs PROD Namespaces & Policies workshop."

### exercises/dev-namespace.yaml
**Purpose:** The DEV-type namespace created in the vcluster.
**Initial contents:** A `Namespace` labelled as DEV type (loose policy posture).

### exercises/prod-namespace.yaml
**Purpose:** The PROD-type namespace created in the vcluster.
**Initial contents:** A `Namespace` labelled as PROD type (Kyverno-enforced).

### exercises/kyverno-policy.yaml
**Purpose:** The representative PROD policy that makes the enforcement difference demonstrable.
**Initial contents:** A Kyverno `ClusterPolicy` (or `Policy`) that applies to PROD-type namespaces only — e.g. requires a resources block / non-root / an owner label — so DEV deploys unchanged and PROD is guarded.

### exercises/hello-dcs.yaml
**Purpose:** The workload deployed into both namespaces.
**Initial contents:** Combined Deployment + Service for `hello-dcs`, image via `${DCS_REGISTRY}/samples/hello-dcs:1.0`.

### exercises/hello-dcs-route.yaml
**Purpose:** The Route the learner tries in DEV (blocked) then in PROD (succeeds).
**Initial contents:** A `Route` targeting the `hello-dcs` Service.

## 6. Workshop Instruction Pages

### 00-workshop-overview.md
**Purpose:** Frame around the unanswered question from Core A04.
**Content outline:**
- `{{< param product_name >}}` framing + first-time note; open on the hook: "In Core A04 your Route needed a PROD namespace. Here's why."
- What You'll Learn; 40m / intermediate. DCS-specific blurb + link `{{< param dcs_docs_base_url >}}/concepts/namespace-types`. No actions.

### 01-two-namespace-types.md
**Purpose:** Establish the policy-posture model and put a DEV and PROD namespace side by side.
**Content outline:**
- The headline: DEV = looser policy, **no Routes**; PROD = stricter Kyverno enforcement, **can create Routes**. A **quick-comparison DEV vs PROD** table with the Kyverno-enforcement and Route rows called out. Introduce Kyverno briefly (policy-as-admission-control) + [Kyverno](https://kyverno.io/docs/) upstream.
- `oc apply -f dev-namespace.yaml` and `oc apply -f prod-namespace.yaml` (`terminal:execute`) → check: both namespaces exist with their type labels.
- `oc get namespaces` (in vcluster) → check: both listed. DCS-specific → `{{< param dcs_docs_base_url >}}/concepts/namespace-types` + blurb.

### 02-deploy-to-dev.md
**Purpose:** Deploy to DEV (loose) and hit the Route wall.
**Content outline:**
- `oc apply -f kyverno-policy.yaml` (`terminal:execute`) → check: PROD-only policy present.
- Deploy the workload to DEV: `envsubst < hello-dcs.yaml | oc apply -n <dev-ns> -f -` (image ref uses `${DCS_REGISTRY}` — never plain `oc apply`) → polling check: workload ready in DEV, unchanged (loose policy).
- Attempt the Route in DEV: `oc apply -n <dev-ns> -f hello-dcs-route.yaml` → **examiner checks the Route is blocked** in DEV (diagnose-style; hint: DEV cannot expose Routes).

### 03-do-it-in-prod.md
**Purpose:** Same workload + Route in PROD — Route works, stricter Kyverno applies.
**Content outline:**
- Deploy to PROD: `envsubst < hello-dcs.yaml | oc apply -n <prod-ns> -f -` → observe the **Kyverno policy** evaluate the workload (block/mutate where DEV accepted it unchanged); read the admission message. Check asserts the enforcement fires.
- Create the Route in PROD: `oc apply -n <prod-ns> -f hello-dcs-route.yaml` → **examiner checks the Route is created** (the PROD-only capability, contrast with page 02's block).
- `oc get route -n <prod-ns>` → check: Route present with a host.

### 04-the-policy-and-promotion.md
**Purpose:** Inspect what PROD enforces and understand promotion.
**Content outline:**
- `oc get clusterpolicy` / `oc describe clusterpolicy <name>` (`terminal:execute`) → check: the PROD policy's rules shown; walk through what it validates.
- Concept: **promotion DEV → PROD** — you re-deploy a vetted workload into PROD, you don't edit PROD in place; the loose-DEV / strict-PROD split is the trade-off (fast iteration vs guarded production). No live promotion tooling — conceptual + docs link `{{< param dcs_docs_base_url >}}/concepts/namespace-types`.

### 99-workshop-summary.md
**Purpose:** Recap and bridge forward.
**Content outline:**
- Recap: DEV (loose, no Route) vs PROD (Kyverno-enforced, Route-capable); the Route block/success contrast; promotion, not in-place edits.
- **Check Your Understanding** (3 Q): which type can create a Route; what makes PROD stricter (Kyverno); how work moves DEV → PROD.
- Bridge to **B07** (Scaling, Health & Resources — make the workload robust within its namespace budget) and note the policy mindset returns in **B08** (Operators) and the Security track.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`.
- No `cd` changes, but every command is explicitly `-n <namespace>` because the learner works across **two** namespaces (DEV and PROD) in the vcluster — track which namespace each step targets.
- Command patterns: `oc apply -f <file>` for namespaces/policy; `envsubst < f.yaml | oc apply -n <ns> -f -` for any manifest with a `${DCS_REGISTRY}` image ref; `oc get`/`oc describe` for Routes and the Kyverno policy.

## 8. Design Notes

- **New lab (the missing one)** + deep model carried from old A03 (Namespace model, vcluster). Covers course-module-b idea 3. The vocabulary layer now lives in Core A06; this lab is purely the *mechanism and enforcement*.
- **vcluster is required** — it is the cheapest way to give the learner two real namespaces with differing policy so the DEV-vs-PROD difference is tangible. Confirm vcluster sizing/availability on DCS (task in tasks.md).
- **Kyverno must be present** in the test cluster to demonstrate PROD enforcement. If unavailable, deliver pages 02–03's PROD enforcement as annotated, **screenshot-driven** steps (as old A03 planned); the Route block/success contrast can still be shown via the namespace-type rule.
- **Carry-forward bug:** any manifest with `${DCS_REGISTRY}` (here `hello-dcs.yaml`) is applied with `envsubst < f.yaml | oc apply -f -`, never plain `oc apply` — the variable won't expand otherwise.
- Reuses the `hello-dcs` sample to avoid new images. Exact production PROD policy set is a P2 to confirm — the *mechanism* (Kyverno) is settled.
