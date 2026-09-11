# Workshop Plan: lab-o04-dev-prod-namespaces

## 1. Metadata
- **Name:** `lab-o04-dev-prod-namespaces` · **Title:** DEV vs PROD Namespaces
- **Duration:** 25m · **Difficulty:** intermediate · **Track:** Operate & Observe, order `40`
- **Lifecycle:** `prod` — the lab creates a Route in its PROD-type peer namespace (label_check enforces this)
- **Prerequisites (curricular):** Core *Terms — Namespaces & Tenancy*, *Health & Resources*
- **Status:** New design, 2026-09-11. Live-verified 22/22.

## 2. Why the vcluster went away
The superseded version ran inside a **vcluster** with Kyverno applied by the learner, assuming a vcluster ships Kyverno's CRDs and controller. It does not. This version drops the vcluster: Kyverno runs on the host cluster, so every refusal the learner sees comes from the real admission path.

`session.objects` provisions two peer namespaces (one of each type) plus a **per-session ClusterPolicy** whose name *and* namespaceSelector are scoped to the session — concurrent sessions cannot collide, and no namespace outside the session is ever matched.

## 3. Measured before authoring
| Behaviour | Result |
|---|---|
| Unsized Deployment → DEV | admitted |
| Unsized Deployment → PROD | refused at `oc apply`, failing path named (Kyverno auto-generates the Deployment rule from the Pod rule) |
| Route → DEV | refused: *"A Route needs a PROD-type namespace."* |
| Sized Deployment + Route → PROD | admitted, real host assigned |
| Tenant reading the ClusterPolicy | **Forbidden** — cluster-scoped, platform-owned |

## 4. Design notes
- The last finding changed page 01: the learner runs `oc auth can-i list clusterpolicies`, gets `no`, and that becomes the lesson — **you meet platform policy through its decisions, not by reading it**. The policy's existence is proved by the two refusals, each naming its rule.
- Two graders assert **absences** (no Route in DEV, no unsized Deployment in PROD), because that is what admission control produces. On a cluster without Kyverno they fail loudly rather than quietly teaching something untrue.
- Ends on promotion: the same image, the same manifest, a fresh apply — never an edit in place, because the next promotion silently overwrites it.
