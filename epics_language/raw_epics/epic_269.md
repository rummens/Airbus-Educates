# TITLE: Runtime Security Implementation Release 6
# STATE: opened
# PARENT: 221
# LABELS: P::1,complexity::high,subproduct::naaS

## Plan & Overview

Release 6 shifts focus from infrastructure setup to **Tenant Usability, Automated Enforcement, GitOps Self-Service, and Enterprise Integration**. The goal is to active runtime protection for application workloads, provide application owners with multi-tenant visibility into their specific namespaces, automate security exception management via `dcs-customer-instances`, and stream audit events to Splunk and Prometheus.

This release targets **Tenant Application Owners & Security Operations Teams**: enforcing baseline process/network policies using NeuVector Custom Resource Definitions (`NvClusterSecurityRule`), wiring tenant OIDC SSO to namespace-scoped roles, and establishing self-service CVE/Runtime exception workflows.

---

## Detailed Description

This Epic turns NeuVector into a multi-tenant, self-service security solution for DCS customers. It introduces namespace-scoped role mapping via OpenShift OIDC, ensuring customer teams only see policy violations, vulnerabilities, and network graphs relevant to their assigned namespaces.

Release 6 replaces manual policy creation with **Security as Code**. Global security baselines (prohibiting unmanaged shell execution, sensitive file tampering, and unauthorized egress) are deployed using NeuVector CRDs (`NvClusterSecurityRule` and `NvAdmissionControlPolicy`). To give tenants flexibility without compromising safety, the `dcs-customer-instances` Helm chart is extended to allow tenants to request CVE deferrals, binary whitelisting, and network ingress/egress exceptions directly through GitOps Pull Requests. Finally, security incidents are routed to central SIEM (Splunk) and Prometheus/Alertmanager for real-time alerting.

---

## Importance of the Epic

1. **Shift-Left & Runtime Convergence:** Bridges static image scanning with real-time runtime protection by validating running container behavior against approved baselines.
2. **Multi-Tenant Self-Service:** Empowers application teams to inspect their own security posture and request exceptions via GitOps without granting them elevated cluster access.
3. **Automated Threat Response:** Automatically isolates compromised pods or kills malicious processes before lateral movement occurs inside the cluster.
4. **Enterprise Observability:** Connects runtime security event logs to central SOC dashboards (Splunk) and operational monitoring (Grafana/Alertmanager).

---

## Functional Requirements

* **Multi-Tenant OIDC Authentication & Namespace RBAC:**

  * Integrate NeuVector Manager UI with OpenShift OIDC provider for tenant authentication.
  * Automate fine-grained RBAC mapping to restrict customer visibility strictly to their provisioned namespaces (`Reader`/`CI/CD` roles per namespace).


* **Global Security Policy Enforcement (GitOps):**

  * Formalize and enforce global vulnerability management policies using NeuVector `NvAdmissionControlPolicy` objects (e.g., block deployment of Critical unpatched CVEs).
  * Enforce baseline runtime process rules (`Discover` -> `Monitor` -> `Protect` modes) prohibiting root execution, interactive shells, and system directory modifications.
  * Enforce zero-trust microsegmentation using `NvClusterSecurityRule` objects.


* **Customer Self-Service Exception Engine:**

  * Extend `dcs-customer-instances` Helm chart to support:
  * **CVE Deferrals:** Suppress specific CVE findings per tenant with mandatory expiration dates.
  * **Process Whitelisting:** Allow specific custom binaries via tenant values files rendering `NvSecurityRule` CRDs.
  * **Network Exceptions:** Allow specific cross-namespace egress/ingress rules rendering `NvSecurityRule` CRDs.


* **SIEM & Monitoring Integration:**

  * Configure NeuVector syslog export to send security events, audit logs, and packet capture triggers directly to Splunk.
  * Expose NeuVector Prometheus metrics endpoints and create Grafana dashboards for policy violations, enforcer health, and scanner status.
  * Route critical threat alerts to Alertmanager and PagerDuty/Slack channels.

* **Tenant Documentation & Training:**

  * Deliver comprehensive User Guides for tenants explaining how to access their NeuVector UI, interpret findings, and submit GitOps exception requests.



---

## Non-Functional Requirements

* **Sub-Second Enforcement Latency:** Policy violation detection and automated enforcement (pod kill or network quarantine) must occur within $<1$ second of occurrence.
* **Strict Data Isolation:** Multi-tenant configuration must guarantee that Tenant A cannot view container logs, network maps, or vulnerability reports belonging to Tenant B under any circumstance.
* **Non-Disruptive Exception Workflow:** Applying a GitOps exception via `NvSecurityRule` must reconcile within seconds without causing pod restarts or service downtime.
* **Usable Alerting:** Alerts sent to application owners must be actionable, containing the cluster, namespace, pod name, violating rule/binary, and a link to the remediation guide.

---

## Roadmap Summary

Enables tenant SSO and namespace isolation, automates policy enforcement via NeuVector CRDs, implements self-service GitOps exceptions in customer charts, and integrates security telemetry into Splunk and Prometheus.