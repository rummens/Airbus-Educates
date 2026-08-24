# TITLE: Cross Country Metric Aggregation
# STATE: opened
# PARENT: 220
# LABELS: P::2,complexity::medium,subproduct::naaS

## 📋 Description

As the Digital Container Service (DCS) expands across multiple isolated national instances alongside our shared central instance, the platform operations and product teams lack a unified "Single Pane of Glass" to monitor global fleet health, software compliance, resource capacity, and test stability.

This Epic focuses on designing, validating, and implementing a centralized metric aggregation framework. The core challenge is achieving global visibility while strictly adhering to the security and isolation boundaries required by national environments.

---

## 🏗️ Strict Architectural Principle

> ⚠️ **CRITICAL CONSTRAINT:** The network data flow for all monitoring, metrics, and heartbeats must **always originate from the National Cluster and push outbound to the Central Cluster**. The Central Cluster must **never** initiate inbound network connections to any national instance.

---

## 🎯 Business Value & Objectives

* **Proactive Global Operations:** Enable the central Operations Team to detect critical outages or infrastructure degradation in any national instance instantly without manual intervention.
* **Cost & Capacity Optimization:** Track global hardware footprints (including expensive GPU resources) and developer adoption (DevSpaces) to forecast infrastructure investment and understand platform utilization.
* **Risk & Drift Mitigation:** Ensure all national deployments remain aligned with central software releases by identifying Helm chart version drift.
* **Secure Compliance Tracking:** Measure the continuous testing stability of isolated clusters globally without violating regional data residency or log-sharing constraints.

---

## 🔍 Scope

### **In Scope:**

* **Architecture Validation:** Conducting a PoC for push-based metric routing (e.g., Prometheus `remote_write`, Thanos Receive, or Pushgateway architectures).
* **Platform Component Health:** Aggregating high-level uptime and availability metrics of core Kubernetes/OpenShift control plane elements.
* **Version Governance:** Gathering deployed Helm chart versions and visualizing cluster compliance baselines.
* **Advanced Tenancy Tracking:** Collecting infrastructure metrics (CPU, Memory, Storage, GPUs) and tenancy counts (Users, Tenants, Dev-type vs. Prod-type Namespaces, and DevSpaces).
* **Anonymized Test Metrics:** Ingesting binary (pass/fail) pipeline test results centrally.

### **Out of Scope:**

* **Centralized Log Collection:** Centralized aggregation of raw application or system logs is strictly forbidden due to data privacy policies.
* **Centralized Trace Collection:** Distributed tracing ingestion into the central instance is out of scope for this phase.
* **Cross-Cluster Control Actions:** This framework is strictly for observability; pushing configuration changes from Central to National clusters via this network path is prohibited.

---

## 🏁 Success Criteria

1. **Zero Firewall Violations:** 100% of the metric traffic is verified as outbound-only from national networks.
2. **Unified Global Dashboards:** Central Grafana provides executive and operational views showing accurate global aggregates alongside per-country filtering.
3. **Automated Drift Detection:** The central system successfully flags any national cluster running an unapproved or outdated platform Helm chart version.
4. **Data Privacy Compliance:** Security audit confirms that no application log data or sensitive tenant data is leaked during test result aggregation.

---

## 📈 Milestones / Key Deliverables

* **Phase 1:** Unidirectional Network & Push Mechanism PoC Sign-off
* **Phase 2:** Global Helm Chart Version Tracking Rollout
* **Phase 3:** Infrastructure Capacity, GPU, and DevSpaces Dashboard Delivery
* **Phase 4:** Global Component Health & Anonymized Test Results Ingestion


## Roadmap Summary

Aggregate key metrics from the countries centrally to enhance oversight of central team and ensure service likeness in all countries.