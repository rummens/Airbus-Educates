# TITLE: DCS Uptime Tracking and Status Page (SLA)
# STATE: opened
# PARENT: 220
# LABELS: P::2,complexity::medium,external-support,subproduct::naaS

~~_Note: This might require the onboarding of DCS into CheckMK first. CheckMK is the standard Airbus monitoring tool, which sits outside of DCS and can act as a external whitness._~~


## **⏱️ Epic Description**

This Epic is focused on establishing a transparent and automated system for **tracking and publicly displaying the uptime and operational status** of the Digital Container Service (DCS) platform. The primary objective is to define the critical **Key Metrics** that accurately represent the platform's health and availability and to leverage a centralized, external monitoring tool, such as **CheckMK**, to act as an external witness for non-disputable uptime tracking. The final deliverables include an internal **Grafana Dashboard** for continuous tracking and a public-facing **Status Page** to communicate the current operational status to internal development teams and stakeholders.

---

## **📈 Importance of the Epic**

Transparently tracking and reporting uptime is **essential for building customer trust and meeting Service Level Agreements (SLAs)**. This Epic is critical because it:

1. **Increases Transparency:** Provides a single, definitive source of truth regarding the platform's health, reducing support inquiries during outages.  
2. **Validates SLAs:** Formalizes the measurement process using an external witness (e.g., CheckMK), ensuring unbiased, auditable tracking of service availability metrics.  
3. **Standardizes Communication:** Ensures consistent and immediate communication to all customers about planned maintenance and current service disruptions across all deployment environments.

---

## **✅ Functional Requirements**

The solution must be built on clear metric definitions and robust exposure mechanisms:

* **Key Metric Definition and Source:**  
  * The project must first **Define Key Metrics which defines Up Status of DCS**. These metrics must cover core platform components like the API server responsiveness, Ingress/Routing layer health, and authentication service availability.  
  * The primary source for uptime calculation should be an external monitoring system like **CheckMK** (requiring onboarding into this tool first, as noted), which acts as the neutral, external witness.  
* **Internal Tracking Dashboard:**  
  * **Build a Grafana Dashboard to track up status with a timer**. This internal dashboard will consume data from the external witness (CheckMK) and the internal monitoring stack (Prometheus) to provide a real-time, minute-by-minute view of platform health, historical uptime percentages, and ongoing incident timers for the Platform Operations team.  
* **Public Status Page Implementation and Deployment:**  
  * **Build and expose a Status page for customers to see the current status**. This page must be easily accessible and securely hosted, displaying the defined key metrics and showing the current status (e.g., "Operational," "Degraded Performance," "Major Outage").  
  * **Deploy the Status Page to all countries/national environments**. The deployment architecture must allow the public page to reflect the current status of the specific cluster(s) serving each national environment.  
* **Integration and Automation:** The Status Page must be configured to automatically update its status based on the defined metrics and alerts, minimizing manual intervention during incidents.

---

## **🛡️ Non-Functional Requirements**

* **Accuracy:** Uptime measurement must be based on the external CheckMK witness, ensuring accuracy and objectivity in tracking service availability.

* **Availability:** The Status Page service itself must be hosted outside the DCS platform (or in a highly redundant, dedicated environment) to ensure it remains available and reachable even during a major DCS outage.

* **Latency:** The status displayed on the public page must be updated near real-time (e.g., within 60 seconds) following a major status change.

* **Security:** The Status Page must be secured against malicious access and configured to prevent the exposure of internal performance data or system details.

* **Scalability:** The Status Page solution must be horizontally scalable to easily incorporate status tracking for additional DCS clusters as the platform expands geographically.

## Roadmap Summary
Gemini said
Automates DCS uptime tracking via CheckMK and Grafana, providing internal dashboards and a public status page for platform health transparency.