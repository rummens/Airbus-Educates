# TITLE: Kyverno Enhancements
# STATE: opened
# PARENT: 220
# LABELS: P::3,complexity::low,component::kyverno,subproduct::naaS

## Epic Description

This epic marks the evolution of the Digital Container Service (DCS) from basic policy enforcement to a sophisticated, automated governance framework. Following the initial MVP release, this epic focuses on refining the security posture and operational efficiency of the managed platform. It introduces advanced **mutation templates**, broadens compliance with **BSI (Federal Office for Information Security) standards**, and implements the **Kyverno Policy Reporter** to provide transparent visibility into policy violations. By optimizing how policies are applied across different environments (DEV vs. PROD), this epic ensures that security guardrails are robust yet flexible enough to support rapid development.

## Importance of the Epic

In a multi-tenant Namespace-as-a-Service (NaaS) environment, policy management is not a "set and forget" task. As the platform matures, the need for more granular control increases. This epic is vital because it addresses the complexity of managing global security standards while maintaining developer velocity. By automating the labeling of resources and providing a "permissive baseline" for development namespaces, we reduce friction for users. Simultaneously, by hardening **NetworkPolicies**, restricting **global pull secrets**, and auditing **Pod Security Contexts**, we mitigate the risk of lateral movement and unauthorized access, fulfilling the high security requirements inherent to the DCS platform.

## Functional Requirements

* **Advanced Policy Logic:**
  * Implement **templating for remediations** in mutating policies to allow for dynamic, context-aware resource adjustments.
  * Transition from global `validationFailureAction` tags to granular, **rule-level `failureAction**` settings for more precise enforcement control.


* **Expanded Compliance & Security:**
  * Integrate missing **BSI policies** to meet federal security standards.
  * Enforce **Secure Image** usage policies and restrict access to the cluster's global pull secret to prevent unauthorized registry access.
  * Hardening of **NetworkPolicies** through automated governance rules to ensure default-deny postures where appropriate.


* **Governance & Visibility:**
  * Deploy the **Kyverno Policy Reporter** to provide a centralized dashboard for real-time policy violation tracking and auditing.
  * Automate **resource labeling** via Kyverno policies to ensure consistent metadata for billing and inventory management.


* **Developer Experience (DevX):**
  * Establish a **permissive policy baseline** for DEV namespaces, disabling non-critical checks to allow for experimentation without compromising core platform stability.
  * Review and manage Pod Security Standard (PSS) violations for whitelisted applications to prevent alert fatigue.



## Non-Functional Requirements

* **Modularization:** Refactor the policy architecture to split monolithic values files into **app-specific policy files**, improving maintainability and code readability.
* **Operational Integrity:** Disable conflicting OpenShift Pod Security Admission (PSA) alerts to ensure a "clean" monitoring environment where only actionable Kyverno alerts are surfaced.
* **Auditability:** Maintain a comprehensive audit trail of Pod Security Contexts across the platform to ensure ongoing compliance with the DCS security roadmap.
* **Performance:** Ensure that the increased number of policies does not introduce significant latency into the Kubernetes API admission controller path.

---

### Proposed High-Level Procedure

1. **Policy Refactoring:** Move existing policies into the new modular file structure to prepare for Release 4 enhancements.
2. **Environment Calibration:** Apply the permissive baselines to DEV clusters while simultaneously rolling out the restricted NetworkPolicies and BSI standards to PROD.
3. **Visualization Rollout:** Install and configure the Policy Reporter, integrating it with the DCS monitoring stack for unified reporting.
4. **Verification:** Utilize the **Kyverno test pipeline** (developed in Release 2) to validate that new mutating templates do not cause unintended resource conflicts.

## Roadmap Summary

Enhance the DCS governance framework by implementing advanced Kyverno policies, BSI compliance standards, and a centralized Policy Reporter to ensure a secure, scalable, and developer-friendly managed platform.