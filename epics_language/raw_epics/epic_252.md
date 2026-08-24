# TITLE: Project Capsule Integration & Tenant Provisioning POC
# STATE: opened
# PARENT: 220
# LABELS: P::2,complexity::medium,subproduct::naaS,type::dev

## Epic Description
This epic focuses on evaluating and implementing [**Project Capsule**](https://projectcapsule.dev/docs/) to provide a native multi-tenancy layer within OpenShift. The goal is to move away from the current custom "Namespace Provisioner" (Helm + Argo AppSets) toward a declarative **Tenant-based** model. This POC will validate if Capsule can successfully enforce the complex requirements of the Airbus DCS stack—including network isolation, global proxy configurations, and automated Harbor/Keycloak onboarding—while offering developers a self-service "Namespace-as-a-Service" experience.

## Importance of the Epic
Currently, our namespace provisioning relies on external automation to "stitch together" RBAC, Quotas, and Network Policies. This creates a "black-box" overhead and scaling challenges. By adopting Capsule, we treat a group of namespaces as a single **Tenant** entity. This ensures:
* **Policy Inheritance:** Global security and networking rules are applied once at the Tenant level and automatically inherited by all child namespaces.
* **Autonomous Scaling:** Tenant owners can create their own namespaces within their allocated resource boundaries without opening Jira tickets or waiting for ArgoCD syncs.
* **Native Integration:** Capsule integrates directly with OpenShift’s Admission Controllers, reducing the complexity of our custom provisioning logic.

## Functional Requirements (Mapping current Provisioner logic)

* **Tenant Abstraction:** Map the existing `project_namespace` and `requiredLabels` (e.g., `tenant_name`, `lifecycle`) into a Capsule `Tenant` resource.
* **Automated Network Isolation:**
    * Implement `NetworkPolicies` at the Tenant level to replace the current `allowedFlows` and `networkPolicy` (MasterNode IPs/VIPs) logic.
    * Validate the `GlobalProxy` injection to ensure all namespaces within a Tenant automatically receive the `proxyIp` configurations.
* **Resource Governance:**
    * Translate `resourceQuota` and `limitRange` blocks into Capsule `spec.resourceQuotas` and `spec.limitRanges`.
    * Ensure `requestsStorage` and `openshiftImageStorage` are enforced across the entire Tenant footprint.
* **RBAC & User Management:**
    * Use Capsule to automate the `project_owner_config` and `project_user_config`, granting `TenantOwner` roles to the specified `initialUsers`.
* **External Provider Integration (Sidecar/Hook):**
    * Develop a mechanism (likely via Capsule’s `NamespaceMetadata` or a custom operator) to trigger **Harbor** and **Keycloak** onboarding based on the `harborOnboardingConfig` and `ProviderConfig` inputs.

## Non-Functional Requirements

* **Performance:** Measure the latency of namespace creation when the Capsule Validating/Mutating webhooks are active.
* **Backward Compatibility:** Ensure existing namespaces not managed by Capsule remain unaffected (Namespace exclusion via labels).
* **Observability:** Integrate Capsule metrics into the OpenShift Monitoring stack to track resource consumption per Tenant.
* **GitOps Alignment:** The `Tenant` YAMLs must be deployable via the existing ArgoCD GitOps pipeline, replacing the current AppSet generators.

---

### Proposed High-Level Procedure

1. **Install Capsule:** Deploy the Capsule Operator into the `capsule-system` namespace on the OpenShift Bare-Metal cluster.
2. **Define the Tenant Template:** Create a "Gold Tenant" manifest that includes:
    * The DCS global `NetworkPolicies`.
    * The standard `LimitRanges` (512Mi RAM, 500m CPU).
    * Mandatory labels (cost_center, tenant_owner).
3. **Provision a Test Tenant:** Apply a `Tenant` CR for `claim-test-01` using the user list and quotas from the reference data.
4. **Validation of Self-Service:** Log in as `projectowneruser01@airbus.com` and verify the ability to create new namespaces (e.g., `claim-test-01-dev`) without cluster-admin rights.
5. **Security Audit:** Verify that a pod in `Tenant A` cannot reach `Tenant B` unless specifically allowed via the `allowedFlows` logic ported to Capsule.



## Roadmap Summary
Evaluate [Project Capsule](https://projectcapsule.dev/docs/) as a replacement for the custom Helm/Argo namespace provisioner to enable native, policy-driven multi-tenancy and developer self-service on OpenShift.