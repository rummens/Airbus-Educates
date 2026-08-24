# TITLE: Runtime Security Implementation Release 5
# STATE: opened
# PARENT: 220
# LABELS: P::2,complexity::high,subproduct::naaS

## Plan & Overview

Release 5 establishes the core **NeuVector Runtime Security Platform infrastructure** across all Digital Container Service (DCS) OpenShift clusters. The primary objective is to deploy, configure, and secure the central control plane, remote agents, and vulnerability scanner infrastructure without impacting tenant workloads.

This release focuses strictly on the **DCS Platform Team & Infrastructure Admin capabilities**: installing the NeuVector Operator via App-of-Apps, establishing Multi-Cluster Federation (Primary Hub to Remote Spokes), configuring persistent storage, setting up offline CVE database synchronization, integrating LDAP for platform admins, and ensuring zero-impact performance profiles.

---

## Detailed Description

This Epic governs the architectural rollout of SUSE NeuVector across the entire OpenShift fleet. The implementation establishes a **Primary (Hub)** control plane on the management cluster and deploys **Remote (Spoke)** controllers, Enforcer DaemonSets, and Scanner pods across all managed clusters (34+ spoke clusters).

The platform is deployed using a modular, unified Helm chart that conditionally renders Primary or Remote configurations based on `global.mode`. The deployment leverages OpenShift-native operators managed via ArgoCD App-of-Apps pattern. Release 5 guarantees that the platform control plane is highly available, telemetry flow is verified between Hub and Spokes, emergency backups are automated, and infrastructure admins can access the central NeuVector Manager UI using corporate LDAP credentials.

---

## Importance of the Epic

1. **Infrastructure Defense Baseline:** Establishes real-time eBPF container kernel monitoring and deep packet inspection (DPI) capabilities across all OpenShift worker nodes.
2. **Centralized Fleet Governance:** Enables multi-cluster visibility from a single Primary NeuVector Hub, eliminating fragmented security management.
3. **Air-Gapped & Offline Readiness:** Ensures continuous vulnerability scanning in restricted environments by building automated workflows for offline CVE database updates.
4. **Platform Stability:** Completes all heavy infrastructure provisioning, storage configuration, and resource tuning before exposing features to end customers.

---

## Functional Requirements

* **Modular Helm Chart & Operator Lifecycle:**
  
  * Develop a base Helm chart supporting `global.mode: hub | spoke` to conditionally deploy NeuVector `Controller`, `Enforcer`, `Scanner`, and `Manager` components.
  * Integrate NeuVector Operator Subscriptions into existing ArgoCD `App-of-Apps` manifests for automated fleet rollout.


* **Multi-Cluster Federation Setup:**

  * Configure automatic registration of Remote (Spoke) NeuVector instances to the Primary (Hub) NeuVector instance using secure API tokens.


* **Storage, TLS, & Backup Configuration:**
  
  * Provision persistent storage (ReadWriteMany/ReadWriteOnce PVCs) for Controller state and policy data.
  * Configure custom TLS certificates for the NeuVector Manager UI and inter-component REST APIs.
  * Automate scheduled backups of NeuVector configuration state.


* **Offline Vulnerability Update Workflow:**

  * Establish an automated pipeline to pull, package, and sync NeuVector CVE database update images into internal registries for air-gapped clusters.


* **Infrastructure Admin Authentication & RBAC:**

  * Integrate NeuVector Manager UI with corporate LDAP/Active Directory.
  * Define global `Admin` and `Reader` roles mapped strictly to Platform Engineering LDAP groups.


* **Observability & Resource Optimization:**

  * Verify real-time telemetry flow from Spoke Enforcers to the Hub Controller.
  * Benchmark and cap CPU/Memory resource limits for Enforcer DaemonSets and Scanner deployments.



---

## Non-Functional Requirements

* **Low System Overhead:** Enforcer DaemonSets must consume $<2\%$ CPU utilization per node and operate with zero measurable impact on application latency or throughput.
* **Control Plane Resilience:** The Primary Controller must be deployed in a high-availability (3-replica) configuration. Loss of connection between a Spoke Enforcer and the Hub Primary Controller must not impair local agent enforcement capabilities.
* **Security & Least Privilege:** Enforcer containers must run under custom OpenShift Security Context Constraints (SCCs) granting only necessary Linux capabilities (`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_SYS_PTRACE`).
* **mTLS Communication:** All internal communication between Controllers, Enforcers, and Scanners must be encrypted using dynamic mutual TLS.

---

## Roadmap Summary

Deploys the foundational NeuVector control plane and agent fleet across all OpenShift clusters, establishes Hub-Spoke federation, configures storage/TLS/LDAP, and validates system health for Platform Admins.