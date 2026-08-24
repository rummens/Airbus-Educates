# TITLE: Platform Enablement for Mistral On-Premise AI Multi-Tenant Stack
# STATE: opened
# PARENT: 220
# LABELS: P::1,complexity::high,subproduct::infrastructure

## Description

The goal of this Epic is to deliver the underlying platform infrastructure, automation, and operational support necessary to deploy the Mistral On-Premise AI stack in a multi-tenant architecture. All platform deployments must be managed declaratively via **ArgoCD** and **Helm charts**. The deployment sequence will begin with initial validation in the **Sandbox cluster**, followed by provisioning and hardening a **dedicated virtual cluster (vcluster)** equipped with GPU access.

## Core Objectives

1. Mirror all required artifacts (images, Helm charts) to internal secure registries.
2. Deploy and automate [foundational operators ](https://docs.google.com/spreadsheets/d/1tiPVchs60PPPDy3JTkjhnX1_xRt5fqZLTZGDUFDWOYM/edit?usp=drive_open&ouid=116085123195042424036)(ClickHouse, APISIX, Temporal) as individual lifecycle units with robust test suites.
3. Establish a secure workaround for OpenShift/APISIX cluster-scoped RBAC limitations.
4. Deliver an isolated, GPU-enabled virtual cluster for the Mistral multi-tenant workload.
5. Provide a global blueprint and documentation for rapid replication across other country clusters.
6. Provide operational hypercare support to the Application team during onboarding.

## Success Criteria

* Mistral base Helm charts can be successfully rendered and deployed via ArgoCD without manual interventions.
* The APISIX Ingress Controller functions seamlessly behind an OpenShift Passthrough Route.
* Virtual cluster workloads can seamlessly leverage underlying physical GPU resources.
* The Application team successfully deploys their components with zero structural platform blockers.

## Documentation

All documentation of Mistral can be found here (access needs to be requested): https://docs-onprem.mistral.ai

### CRD list (old)
[Mistral_Studio_-_CRDs.xlsx](/uploads/2842e7f33cd57e3b4f99cdab4a09c181/Mistral_Studio_-_CRDs.xlsx)

### Commercial Deployment Troubles/Report
https://docs.google.com/document/d/1ArTyk2CAT6ea43JOlNpXQxvnPIBbdct2/edit?usp=drive_link&ouid=116085123195042424036&rtpof=true&sd=true

### Potential new Cluster design
https://docs.google.com/drawings/d/1RWrOH1rrdVEpDJ0Cr_cOAVLwTwpnfyjzCdSIct89N5k/edit


## Roadmap Summary
Bring the Mistral AI Suite to DCS, so the company can use its services.