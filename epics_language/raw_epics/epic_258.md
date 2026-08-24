# TITLE: DCS Upgrades - Release 5
# STATE: opened
# PARENT: 220
# LABELS: P::1,complexity::high,subproduct::naaS

## **⬆️ Epic Description: OpenShift Version Upgrades (v4.20)**

This Epic covers the complete planning, execution, and validation of the version upgrades for the Digital Container Service (DCS) managed OpenShift platform: moving from the current version to **OpenShift 4.20**. The primary objective is to maintain platform currency, integrate critical new features, and ensure the long-term support and security posture of the DCS environment. This process demands meticulous pre-upgrade analysis of all installed Operators and custom components (e.g., Keycloak, GitOps, Storage, Security tools) and execution of a **fully automated, non-disruptive rolling upgrade** strategy to minimize impact on internal development teams.
**This also includes the update** of all other serivces to the latest stable version of each service (as indicated above)

---

## **📈 Importance of the Epic**

Regular, managed platform upgrades are **absolutely critical** for the stability, security, and competitiveness of the DCS offering. This Epic is vital because:

1. **Ensures Security and Compliance:** Newer OpenShift versions contain critical security patches, ensuring the underlying platform meets enterprise and regulatory security standards.  
2. **Unlocks Innovation:** Provides access to essential new features, performance enhancements, and stability fixes in the OpenShift platform and its core operators, which are necessary for supporting modern developer workloads.  
3. **Prevents Technical Debt:** Avoids falling into an unsupported version state, which would drastically increase the risk, complexity, and downtime associated with future, larger version jumps.

---

## **✅ Functional Requirements**

The upgrade process must adhere to a strict, phased, and comprehensive plan:

* **Pre-Upgrade Analysis and Validation:**  
  * **Operator Compatibility Assessment:** For each target version, verify that all installed DCS operators (e.g., Kyverno, Keycloak, Trident, Loki, ArgoCD) have compatible, supported versions available for the new OpenShift release train.  
  * **Custom Component Readiness:** Review all non-operator DCS components (e.g., custom webhooks, monitoring stack configurations, base images) for necessary schema changes or deprecated APIs, remediating potential conflicts *before* the upgrade starts.  
  * **Staging/Sandbox Validation:** Execute the full upgrade process on a dedicated non-production **Sandbox environment** first, running the entire **Test Automation Suite** (including performance tests) to prove stability before proceeding to higher environments.  
* **Rolling Upgrade Execution:**  
  * Execute the upgrade following the official OpenShift documentation for **Managed Upgrades**, utilizing the Cluster Version Operator (CVO) to perform a **rolling update** of control plane and worker nodes to minimize application downtime.  
  * Implement necessary **MachineConfigPool (MCP) drains** and updates for worker node OS (RHCOS) to ensure a controlled and non-disruptive process.  
* **Post-Upgrade Health Check and Verification:**  
  * Immediately following the upgrade, execute the complete **OpenShift Core Test Automation Suite** to confirm the cluster is fully functional (e.g., pod scheduling, networking, routing, authentication).  
  * Verify all DCS component operators are in a Succeeded state and performing reconciliations correctly.  
* **Documentation and Communication:**  
  * Document the successful execution, noting any required manual steps or deviations.  
  * Send timely **Application Owner notifications** detailing the planned maintenance window, potential service impact (should be minimal), and confirmation upon successful completion of the upgrade.

---

## **🛡️ Non-Functional Requirements**

*  **Availability (RTO):** The upgrade process must adhere to a non-disruptive, rolling update methodology, ensuring the target RTO (Recovery Time Objective) for tenant applications is zero downtime (service continuity maintained by the scheduler/router).

*  **Resilience:** Robust rollback plans and necessary cluster backups must be established before initiating the upgrade, allowing for immediate recovery in case of catastrophic failure.

*  **Performance:** Post-upgrade, baseline performance metrics (e.g., API response time, network latency) must not regress compared to the pre-upgrade state.

*  **Security:** Security-related operators (e.g., Kyverno, runtime security agents) must be among the first components verified post-upgrade to ensure security policy enforcement remains active.

*  **Compliance:** All upgrade activities must be fully logged and auditable, demonstrating compliance with the internal Change Management process and the manufacturer's supported upgrade paths.

## Roadmap Summary
Upgrade DCS additional core services to latest stable versions via automated, non-disruptive rolling updates.