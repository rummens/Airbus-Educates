# Workshop Plan: lab-c02-pod-security-scc

## 1. Workshop Metadata

- **Name:** `lab-c02-pod-security-scc`
- **Title:** Pod Security & SCC on DCS
- **Description:** See why DCS runs workloads under the restricted policy, watch a root-assuming Pod get rejected at admission, and remediate its securityContext so it complies.
- **Duration:** 40m
- **Difficulty:** intermediate
- **Type:** Elective (Module C — Security & Compliance)
- **Prerequisites:** Module A (esp. A02 Kubernetes Essentials — Pods/Deployments, applying manifests).
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- Console: enabled; `security.token.enabled: true`
- Examiner: `enabled: true`
- Run location: **native OpenShift session namespace** (vcluster `enabled: false`). Critical: the session namespace already **enforces the `restricted` Pod Security Standard + `restricted-v2` SCC** — that enforcement is the whole point of the lab, so we must NOT relax it. `security.policy: restricted` (default), `budget: medium`.
- Workshop image: **`dcs-workshop-base`**.
- Params: trio; images via `{{< param dcs_registry >}}` / `$DCS_REGISTRY`.
- **No new sample image:** compliant and non-compliant cases both use `samples/hello-dcs:1.0`; the difference is the **Pod spec** (root/privileged request), which admission rejects. Rationale in Design Notes.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain what **Security Context Constraints (SCC)** and the **Pod Security Standards (PSA)** are, and why DCS runs tenant workloads under **restricted**.
- Describe the **arbitrary-UID** requirement and why images must not assume a fixed UID (esp. root).
- Read an admission **rejection** message and identify which control was violated.
- Fix a workload's `securityContext` (`runAsNonRoot`, drop `ALL` capabilities, `seccompProfile`, no privilege escalation) so it is admitted.
- Recognise when **baseline** is legitimately needed and that raising the policy is a governed, exceptional request.

## 4. Connection to Previous Workshop

Elective — assumes only Module A. **Already known:** deploy a Pod/Deployment with `oc apply`, read `oc get`/`oc describe`. **New here:** SCC vs PSA, the restricted controls, the `openshift.io/scc` annotation, `securityContext` fields, and reading an admission rejection. **Do NOT re-teach:** basic Pod/Deployment mechanics.

## 5. Exercise Files to Create

- `exercises/README.md` — placeholder.
- `exercises/pod-compliant.yaml` — a Pod running `$DCS_REGISTRY/samples/hello-dcs:1.0` with a correct restricted `securityContext` (runAsNonRoot, allowPrivilegeEscalation false, capabilities drop ALL, seccompProfile RuntimeDefault). Admits + runs.
- `exercises/pod-root.yaml` — same image, but `securityContext.runAsUser: 0` + `privileged: true` (and no drops). Violates restricted → rejected at admission.
- `exercises/pod-remediated.yaml` — created by the learner via editor actions from `pod-root.yaml` (or a copy) with the securityContext fixed; ends up equivalent to compliant. *(Plan may instead have the learner edit `pod-root.yaml` in place with `editor:replace-matching-text`.)*

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — overview + first-time note. DCS blurb: **Governance & compliance** (responsibility split) → `{{< param dcs_docs_base_url >}}/governance/overview`; note SCC/PSA are standard OpenShift → upstream.
- **`01-why-pod-security.md`** — concept. [Security Context Constraints](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html) and [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/); the **restricted** controls; **arbitrary UID** (why hardcoding UID/root breaks); how this maps to the DCS responsibility split (platform sets the floor; tenant builds compliant images). *(Concept page, no command.)*
- **`02-deploy-compliant.md`** —
  - `editor:open-file` `pod-compliant.yaml`; walk the `securityContext`.
  - `terminal:execute` `oc apply -f pod-compliant.yaml`; `oc get pod hello-compliant -w --request-timeout=60s` → examiner `verify-compliant-running` (Running; polling `.INF`).
  - `terminal:execute` `oc get pod hello-compliant -o jsonpath='{.metadata.annotations.openshift\.io/scc}'` → examiner `verify-scc-annotation` (equals `restricted-v2`). Explain the annotation shows which SCC admitted it.
- **`03-deploy-noncompliant.md`** —
  - `editor:open-file` `pod-root.yaml`; point at `runAsUser: 0` + `privileged: true`.
  - `terminal:execute` `oc apply -f pod-root.yaml` — expect an **admission rejection** (non-zero; PodSecurity "restricted" / SCC denies it). `{{< warning >}}` this is the expected failure.
  - Examiner `verify-root-rejected` — asserts the Pod `hello-root` is **absent / not Running** (the apply was denied). Diagnostic message points at `oc apply` output + the violated controls.
  - Read the rejection: identify `runAsNonRoot`, `privileged`, `allowPrivilegeEscalation`, capabilities as the violated controls.
- **`04-remediate.md`** —
  - Use `editor:replace-matching-text` to fix `pod-root.yaml` → drop `privileged`, set `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, `seccompProfile.type: RuntimeDefault`, remove `runAsUser: 0`.
  - `terminal:execute` `oc apply -f pod-root.yaml`; `oc get pod hello-root -w` → examiner `verify-remediated-running` (Running; polling).
  - Concept: **when baseline is needed** (e.g. a workload that genuinely needs a capability) → it's a **Security Exception** (ITSM/governed), not a self-service toggle. Blurb + DCS docs.
- **`98-your-feedback.md`** — standard (workshop=lab-c02-pod-security-scc).
- **`99-workshop-summary.md`** — recap; **Check Your Understanding** (3 Q): SCC vs PSA; why arbitrary-UID/no-root; what fields make a Pod restricted-compliant. Final examiner (`verify-scc-annotation`-style) as the knowledge-check action.

## 7. Terminal Working Directory Tracking

- Single working terminal in `~/exercises`. All `oc`/`editor` on local manifests — no `cd`.

## 8. Design Notes

- **Rejection comes from the Pod spec, not the image** — so no custom "root image" is needed (and none could be built/pushed air-gapped anyway). Admission (PSA restricted / restricted-v2 SCC) denies `privileged`/`runAsUser:0`. This is fully testable on any restricted namespace (CRC proved restricted SCC in A02 testing).
- **Do not relax the security policy** in `workshop.yaml` — the enforcement IS the lesson.
- Pairs with **C01** (image security) and **C03** (secrets) as the "runtime hardening" trio. No cross-dependency beyond Module A.
- Governance/exception thread is picked up again in **C05**.
