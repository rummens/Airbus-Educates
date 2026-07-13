# Pod Security & SCC on DCS

**See why DCS admits every workload under the restricted policy, watch a root-assuming Pod get rejected at admission, and fix its securityContext so it complies.**

Every workload on the Digital Container Service (DCS) is admitted under a restricted security policy — no root, no privilege, no assuming the image owns the box. This lab shows you why that floor exists, then makes it concrete: you'll deploy a compliant Pod and confirm which SCC admitted it, watch a non-compliant Pod get rejected the moment you apply it, read the rejection to spot the violated control, and remediate the workload's `securityContext` until it is admitted. The rules come from two standard OpenShift mechanisms — Security Context Constraints (SCC) and the Pod Security Standards (PSA) — working together at admission; what is DCS-specific is the governance that makes raising the floor a deliberate, governed exception rather than a self-service toggle.

- **Track / module:** Security & Compliance — Secure on DCS (Module C) · Lab 2 of 5
- **Audience:** Intermediate — comfortable applying manifests and reading `oc get` / `oc describe`
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a02-kubernetes-essentials · external: basic Linux CLI, familiarity with Pods

## By the end of this lab you'll be able to

- Explain what SCC and the Pod Security Standards are, and why DCS runs tenant workloads under restricted.
- Describe the arbitrary-UID requirement and why an image must not assume a fixed UID — least of all root.
- Deploy a Pod with a correct restricted `securityContext` and confirm the SCC that admitted it.
- Read an admission rejection and identify which control was violated.
- Remediate a workload's `securityContext` (`runAsNonRoot`, drop `ALL` capabilities, `seccompProfile`, no privilege escalation) so it is admitted.
- Recognise when baseline is legitimately needed, and that raising the policy is a governed Security Exception.

## What you'll do

- Deploy a Pod with a correct restricted `securityContext` and confirm the admitting SCC.
- Apply a root-assuming Pod, watch admission reject it, and read the rejection to find the violated control.
- Remediate the `securityContext` field by field until the workload is admitted.
